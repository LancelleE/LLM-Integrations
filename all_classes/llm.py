import json

class LlmTemplate:
    """
    This class presents a template for working with various LLMs.

    Methods:
        __init__: initialization, pick a model
        _validate_model: make sure the wanted model exists
        _get_price: calculate the price of each completion
        _store_last_completion: stores the output in a JSON file
        get_completion: return the completion based on a prompt and a system.
    """
    def __init__(
            self,
            api_key,
            model
        ):
        self.api_key = api_key
        self.model = model
        self.last_completion = None
        self.nb_session_completions = 0
        self.nb_session_tokens = 0
        self._validate_model(model)

    def __repr__(self):
        return(
            f"""
               Model: {self.model}
               Nb completions: {self.nb_session_completions}
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
        valid_models = self._get_valid_models()
        if model not in valid_models:
            raise ValueError(f"Invalid model. Please choose from {valid_models}")

    def _get_valid_models(self):
        raise NotImplementedError("Subclasses must implement _get_valid_models method")

    def _get_price(
            self,
            completion
        ):
        raise NotImplementedError("Subclasses must implement _get_price method")

    def _store_last_completion(
            self,
            message_id
        ):
        filename = "history/last_completion.json"
        try:
            with open(filename, "r", encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}

        data[message_id] = self.last_completion

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f)


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
        raise NotImplementedError("Subclasses must implement get_completion method")
