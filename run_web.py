
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("Clash Royale Knowledge Graph RAG - Web Interface")
    print("=" * 60)
    print("\nStarting server...")
    print("Open your browser and navigate to: http://localhost:8000")
    print("\nPress Ctrl+C to stop the server\n")

    uvicorn.run(
        "web.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
