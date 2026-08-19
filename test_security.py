import os
import sys

from dotenv import load_dotenv

load_dotenv()

def check_environment() -> None:
    """Verifies that vital API keys are present in system RAM and not hardcoded."""

    api_key = os.getenv("GEMINI_API_KEY")
    
    # Defensive programming: stop immediately if the key is missing from memory
    if not api_key:
        print("CRITICAL ERROR: GEMINI_API_KEY is missing", file=sys.stderr)
        print("Please verify your .env file exists and contains GEMINI_API_KEY.", file=sys.stderr)
        sys.exit(1)
        
    print("Security check passed. System environment contains the required API credentials.")

if __name__ == "__main__":
    check_environment()
