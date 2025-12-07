"""
Main Entry Point for Clash Royale Knowledge Graph RAG System (v2)

This is the enhanced version with:
- Better RAG pipeline
- Rich CLI interface
- Streaming support
- Service layer architecture
"""

import sys
import argparse
from src.cli.main import main as cli_main


def main():
    parser = argparse.ArgumentParser(
        description="Clash Royale Knowledge Graph RAG System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_v2.py                    # Start interactive CLI
  python main_v2.py --verbose          # Start CLI with verbose output
  python main_v2.py --help             # Show this help message

For more information, see README.md
        """
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    if args.verbose:
        import os
        os.environ["VERBOSE"] = "true"

    try:
        cli_main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
