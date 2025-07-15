import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()  # Load variables from .env

# Retrieve the API key
api_key = os.getenv("ELEVENLABS_API_KEY")

# Safety check
if not api_key:
    raise RuntimeError("❌ ELEVENLABS_API_KEY not found! Check your .env file and its location.")

# Initialize the client only if key is present
client = ElevenLabs(api_key=api_key)
print("✅ ElevenLabs client initialized successfully.")
