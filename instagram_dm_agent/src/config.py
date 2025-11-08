# src/config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Instagram API Credentials ---
# These are essential for connecting to the Instagram Graph API.
# Ensure you have a Meta Developer App and an Instagram Business/Creator account.
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

# --- Language Model API Key ---
# The API key for your chosen language model provider (e.g., OpenAI, Anthropic, etc.).
LLM_API_KEY = os.getenv("LLM_API_KEY")

# --- Creator's Information ---
# These details are used to personalize the outreach messages.
# They are loaded from the .env file to make the agent easily configurable for different users.
CREATOR_INSTAGRAM_HANDLE = os.getenv("CREATOR_INSTAGRAM_HANDLE", "YourInstagramHandle")
CREATOR_NAME = os.getenv("CREATOR_NAME", "Your Name")
CREATOR_NICHE = os.getenv("CREATOR_NICHE", "your niche")
CREATOR_BIO = os.getenv("CREATOR_BIO", "A passionate content creator.")

# --- Agent Configuration ---
# You can add other configurations here, such as rate limits or logging levels.
MAX_MESSAGES_PER_HOUR = 60  # Safety feature to prevent spamming
FOLLOW_UP_DAYS = 5  # Days to wait before suggesting a follow-up

# --- Validation ---
# A simple check to ensure that critical environment variables are set.
if not all([INSTAGRAM_BUSINESS_ACCOUNT_ID, INSTAGRAM_ACCESS_TOKEN, LLM_API_KEY]):
    print("CRITICAL ERROR: One or more required environment variables are not set.")
    print("Please create a .env file and fill in your API keys and account ID.")
    # In a real application, you might raise an exception here.
    # For this example, we'll print a message and continue, but dependent functionality will fail.

if __name__ == '__main__':
    # This block allows you to run this file directly to test if variables are loaded correctly.
    print("--- Configuration Loaded ---")
    print(f"Instagram Business Account ID: {'Loaded' if INSTAGRAM_BUSINESS_ACCOUNT_ID else 'Not Found'}")
    print(f"Instagram Access Token: {'Loaded' if INSTAGRAM_ACCESS_TOKEN else 'Not Found'}")
    print(f"LLM API Key: {'Loaded' if LLM_API_KEY else 'Not Found'}")
    print("-" * 20)
    print(f"Creator Handle: {CREATOR_INSTAGRAM_HANDLE}")
    print(f"Creator Name: {CREATOR_NAME}")
    print(f"Creator Niche: {CREATOR_NICHE}")
    print(f"Creator Bio: {CREATOR_BIO}")
    print("-" * 20)
    print(f"Max messages per hour: {MAX_MESSAGES_PER_HOUR}")
    print(f"Follow-up days: {FOLLOW_UP_DAYS}")
    print("----------------------------")
