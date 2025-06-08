import re

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class Model:
    def __init__(self, path: str):
        tokenizer = AutoTokenizer.from_pretrained(path)
        model = AutoModelForCausalLM.from_pretrained(path)
        self.generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

    @staticmethod
    def extract_level(text: str) -> str:
        """Extract X/O grid from generated text after <|level|> token."""
        split = text.split("<|level|>")
        after_level = split[1]
        clean = re.sub(r"[^OX]", "", after_level)
        filtered_grid = clean.strip().splitlines()
        return filtered_grid

    def generate(self, prompt: str, max_new_tokens: int = 100) -> str:
        if self.generator is None:
            raise ValueError("Model is not loaded. Please call load_weights() first.")

        formatted_prompt = (
            f"<|label|> {prompt}, where X is a wall and O is a free space <|level|>\n"
        )

        result = self.generator(
            formatted_prompt, max_new_tokens=max_new_tokens, add_special_tokens=True
        )[0]["generated_text"]

        cleared_result = self.extract_level(result)

        return cleared_result
