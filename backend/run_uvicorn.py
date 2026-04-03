"""
Simple launcher to start the FastAPI app via uvicorn.
This script is called from the batch launcher after environment is set up.
"""
from uvicorn import run

if __name__ == "__main__":
    # Run uvicorn - environment variables should be loaded by caller
    run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )

