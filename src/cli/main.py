"""
Main CLI Application for Clash Royale RAG System

Features:
- Interactive Q&A mode
- Streaming output
- Rich formatting
- Command system
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.cli.display import CLIDisplay, console
from src.rag_v2.pipeline import RAGPipeline
from rag.llm import llm  # Import from original llm module
from rich.prompt import Prompt


class ClashRoyaleCLI:
    """Interactive CLI for Clash Royale Knowledge Graph RAG"""

    def __init__(self):
        self.display = CLIDisplay()
        self.pipeline = None
        self.verbose = False
        self.running = True

    def initialize(self):
        """Initialize the RAG pipeline"""
        self.display.print_info("Loading language model...")

        try:
            self.pipeline = RAGPipeline(llm, verbose=self.verbose)

            if not self.pipeline.test_connection():
                self.display.print_error("Failed to connect to Neo4j database")
                self.display.print_info("Please ensure Neo4j is running and credentials are correct in .env file")
                return False

            self.display.print_success("Successfully connected to knowledge graph")
            return True

        except Exception as e:
            self.display.print_error(f"Failed to initialize: {e}")
            return False

    def run(self):
        """Run the interactive CLI"""
        self.display.clear()
        self.display.print_header("Clash Royale Knowledge Graph RAG System")

        # Initialize
        if not self.initialize():
            return

        self.display.print_info("Type your question, or /help for commands, /exit to quit")
        console.print()

        # Main loop
        while self.running:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    self.handle_command(user_input)
                else:
                    # Process question
                    self.process_question(user_input)

            except KeyboardInterrupt:
                console.print("\n")
                self.display.print_info("Use /exit to quit")
                continue
            except EOFError:
                break
            except Exception as e:
                self.display.print_error(f"Unexpected error: {e}")

        # Cleanup
        self.shutdown()

    def process_question(self, question: str):
        """Process a user question"""
        console.print()

        try:
            self.process_question_streaming(question)

        except Exception as e:
            self.display.print_error(f"Error processing question: {e}")

    def process_question_streaming(self, question: str):
        """Process question with streaming output"""
        current_stage = None
        answer_text = ""

        for stage, content in self.pipeline.query_with_streaming(question):
            if stage == "info":
                # Display info messages (corrections, alternatives, etc.)
                console.print()
                console.print(f"[bold yellow]ℹ️  {content}[/bold yellow]")
                console.print()

            elif stage == "cypher":
                if current_stage != "cypher":
                    if self.verbose:
                        self.display.print_info("🔧 Translating to Cypher...")
                    current_stage = "cypher"
                if self.verbose and content and not content.startswith("Translating"):
                    self.display.print_cypher(content)

            elif stage == "retrieval":
                if current_stage != "retrieval":
                    if self.verbose:
                        console.print()
                        self.display.print_info("🔍 Searching knowledge graph...")
                    current_stage = "retrieval"
                if self.verbose and "Found" in content:
                    self.display.print_info(f"  {content}")

            elif stage == "generation":
                if current_stage != "generation":
                    console.print()
                    console.print("[bold green]Answer:[/bold green]", end=" ")
                    current_stage = "generation"

                # Stream the answer word by word
                if not content.startswith("Generating"):
                    console.print(content, end="")
                    answer_text += content

            elif stage == "error":
                console.print()
                self.display.print_error(content)
                return

            elif stage == "done":
                # Print final metadata
                console.print("\n")

                if self.verbose and content.get("sources"):
                    self.display.print_info("Sources: " + ", ".join(content["sources"]))

                if self.verbose and content.get("confidence"):
                    conf = content["confidence"]
                    conf_color = "green" if conf >= 0.8 else "yellow" if conf >= 0.6 else "red"
                    console.print(f"[dim]Confidence:[/dim] [{conf_color}]{conf:.0%}[/{conf_color}]")

                if self.verbose and content.get("cypher"):
                    console.print()
                    self.display.print_info("Cypher Query:")
                    console.print(f"[dim]{content['cypher']}[/dim]")

        console.print()

    def handle_command(self, command: str):
        """Handle CLI commands"""
        cmd = command.lower().strip()

        if cmd in ["/exit", "/quit", "/q"]:
            self.running = False
            console.print("\n[bold cyan]Goodbye![/bold cyan]\n")

        elif cmd == "/help":
            console.print()
            self.display.print_help()

        elif cmd == "/examples":
            console.print()
            self.display.print_examples()

        elif cmd == "/stats":
            console.print()
            self.display.print_info("Fetching knowledge graph statistics...")
            stats = self.pipeline.get_stats()
            if stats:
                self.display.print_stats(stats)
            else:
                self.display.print_error("Could not retrieve statistics")

        elif cmd == "/verbose":
            self.verbose = not self.verbose
            self.pipeline.verbose = self.verbose
            status = "ON" if self.verbose else "OFF"
            self.display.print_success(f"Verbose mode: {status}")

        elif cmd == "/clear":
            self.display.clear()
            self.display.print_header("Clash Royale Knowledge Graph RAG System")

        else:
            self.display.print_error(f"Unknown command: {command}")
            self.display.print_info("Type /help for available commands")

    def shutdown(self):
        """Cleanup resources"""
        if self.pipeline:
            self.pipeline.close()


def main():
    """Entry point"""
    cli = ClashRoyaleCLI()
    cli.run()


if __name__ == "__main__":
    main()
