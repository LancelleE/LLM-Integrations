from datetime import datetime
from all_classes.llm import LlmTemplate
from openai import OpenAI

class LlmOpenAi(LlmTemplate):
    """
    This class presents an easy way to work with Anthropic's Claude.

    Methods:
        __init__: initialization, pick a model
        _get_valid_models: return valid models for this class
        _get_price: calculate the price of each completion
        get_completion: return Claude's completion based on a prompt and a system.
    """
    def __init__(
            self,
            openai_api_key,
            model
        ):
        super().__init__(api_key=openai_api_key, model=model)

    def _get_valid_models(self):
        return ['gpt-4-0125-preview','gpt-4','gpt-3.5-turbo-0125']

    def _get_price(
            self,
            completion
        ):
        prices = {
            'gpt-4-0125-preview': {'input': 10, 'output': 30},
            'gpt-4': {'input': 30, 'output': 60},
            'gpt-3.5-turbo-0125': {'input': .5, 'output': 1.5}
        }
        model_price = prices[self.model]
        input_price = completion.usage.prompt_tokens * model_price['input'] / 1_000_000
        output_price = completion.usage.completion_tokens * model_price['output'] / 1_000_000
        return input_price + output_price

    def get_completion(
            self,
            system,
            prompt,
            max_tokens=None
        ):
        start_time = datetime.now()
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        )

        duration = datetime.now() - start_time

        self.last_completion = {
                    'model': self.model,
                    'datetime': str(start_time),
                    'duration_sec': duration.total_seconds(),
                    'system': system,
                    'prompt': prompt,
                    'completion': response.choices[0].message.content,
                    'input_token': response.usage.completion_tokens,
                    'output_token': response.usage.prompt_tokens,
                    'price': self._get_price(response)
                }

        self._store_last_completion(response.id)
        self._add_stats(tokens=self.last_completion['input_token'] + self.last_completion['output_token'])

        return self.last_completion
