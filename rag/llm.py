import os
import json

MODEL_NAME = os.getenv("LLM_MODEL", "claude/haiku-4.5")

if "claude" in MODEL_NAME.lower():
    try:
        from anthropic import Anthropic

        API_KEY = os.getenv("ANTHROPIC_API_KEY")
        if not API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY not set")

        client = Anthropic(api_key=API_KEY)

        class AnthropicLLM:
            def __init__(self, client, model: str = None):
                self.client = client
                self.model = model or "claude-haiku-4.5"

            def invoke(self, prompt: str):
                resp = self.client.completions.create(
                    model=self.model,
                    prompt=prompt,
                    max_tokens_to_sample=512,
                    temperature=0.1
                )

                class Resp:
                    def __init__(self, text):
                        self.content = text

                text = resp.completion if hasattr(resp, 'completion') else str(resp)
                return Resp(text)

        llm = AnthropicLLM(client, model=MODEL_NAME.split('/')[-1])
        print(f"Using Anthropic model: {MODEL_NAME}")

    except Exception as e:
        print(f"Failed to initialize Anthropic client ({e}), falling back to HuggingFace pipeline")
        MODEL_NAME = os.getenv("FALLBACK_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")

        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
            import torch
            from langchain_huggingface import HuggingFacePipeline

            device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
            print(f"Using device: {device}")
            print(f"Loading {MODEL_NAME}...")

            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                dtype=torch.float16,
                low_cpu_mem_usage=True
            ).to(device)

            hf_pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=256,
                temperature=0.1,
                do_sample=True,
                return_full_text=False,
                device=device
            )

            llm = HuggingFacePipeline(pipeline=hf_pipeline)
            print("Fallback model loaded successfully")
        except Exception as e2:
            print(f"Failed to load fallback model: {e2}")
            # Minimal stub to avoid crashes
            class StubLLM:
                def invoke(self, prompt: str):
                    class R:
                        def __init__(self, text):
                            self.content = text
                    return R("")

            llm = StubLLM()

else:
    # Non-Anthropic flow: try to load a HF model
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        import torch
        from langchain_huggingface import HuggingFacePipeline

        device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"Using device: {device}")
        print(f"Loading {MODEL_NAME}...")

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            dtype=torch.float16,
            low_cpu_mem_usage=True
        ).to(device)

        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=256,
            temperature=0.1,
            do_sample=True,
            return_full_text=False,
            device=device
        )

        llm = HuggingFacePipeline(pipeline=hf_pipeline)
        print("Model loaded successfully!")

    except Exception as e:
        print(f"Failed to load model {MODEL_NAME}: {e}")
        class StubLLM:
            def invoke(self, prompt: str):
                class R:
                    def __init__(self, text):
                        self.content = text
                return R("")

        llm = StubLLM()