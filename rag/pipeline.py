from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from rag.translator import TranslatorRunnable
from rag.retriever import RetrieverRunnable
from rag.answerer import AnswererRunnable

def log_step(data, step_name):
    print(f"\n--- {step_name} ---")
    print(data)
    return data

pipeline = (
    RunnablePassthrough.assign(
        cypher=lambda x: TranslatorRunnable.invoke(x["question"])
    )
    | RunnableLambda(lambda x: log_step(x, "Generated Cypher"))
    | RunnablePassthrough.assign(
        data=lambda x: RetrieverRunnable.invoke(x["cypher"])
    )
    | RunnableLambda(lambda x: log_step(x, "Retrieved Data"))
    | AnswererRunnable
)

def answer_question(question: str):
    return pipeline.invoke({"question": question})