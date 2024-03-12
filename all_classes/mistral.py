from datetime import datetime
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from all_classes.llm import LlmTemplate

class LlmMistral(LlmTemplate):
    """
    This class presents an easy way to work with Anthropic's Claude.

    Methods:
        __init__: initialization, pick a model
        _get_valid_models: return valid models for this class
        _get_price: calculate the price of each completion
        get_completion: return Mistral's completion based on a prompt and a system.
    """
    def __init__(
            self,
            mistral_api_key,
            model
        ):
        self.client = MistralClient(api_key=mistral_api_key)
        super().__init__(api_key=mistral_api_key, model=model)
        

    def _get_valid_models(self):
        return [model.id for model in self.client.list_models().data]
        

    def _get_price(
            self,
            completion
        ):
        prices = {
            'open-mistral-7b': {'input': .25, 'output': .25},
            'open-mixtral-8x7b': {'input': .7, 'output': .7},
            'mistral-small-latest': {'input': 2, 'output': 6},
            'mistral-medium-latest': {'input': 2.7, 'output': 8.1},
            'mistral-large-latest': {'input': 8, 'output': 24}
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
        # fill with completion
        # client = MistralClient(api_key=self.api_key)
        
        response = self.client.chat(
            model = self.model,
            messages = [
                ChatMessage(role='user', content=system),
                ChatMessage(role='user', content=prompt)
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
