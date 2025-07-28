import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.local_llm_interface import LocalLLM

def main():
    llm = LocalLLM(model="llama3")
    print("Testing local LLaMA 3 via Ollama...\n")

    # Ask a simple question
    question = "What is the capital of France?"
    print(f"Question: {question}")
    response = llm.ask(question)
    print(f"Response: {response}\n")

    # Another test
    question = "Write a haiku about local AI models."
    print(f"Question: {question}")
    response = llm.ask(question)
    print(f"Response: {response}\n")

if __name__ == "__main__":
    main()
