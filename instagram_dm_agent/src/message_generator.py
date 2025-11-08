# src/message_generator.py

import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models.llms import BaseLLM
from langchain_core.language_models.fake import FakeListLLM

from .config import (
    CREATOR_NAME,
    CREATOR_INSTAGRAM_HANDLE,
    CREATOR_NICHE,
)
from .profile_analyzer import analyze_profile

def create_message_generation_chain(llm: BaseLLM):
    """
    Creates a LangChain chain to generate a personalized Instagram DM.
    """
    prompt_template = """
    You are an expert copywriter for a content creator named {creator_name} who is in the "{creator_niche}" niche.
    Your task is to write a friendly, concise, and engaging Instagram DM to a potential collaborator.

    **Collaboration Context:**
    - **Your Creator:** {creator_name} (@{creator_handle})
    - **Collaboration Goal:** Propose a collaboration that is mutually beneficial.
    - **Key Information from Profile Analysis:**
      - **Personalization Hook:** {personalization_hook}
      - **Suggested Collaboration Angle:** {collaboration_angle}

    **Message Requirements:**
    1.  **Greeting:** Start with a friendly and personal greeting.
    2.  **Personal Reference:** Mention the "Personalization Hook" to show you've done your research.
    3.  **Collaboration Pitch:** Clearly and concisely propose the "Collaboration Angle."
    4.  **Call to Action:** End with a clear, low-pressure question to encourage a reply.
    5.  **Sign-off:** Keep it professional and friendly.
    6.  **Constraints:** The entire message must be under 1000 characters.

    **Example Output:**
    "Hi [Target Name], I came across your profile and was so impressed by your work! {personalization_hook}. As a fellow creator in the {creator_niche} space, I think a collaboration could be amazing. What are your thoughts on {collaboration_angle}? Let me know if you're interested! Best, {creator_name} @{creator_handle}"

    **Draft the message below:**
    """
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=[
            "personalization_hook",
            "collaboration_angle",
            "creator_name",
            "creator_handle",
            "creator_niche"
        ],
    )

    parser = StrOutputParser()
    chain = prompt | llm | parser
    return chain

def generate_message(profile_analysis: dict) -> str:
    """
    Generates a personalized outreach message based on profile analysis.

    Args:
        profile_analysis: A dictionary containing the analysis from the profile_analyzer.

    Returns:
        A personalized message string, or an error message if generation fails.
    """
    if not profile_analysis:
        return "Error: Profile analysis data is missing."

    # Use a fake LLM for deterministic output in this example.
    # In a real application, you would use a real LLM here.
    mock_response = f"Hi there! I absolutely loved your recent post on sustainable fashion. As a fellow creator in the {CREATOR_NICHE} niche, I think a joint reel on eco-friendly brands would be fantastic. What do you think? Best, {CREATOR_NAME} @{CREATOR_INSTAGRAM_HANDLE}"
    llm = FakeListLLM(responses=[mock_response])

    message_chain = create_message_generation_chain(llm)

    try:
        message = message_chain.invoke({
            "personalization_hook": profile_analysis.get("personalization_hook"),
            "collaboration_angle": profile_analysis.get("collaboration_angle"),
            "creator_name": CREATOR_NAME,
            "creator_handle": CREATOR_INSTAGRAM_HANDLE,
            "creator_niche": CREATOR_NICHE,
        })
        return message
    except Exception as e:
        print(f"ERROR: Failed to generate message. Reason: {e}")
        return f"Error: Could not generate message due to: {e}"

# --- Main Execution Block for Testing ---
if __name__ == '__main__':
    print("--- Running Message Generator Test ---")

    # First, get the profile analysis for a test user.
    target_username = "stylebygreen"
    analysis = analyze_profile(target_username)

    if analysis:
        print("\n--- Generating Message Based on Analysis ---")
        # Now, generate a message using that analysis.
        generated_message = generate_message(analysis)

        print("\n--- Generated DM ---")
        print(generated_message)
        print("-" * 20)
        print(f"Character count: {len(generated_message)}")
        print("--------------------")
    else:
        print("Could not perform analysis, so message generation is skipped.")

    print("------------------------------------")
