from datetime import datetime
from llm import LlmTemplate
import anthropic

class LlmClaude(LlmTemplate):
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
            claude_api_key,
            model
        ):
        super().__init__(api_key=claude_api_key, model=model)

    def _get_valid_models(self):
        return ['claude-2.0', 'claude-instant-1.2', 'claude-3-sonnet-20240229',
                'claude-3-opus-20240229', 'claude-3-haiku-20240229', 'claude-2.1']

    def _get_price(
            self,
            completion
        ):
        prices = {
            'claude-2.0': {'input': 8, 'output': 24},
            'claude-instant-1.2': {'input': .8, 'output': 2.4},
            'claude-3-sonnet-20240229': {'input': 3, 'output': 15},
            'claude-3-opus-20240229': {'input': 15, 'output': 75},
            'claude-3-haiku-20240229': {'input': .25, 'output': 1.25},
            'claude-2.1': {'input': 8, 'output': 24}
        }
        model_price = prices[self.model]
        input_price = completion.usage.input_tokens * model_price['input'] / 1_000_000
        output_price = completion.usage.output_tokens * model_price['output'] / 1_000_000
        return input_price + output_price

    def get_completion(
            self,
            system,
            prompt,
            max_tokens=None
        ):
        """
        Args:
            system: 
            prompt: 
            max_tokens: 
        
        Returns:
            completion: 
        """
        start_time = datetime.now()
        completion = anthropic.Anthropic(api_key = self.api_key).messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[
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
                    'completion': completion.content[0].text,
                    'input_token': completion.usage.input_tokens,
                    'output_token': completion.usage.output_tokens,
                    'price': self._get_price(completion)
                }

        self._store_last_completion(completion.id)
        self._add_stats(tokens=self.last_completion['input_token'] + self.last_completion['output_token'])

        return self.last_completion
