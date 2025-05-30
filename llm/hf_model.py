from .base_model import base_model
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class hf_model(base_model):
    def __init__(self, model_name: str, temperature: float = 0.7, max_tokens: int = 1024):
        super().__init__(model_name, temperature, max_tokens)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map='auto')
        self.model.eval()  # Set the model to evaluation mode

    def generate_by_prompt(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(self.model.device)
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        output = self.model.generate(input_ids=input_ids, attention_mask=attention_mask, max_new_tokens=self.max_tokens, temperature=self.temperature, eos_token_id=self.tokenizer.eos_token_id, pad_token_id=self.tokenizer.pad_token_id)
        generated_text = self.tokenizer.decode(output[0][input_ids.shape[1]:], skip_special_tokens=True)
        return generated_text.strip()
    
    def generate_by_prompt_batch(self, prompts: list[str]) -> list[str]:
        tokenized_chat = self.tokenizer.batch_encode_plus(prompts, return_tensors="pt", padding=True, truncation=True).to(self.model.device)
        input_ids = tokenized_chat['input_ids']
        attention_mask = tokenized_chat['attention_mask']
        outputs = self.model.generate(input_ids=input_ids, attention_mask=attention_mask, max_new_tokens=self.max_tokens, temperature=self.temperature, eos_token_id=self.tokenizer.eos_token_id, pad_token_id=self.tokenizer.pad_token_id)
        response = self.tokenizer.batch_decode(outputs[:, input_ids.shape[1]:], skip_special_tokens=True)
        return [text.strip() for text in response]
    
    def generate_by_template(self, template: list[dict]) -> str:
        tokenized_chat = self.tokenizer.apply_chat_template(
            template,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)
        output = self.model.generate(
            tokenized_chat,
            max_new_tokens=self.max_tokens,
            temperature=self.temperature,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id
        )
        generated_text = self.tokenizer.decode(output[0][tokenized_chat.shape[1]:], skip_special_tokens=True)
        return generated_text.strip()
    
    def generate_by_template_batch(self, templates: list[list[dict]]) -> list[str]:
        tokenized_chats = self.tokenizer.apply_chat_template(
            templates,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)
        outputs = self.model.generate(
            tokenized_chats,
            max_new_tokens=self.max_tokens,
            use_cache=True,
            temperature=self.temperature,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id
        )
        response = self.tokenizer.batch_decode(outputs[:, tokenized_chats.shape[1]:], skip_special_tokens=True)
        return [text.strip() for text in response]

# Example usage
if __name__ == "__main__":
    model = hf_model("deepseek-ai/deepseek-llm-7b-chat", temperature=0.1, max_tokens=1024)
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