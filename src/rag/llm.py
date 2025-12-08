import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # Options: "gemini" or "openrouter"
MODEL_NAME = os.getenv("LLM_MODEL", "gemini-1.5-flash")
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "512"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Debug: Print what was loaded
print(f"[DEBUG] LLM_PROVIDER loaded: '{LLM_PROVIDER}'")
print(f"[DEBUG] MODEL_NAME loaded: '{MODEL_NAME}'")
print(f"[DEBUG] GEMINI_API_KEY exists: {bool(GEMINI_API_KEY)}")
print(f"[DEBUG] OPENROUTER_API_KEY exists: {bool(OPENROUTER_API_KEY)}")

if not OPENROUTER_API_KEY and not GEMINI_API_KEY:
    print("Warning: No API key set. Set either OPENROUTER_API_KEY or GEMINI_API_KEY")
    print("OpenRouter: $env:OPENROUTER_API_KEY='your_key' (https://openrouter.ai/)")
    print("Gemini: $env:GEMINI_API_KEY='your_key' (https://aistudio.google.com/app/apikey)")

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
                "max_tokens": LLM_MAX_TOKENS,
                "temperature": LLM_TEMPERATURE,
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


class GeminiLLM:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model or MODEL_NAME

    def invoke(self, prompt: str):
        if not self.api_key:
            class R:
                def __init__(self, text):
                    self.content = text
            return R("[No API key set. Please set GEMINI_API_KEY environment variable]")

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)

            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=LLM_MAX_TOKENS,
                    temperature=LLM_TEMPERATURE,
                )
            )

            class R:
                def __init__(self, content):
                    self.content = content

            return R(response.text)

        except ImportError:
            print("Error: google-generativeai package not installed.")
            print("Install it with: pip install google-generativeai")
            class R:
                def __init__(self, content):
                    self.content = content
            return R("Error: google-generativeai package not installed")
        except Exception as e:
            print(f"Gemini API error: {e}")
            class R:
                def __init__(self, content):
                    self.content = content
            return R(f"Error: {str(e)}")


# Select LLM based on LLM_PROVIDER environment variable
if LLM_PROVIDER.lower() == "gemini":
    if GEMINI_API_KEY:
        llm = GeminiLLM(api_key=GEMINI_API_KEY, model=MODEL_NAME)
        print(f"Using Gemini model: {MODEL_NAME}")
    else:
        print("Warning: LLM_PROVIDER is set to 'gemini' but GEMINI_API_KEY is not set!")
        print("Falling back to OpenRouter...")
        llm = OpenRouterLLM(api_key=OPENROUTER_API_KEY, model=MODEL_NAME)
        print(f"Using OpenRouter model: {MODEL_NAME}")
elif LLM_PROVIDER.lower() == "openrouter":
    if OPENROUTER_API_KEY:
        llm = OpenRouterLLM(api_key=OPENROUTER_API_KEY, model=MODEL_NAME)
        print(f"Using OpenRouter model: {MODEL_NAME}")
    else:
        print("Warning: LLM_PROVIDER is set to 'openrouter' but OPENROUTER_API_KEY is not set!")
        print("Falling back to Gemini...")
        llm = GeminiLLM(api_key=GEMINI_API_KEY, model=MODEL_NAME)
        print(f"Using Gemini model: {MODEL_NAME}")
else:
    print(f"Warning: Unknown LLM_PROVIDER '{LLM_PROVIDER}'. Valid options: 'gemini' or 'openrouter'")
    print("Defaulting to Gemini...")
    llm = GeminiLLM(api_key=GEMINI_API_KEY, model=MODEL_NAME)
    print(f"Using Gemini model: {MODEL_NAME}")
