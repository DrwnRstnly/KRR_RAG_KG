"""
Rich CLI display utilities with colored output and formatting
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from typing import List, Dict, Any
import sys

console = Console()


class CLIDisplay:
    """Handles formatted CLI output"""

    @staticmethod
    def print_header(title: str):
        """Print a header banner"""
        console.print()
        console.print(Panel(f"[bold cyan]{title}[/bold cyan]", style="bold blue"))
        console.print()

    @staticmethod
    def print_question(question: str):
        """Print the user's question"""
        console.print(f"[bold yellow]Question:[/bold yellow] {question}")
        console.print()

    @staticmethod
    def print_cypher(cypher: str):
        """Print Cypher query with syntax highlighting"""
        console.print("[dim]Generated Cypher Query:[/dim]")
        syntax = Syntax(cypher, "cypher", theme="monokai", line_numbers=False)
        console.print(syntax)
        console.print()

    @staticmethod
    def print_answer(answer: str, sources: List[str] = None, confidence: float = None):
        """Print the answer with formatting"""
        # Answer
        console.print("[bold green]Answer:[/bold green]")
        console.print(f"  {answer}")
        console.print()

        # Sources
        if sources:
            console.print("[dim]Sources:[/dim]")
            for source in sources:
                console.print(f"  • {source}")
            console.print()

        # Confidence
        if confidence is not None:
            confidence_color = "green" if confidence >= 0.8 else "yellow" if confidence >= 0.6 else "red"
            console.print(f"[dim]Confidence:[/dim] [{confidence_color}]{confidence:.0%}[/{confidence_color}]")
            console.print()

    @staticmethod
    def print_error(error: str):
        """Print error message"""
        console.print(f"[bold red]Error:[/bold red] {error}")
        console.print()

    @staticmethod
    def print_info(message: str):
        """Print info message"""
        console.print(f"[dim]{message}[/dim]")

    @staticmethod
    def print_success(message: str):
        """Print success message"""
        console.print(f"[bold green][OK][/bold green] {message}")

    @staticmethod
    def print_stats(stats: Dict[str, Any]):
        """Print knowledge graph statistics"""
        table = Table(title="Knowledge Graph Statistics", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta", justify="right")

        for key, value in stats.items():
            formatted_key = key.replace("_", " ").title()
            table.add_row(formatted_key, str(value))

        console.print(table)
        console.print()

    @staticmethod
    def print_help():
        """Print help menu"""
        help_text = """
# Clash Royale Knowledge Graph RAG System

## Available Commands:

- **Ask questions** - Just type your question and press Enter
- `/stats` - Show knowledge graph statistics
- `/examples` - Show example questions
- `/verbose` - Toggle verbose mode (show intermediate steps)
- `/clear` - Clear screen
- `/help` - Show this help menu
- `/exit` or `/quit` - Exit the program

## Example Questions:

- What is the elixir cost of the Giant?
- Which cards can hit air units?
- What are all Legendary cards?
- Which cards counter P.E.K.K.A?
- What cards synergize with Giant?
- Compare Musketeer and Wizard stats

## Features:

- 🎯 Natural language to Cypher query translation
- 🔍 Retrieval from Neo4j knowledge graph
- 🤖 AI-generated answers with source grounding
- ⚡ Streaming output for better UX
- 📊 Rich formatted display
        """
        md = Markdown(help_text)
        console.print(md)
        console.print()

    @staticmethod
    def print_examples():
        """Print example questions"""
        table = Table(title="Example Questions", show_header=True)
        table.add_column("Category", style="cyan")
        table.add_column("Question", style="white")

        examples = [
            ("Basic Stats", "What is the HP of the Giant?"),
            ("Basic Stats", "How much elixir does Fireball cost?"),
            ("Filtering", "Which cards can hit air units?"),
            ("Filtering", "Show me all Legendary cards"),
            ("Filtering", "What are the cheapest spell cards?"),
            ("Comparison", "Compare Musketeer and Wizard"),
            ("Relationships", "Which cards counter P.E.K.K.A?"),
            ("Relationships", "What cards synergize with Giant?"),
            ("Archetypes", "Which cards fit the Beatdown archetype?"),
        ]

        for category, question in examples:
            table.add_row(category, question)

        console.print(table)
        console.print()

    @staticmethod
    def create_progress():
        """Create a progress indicator"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        )

    @staticmethod
    def stream_text(text_generator):
        """Stream text output with Live display"""
        with Live("", console=console, refresh_per_second=20) as live:
            accumulated_text = ""
            for chunk in text_generator:
                accumulated_text += chunk
                live.update(accumulated_text)

    @staticmethod
    def clear():
        """Clear the console"""
        console.clear()


def print_header(title: str):
    CLIDisplay.print_header(title)


def print_question(question: str):
    CLIDisplay.print_question(question)


def print_cypher(cypher: str):
    CLIDisplay.print_cypher(cypher)


def print_answer(answer: str, sources: List[str] = None, confidence: float = None):
    CLIDisplay.print_answer(answer, sources, confidence)


def print_error(error: str):
    CLIDisplay.print_error(error)


def print_info(message: str):
    CLIDisplay.print_info(message)


def print_success(message: str):
    CLIDisplay.print_success(message)
