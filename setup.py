import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".env")
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")
LLM_MODEL = os.getenv("LLM_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
LLM_DEVICE = os.getenv("LLM_DEVICE", "cpu")
LLM_MAX_TOKENS = os.getenv("LLM_MAX_TOKENS", "512")
LLM_TEMPERATURE = os.getenv("LLM_TEMPERATURE", "0.1")
VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"

def check_docker():
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        return True
    except:
        return False

def check_neo4j_running():
    try:
        result = subprocess.run(["docker", "ps", "--filter", "name=neo4j"], capture_output=True, text=True)
        return "neo4j" in result.stdout
    except:
        return False

def start_neo4j():
    if check_neo4j_running():
        return True
    compose_file = Path("docker-compose.yml")
    if compose_file.exists():
        try:
            subprocess.run(["docker-compose", "up", "-d", "neo4j"], check=True)
            time.sleep(5)
            return True
        except:
            return False
    else:
        try:
            subprocess.run([
                "docker", "run", "-d",
                "--name", "neo4j",
                "-p", "7687:7687",
                "-p", "7474:7474",
                f"-e NEO4J_AUTH={NEO4J_USER}/{NEO4J_PASSWORD}",
                "neo4j:latest"
            ], check=True)
            time.sleep(5)
            return True
        except:
            return False

def seed_database():
    data_file = Path("data/raw/fandom_arenas_cards.json")
    if not data_file.exists():
        return False
    try:
        env = os.environ.copy()
        env.update({
            "NEO4J_URI": NEO4J_URI,
            "NEO4J_USER": NEO4J_USER,
            "NEO4J_PASSWORD": NEO4J_PASSWORD,
            "LLM_MODEL": LLM_MODEL,
            "LLM_DEVICE": LLM_DEVICE,
            "LLM_MAX_TOKENS": LLM_MAX_TOKENS,
            "LLM_TEMPERATURE": LLM_TEMPERATURE,
            "VERBOSE": str(VERBOSE)
        })
        subprocess.run([sys.executable, "-m", "src.kg.ingestion"], env=env, check=True)
        return True
    except:
        return False

def test_connections():
    try:
        result = subprocess.run([sys.executable, "test_system.py"], check=False)
        return result.returncode == 0
    except:
        return False

def show_menu():
    choice = input("Select option (1-6): ").strip()
    return choice

def main():
    if not check_docker():
        sys.exit(1)
    command = sys.argv[1].lower() if len(sys.argv) > 1 else None
    if command == "neo4j":
        start_neo4j()
    elif command == "seed":
        seed_database()
    elif command == "all":
        start_neo4j()
        seed_database()
    elif command == "test":
        test_connections()
    elif command == "full":
        start_neo4j()
        seed_database()
        test_connections()
    else:
        while True:
            choice = show_menu()
            if choice == "1":
                start_neo4j()
            elif choice == "2":
                seed_database()
            elif choice == "3":
                start_neo4j()
                seed_database()
            elif choice == "4":
                test_connections()
            elif choice == "5":
                start_neo4j()
                seed_database()
                test_connections()
            elif choice == "6":
                break

if __name__ == "__main__":
    main()
