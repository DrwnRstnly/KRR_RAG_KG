"""
System Test Script

Runs basic tests to verify the RAG system is working correctly.
"""

import sys
from rich.console import Console
from rich.table import Table

console = Console()


def test_imports():
    """Test if all modules can be imported"""
    console.print("\n[bold]1. Testing Imports...[/bold]")

    try:
        from src.domain.models import Card, RAGResponse
        from src.kg.schema import KGSchema
        from src.kg.ingestion import KnowledgeGraphIngestion
        from src.rag_v2.translator import QueryTranslator
        from src.rag_v2.retriever import KGRetriever
        from src.rag_v2.generator import AnswerGenerator
        from src.rag_v2.pipeline import RAGPipeline
        from src.cli.display import CLIDisplay
        from src.services.rag_service import RAGService

        console.print("  [green]✓[/green] All modules imported successfully")
        return True
    except ImportError as e:
        console.print(f"  [red]✗[/red] Import failed: {e}")
        return False


def test_neo4j_connection():
    """Test Neo4j connection"""
    console.print("\n[bold]2. Testing Neo4j Connection...[/bold]")

    try:
        from src.rag_v2.retriever import KGRetriever

        retriever = KGRetriever()
        if retriever.test_connection():
            console.print("  [green]✓[/green] Neo4j connection successful")
            retriever.close()
            return True
        else:
            console.print("  [red]✗[/red] Neo4j connection failed")
            return False
    except Exception as e:
        console.print(f"  [red]✗[/red] Error: {e}")
        return False


def test_llm_loading():
    """Test LLM loading"""
    console.print("\n[bold]3. Testing LLM Loading...[/bold]")

    try:
        from rag.llm import llm

        # Test simple generation
        result = llm.invoke("Test")
        console.print("  [green]✓[/green] LLM loaded and working")
        return True
    except Exception as e:
        console.print(f"  [red]✗[/red] LLM loading failed: {e}")
        return False


def test_query_translation():
    """Test query translation"""
    console.print("\n[bold]4. Testing Query Translation...[/bold]")

    try:
        from rag.llm import llm
        from src.rag_v2.translator import QueryTranslator

        translator = QueryTranslator(llm)
        cypher = translator.translate("What is the elixir cost of Giant?")

        if cypher and "MATCH" in cypher:
            console.print("  [green]✓[/green] Query translation working")
            console.print(f"    Generated: {cypher[:80]}...")
            return True
        else:
            console.print("  [red]✗[/red] Invalid Cypher generated")
            return False
    except Exception as e:
        console.print(f"  [red]✗[/red] Translation failed: {e}")
        return False


def test_retrieval():
    """Test data retrieval"""
    console.print("\n[bold]5. Testing Data Retrieval...[/bold]")

    try:
        from src.rag_v2.retriever import KGRetriever

        retriever = KGRetriever()
        result = retriever.retrieve("MATCH (c:Card) RETURN c.name AS name LIMIT 5")

        if result.data and len(result.data) > 0:
            console.print("  [green]✓[/green] Data retrieval working")
            console.print(f"    Retrieved {len(result.data)} records")
            retriever.close()
            return True
        else:
            console.print("  [red]✗[/red] No data retrieved")
            console.print("    Have you run the ingestion script?")
            retriever.close()
            return False
    except Exception as e:
        console.print(f"  [red]✗[/red] Retrieval failed: {e}")
        return False


def test_full_pipeline():
    """Test full RAG pipeline"""
    console.print("\n[bold]6. Testing Full RAG Pipeline...[/bold]")

    try:
        from rag.llm import llm
        from src.rag_v2.pipeline import RAGPipeline

        pipeline = RAGPipeline(llm, verbose=False)
        response = pipeline.query("What is the elixir cost of Giant?")

        if response.answer and not response.answer.startswith("I couldn't"):
            console.print("  [green]✓[/green] Full pipeline working")
            console.print(f"    Answer: {response.answer[:100]}...")
            pipeline.close()
            return True
        else:
            console.print("  [red]✗[/red] Pipeline failed to generate answer")
            pipeline.close()
            return False
    except Exception as e:
        console.print(f"  [red]✗[/red] Pipeline test failed: {e}")
        return False


def test_kg_stats():
    """Test knowledge graph statistics"""
    console.print("\n[bold]7. Testing Knowledge Graph Stats...[/bold]")

    try:
        from src.rag_v2.retriever import KGRetriever

        retriever = KGRetriever()
        stats = retriever.get_stats()

        if stats and stats.get("cards", 0) > 0:
            console.print("  [green]✓[/green] Statistics retrieved successfully")

            table = Table(title="Knowledge Graph Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Count", style="magenta", justify="right")

            for key, value in stats.items():
                formatted_key = key.replace("_", " ").title()
                table.add_row(formatted_key, str(value))

            console.print(table)
            retriever.close()
            return True
        else:
            console.print("  [yellow]![/yellow] Stats retrieved but database may be empty")
            console.print("    Have you run the ingestion script?")
            retriever.close()
            return True
    except Exception as e:
        console.print(f"  [red]✗[/red] Stats retrieval failed: {e}")
        return False


def main():
    """Run all tests"""
    console.print("\n[bold cyan]═══ Clash Royale RAG System Tests ═══[/bold cyan]\n")

    tests = [
        ("Imports", test_imports),
        ("Neo4j Connection", test_neo4j_connection),
        ("LLM Loading", test_llm_loading),
        ("Query Translation", test_query_translation),
        ("Data Retrieval", test_retrieval),
        ("Full Pipeline", test_full_pipeline),
        ("KG Statistics", test_kg_stats),
    ]

    results = []

    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Tests interrupted by user[/yellow]")
            sys.exit(1)
        except Exception as e:
            console.print(f"\n[red]Unexpected error in {name}: {e}[/red]")
            results.append((name, False))

    # Summary
    console.print("\n[bold]═══ Test Summary ═══[/bold]\n")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "[green]PASS[/green]" if success else "[red]FAIL[/red]"
        console.print(f"  {status} - {name}")

    console.print(f"\n[bold]Results: {passed}/{total} tests passed[/bold]")

    if passed == total:
        console.print("\n[bold green]✓ All tests passed! System is ready to use.[/bold green]\n")
        console.print("Run: [cyan]python main_v2.py[/cyan] to start the CLI\n")
        return 0
    else:
        console.print("\n[bold yellow]! Some tests failed. Check the errors above.[/bold yellow]\n")
        console.print("Common fixes:")
        console.print("  • Ensure Neo4j is running")
        console.print("  • Run ingestion: [cyan]python -m src.kg.ingestion[/cyan]")
        console.print("  • Check .env configuration\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
