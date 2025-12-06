"""Configuration management"""

import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Neo4jConfig:
    """Neo4j database configuration"""
    uri: str
    user: str
    password: str

    @classmethod
    def from_env(cls):
        return cls(
            uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            user=os.getenv("NEO4J_USER", "neo4j"),
            password=os.getenv("NEO4J_PASSWORD", "12345678")
        )


@dataclass
class LLMConfig:
    """Language model configuration"""
    model_name: str
    device: str
    max_tokens: int
    temperature: float

    @classmethod
    def from_env(cls):
        return cls(
            model_name=os.getenv("LLM_MODEL", "claude/haiku-4.5"),
            device=os.getenv("LLM_DEVICE", "auto"),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "512")),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.1"))
        )


@dataclass
class AppConfig:
    """Application configuration"""
    neo4j: Neo4jConfig
    llm: LLMConfig
    verbose: bool

    @classmethod
    def from_env(cls):
        return cls(
            neo4j=Neo4jConfig.from_env(),
            llm=LLMConfig.from_env(),
            verbose=os.getenv("VERBOSE", "false").lower() == "true"
        )


config = AppConfig.from_env()
