"""
Title: Llm classes
Author: ELA

This module contains utility classes for working with LLMs.

Classes:
- LlmClaude.
"""

from datetime import datetime
import json
import anthropic

class LlmClaude:
    """
    This class presents an easy way to work with Anthropic's Claude.

    Methods:
        __init__: initialization, pick a model
        _validate_model: make sure the wanted model exists
        _get_price: calculate the price of each completion
        _store_last_completion: stores the output in a JSON file
        get_completion: return Claude's completion based on a prompt and a system.
    """
    def __init__(
            self,
            claude_api_key,
            model
        ):
        self.claude_api_key = claude_api_key
        self.model = model
        self.last_completion = None
        self.nb_session_completions = 0
        self.nb_session_tokens = 0
        self._validate_model(model)

    def __repr__(self):
        return(
            f"""
               Model : {self.model}\n
               Nb completions : {self.nb_session_completions}\n
               Total tokens: {self.nb_session_tokens}
            """
        )

    def _add_stats(
            self, 
            tokens
        ):
        self.nb_session_completions += 1
        self.nb_session_tokens += tokens

    def _validate_model(
            self, 
            model
        ):
        valid_models = ['claude-2.0', 'claude-instant-1.2', 'claude-3-sonnet-20240229',
                        'claude-3-opus-20240229', 'claude-3-haiku-20240229', 'claude-2.1']
        if model not in valid_models:
            raise ValueError(f"Invalid model. Please choose from {valid_models}")

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

    def _store_last_completion(self, message_id):
        # Define the filename
        filename = "last_completion.json"
        
        try:
            # Try to open the JSON file
            with open(filename, "r", encoding='utf-8') as json_file:
                # Load existing data
                data = json.load(json_file)
        except FileNotFoundError:
            # If file doesn't exist, initialize an empty dictionary
            data = {}

        # Add the last completion associated with the given ID to the dictionary
        data[message_id] = self.last_completion

        # Write the updated data back to the JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)


    def get_completion(
            self,
            system,
            prompt,
            max_tokens = 1024
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
        completion = anthropic.Anthropic(api_key = self.claude_api_key).messages.create(
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
