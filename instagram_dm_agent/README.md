# AI-Powered Instagram DM Agent for Creator Collaborations

This project is an AI-powered agent designed to help content creators automate the outreach process for collaborations on Instagram. The agent identifies potential collaborators, analyzes their profiles for personalization, and generates tailored DM templates for outreach.

**Disclaimer:** This project is a foundational scaffold and not a fully functional, production-ready agent. The core integrations with the Instagram Graph API and a live language model are implemented with placeholders and mock data. This allows for safe testing of the agent's logic and workflow without requiring API keys. To make this agent fully operational, you will need to replace the mock functions with real API calls. This agent is designed to comply with Instagram's Terms of Service by generating messages for manual review and sending. It does **not** automate the sending of DMs, which can violate Instagram's policies and lead to account restrictions. Always use official APIs and prioritize ethical outreach practices.

## Features

- **Target Discovery:** (Future Scope) Identify potential collaborators based on niche, follower count, and other criteria.
- **Profile Analysis:** Analyzes a target's bio and recent posts to find personalization hooks.
- **Personalized Message Generation:** Uses a language model to craft unique and engaging outreach messages.
- **Manual Review Queue:** Generates a CSV file with message templates, allowing the creator to review, approve, and send them manually.
- **Safety First:** Includes rate limiting and emphasizes user consent and ethical compliance.

## How It Works

1.  **Configuration:** You provide your Instagram handle, target criteria, and collaboration details in a `.env` file.
2.  **Profile Analysis:** The agent fetches public information from a list of target profiles.
3.  **Message Crafting:** Using a powerful language model, the agent writes a personalized DM for each target.
4.  **Review and Send:** The generated messages are saved to a `outreach_plan.csv` file. You can then copy-paste these messages to send them from the Instagram app.

## Setup and Installation

### Prerequisites

- Python 3.8+
- An Instagram Business or Creator account.
- A Facebook Developer account and a configured Facebook App to access the Instagram Graph API.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/instagram-dm-agent.git
    cd instagram-dm-agent
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Configure your environment variables:**
    - Create a `.env` file by copying the example:
      ```bash
      cp .env.example .env
      ```
    - Open the `.env` file and add your credentials:
      - `INSTAGRAM_BUSINESS_ACCOUNT_ID`: Your Instagram Business Account ID.
      - `INSTAGRAM_ACCESS_TOKEN`: Your temporary or permanent access token for the Graph API.
      - `LLM_API_KEY`: Your API key for the language model (e.g., OpenAI).
      - Your creator-specific details for message personalization.

## Usage

To run the agent, execute the main script with a list of target Instagram handles:

```bash
python src/agent.py --targets "target_handle1,target_handle2,target_handle3"
```

The agent will process these profiles and generate an `outreach_plan.csv` file in the project's root directory.

## Ethical Considerations

- **No Spamming:** This tool is for personalized, high-quality outreach, not for spam. Keep your target list small and focused.
- **Compliance:** The agent is designed for manual sending to avoid breaking Instagram's automation rules.
- **Transparency:** Be clear and honest in your outreach messages.

---

*This project is for educational and experimental purposes. The user is responsible for ensuring compliance with all applicable platform policies and regulations.*
