from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from langchain_huggingface import HuggingFacePipeline

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

print(f"Loading {MODEL_NAME}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float16,
    low_cpu_mem_usage=True
).to(device) 

falcon_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256,
    temperature=0.1, 
    do_sample=True,
    return_full_text=False,
    device=device # Tell pipeline to use the device
)

llm = HuggingFacePipeline(pipeline=falcon_pipeline)
print("Model loaded successfully!")