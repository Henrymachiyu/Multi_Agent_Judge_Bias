from .base_model import base_model
from openai import OpenAI
import retry
import asyncio

# Configure API key
API_KEY = ""

class openai_model(base_model):

    def __init__(self, model_name="gpt-4o-mini", temperature: float = 0.7, max_tokens: int = 1024):
        super().__init__(model_name, temperature, max_tokens)
        self.model_name = model_name
        self.client = OpenAI(api_key=API_KEY)
    
    @retry.retry(tries=5, delay=3)
    def generate_by_prompt(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
        
    @retry.retry(tries=5, delay=3)
    def generate_by_template(self, prompt_template):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=prompt_template,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
    
    @retry.retry(tries=5, delay=3)
    async def _a_get_response_prompt(self, prompt):
        response = self.client.chat.completions.create(
            model= self.model_name,
            messages= [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature= self.temperature,
            max_tokens= self.max_tokens,
        )
        return response.choices[0].message.content
    
    @retry.retry(tries=5, delay=3)
    async def _a_get_response_template(self, prompt_template):
        response = self.client.chat.completions.create(
            model= self.model_name,
            messages= prompt_template,
            temperature= self.temperature,
            max_tokens= self.max_tokens,
        )
        return response.choices[0].message.content
    
    async def _generate_by_prompt_batch(self, prompts: list[str]) -> list[str]:
        tasks = [self._a_get_response_prompt(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks)
        return results
    
    async def _generate_by_template_batch(self, prompt_templates: list[list[dict]]) -> list[str]:
        tasks = [self._a_get_response_template(prompt_template) for prompt_template in prompt_templates]
        results = await asyncio.gather(*tasks)
        return results
    
    def generate_by_prompt_batch(self, prompts: list[str]) -> list[str]:
        return asyncio.run(self._generate_by_prompt_batch(prompts))
    
    def generate_by_template_batch(self, prompt_templates: list[list[dict]]) -> list[str]:
        return asyncio.run(self._generate_by_template_batch(prompt_templates))
    
# Example usage
if __name__ == "__main__":
    model = openai_model("gpt-4o-mini", temperature=0.7, max_tokens=1024)
    prompt = "What is the capital of France?"
    response = model.generate_by_prompt(prompt)
    print("Response to prompt:", response)

    # Example of using generate_by_template
    template = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Translate 'Hello' to French."}
    ]
    response_template = model.generate_by_template(template)
    print("Response to template:", response_template)

    # Example of using generate_by_prompt_batch
    prompts = ["What is the capital of Germany?", "What is 2 + 2?"]
    responses = model.generate_by_prompt_batch(prompts)
    print("Responses to prompt batch:", responses)

    # Example of using generate_by_template_batch
    templates = [
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the largest planet in our solar system?"}
        ],
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who wrote 'Pride and Prejudice'?"}
        ]
    ]
    responses_template_batch = model.generate_by_template_batch(templates)
    print("Responses to template batch:", responses_template_batch)
