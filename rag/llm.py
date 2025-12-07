import os
import requests

MODEL_NAME = os.getenv("LLM_MODEL", "anthropic/claude-3.5-haiku")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("Warning: OPENROUTER_API_KEY not set. Set it via: $env:OPENROUTER_API_KEY='your_key'")
    print("Get a free key at: https://openrouter.ai/")

class OpenRouterLLM:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.model = model or MODEL_NAME
        self.base_url = "https://openrouter.ai/api/v1"

    def invoke(self, prompt: str):
        if not self.api_key:
            class R:
                def __init__(self, text):
                    self.content = text
            return R("[No API key set. Please set OPENROUTER_API_KEY environment variable]")

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,  # Increased from 512
                "temperature": 0.1,
            }

            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if not resp.ok:
                error_detail = ""
                try:
                    error_json = resp.json()
                    error_detail = f"\nAPI Error Details: {error_json}"
                except:
                    error_detail = f"\nResponse Text: {resp.text[:500]}"

                print(f"OpenRouter API HTTP {resp.status_code} error{error_detail}")
                raise requests.HTTPError(f"{resp.status_code} {resp.reason}{error_detail}")

            result = resp.json()

            try:
                text = result["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError) as e:
                print(f"OpenRouter response structure error: {e}")
                print(f"Response: {result}")
                raise ValueError(f"Invalid API response structure: {e}")

            class R:
                def __init__(self, content):
                    self.content = content

            return R(text)

        except Exception as e:
            print(f"OpenRouter API error: {e}")
            class R:
                def __init__(self, content):
                    self.content = content
            return R(f"Error: {str(e)}")


llm = OpenRouterLLM(api_key=OPENROUTER_API_KEY, model=MODEL_NAME)
print(f"Using OpenRouter model: {MODEL_NAME}")
