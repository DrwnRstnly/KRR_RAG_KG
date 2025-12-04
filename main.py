from rag.pipeline import answer_question


def main():
    print("=== Clash Royale Knowledge Graph ===")
    print("Ask about Cards, Rarities, Arenas, and Stats!")
    print("Type 'exit' or 'quit' to leave.")
    print("========================================")

    while True:
        try:
            question = input("\nQuestion: ").strip()

            if question.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not question:
                continue

            print("Thinking...")
            try:
                response = answer_question(question)
                print(f"\nAnswer:\n{response}")
            except Exception as e:
                print(f"\nError processing question: {e}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nUnexpected Error: {e}")

if __name__ == "__main__":
    main()