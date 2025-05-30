from abc import ABC, abstractmethod

### Abstract Class for LLM Models
class base_model(ABC):

    def __init__(self, model_name, temperature: float = 0.7, max_tokens: int = 1024):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    @abstractmethod
    def generate_by_prompt(self, prompt: str) -> str:
        pass

    @abstractmethod
    def generate_by_template(self, prompt_template: list[dict]) -> str:
        pass

    @abstractmethod
    def generate_by_prompt_batch(self, prompt: list[str]) -> list[str]:
        pass

    @abstractmethod
    def generate_by_template_batch(self, prompt: list[list[str]]) -> list[str]:
        pass