# src/profile_analyzer.py

import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.language_models.llms import BaseLLM
from langchain_core.language_models.fake import FakeListLLM


from .config import LLM_API_KEY, CREATOR_NICHE

# --- Placeholder for Instagram API Call ---
# In a real application, this function would use the Instagram Graph API to fetch profile data.
# For this example, we'll return mock data to simulate the API response.
def get_instagram_profile_data(username: str) -> dict:
    """
    Fetches public data for a given Instagram username.

    Args:
        username: The Instagram handle of the target user.

    Returns:
        A dictionary containing the user's bio, recent posts, and other public info.
        Returns a mock response if the API call fails or for testing purposes.
    """
    print(f"INFO: Fetching mock data for Instagram profile: {username}")
    # This mock data simulates what you might get from the Graph API.
    mock_data = {
        "username": username,
        "bio": f"🌿 Sustainable Fashion Advocate | 📍 London | Spreading positivity through style. ✨ Let's collaborate to make the world greener!",
        "recent_posts": [
            {"caption": "Just dropped a new blog post on the top 5 eco-friendly fabrics! #SustainableFashion #EcoFriendly", "likes": 1200},
            {"caption": "Loved visiting the thrift stores in Brick Lane today! So many hidden gems. #VintageFinds #LondonFashion", "likes": 2500},
            {"caption": "Partnering with @GreenStyle to plant a tree for every share of this post! 🌳 #GoGreen", "likes": 5000}
        ],
        "follower_count": 45000
    }
    return mock_data

# --- LangChain Profile Analysis ---

def create_profile_analysis_chain(llm: BaseLLM):
    """
    Creates a LangChain chain that analyzes an Instagram profile and extracts personalization points.
    """
    prompt_template = """
    You are an expert AI assistant for a content creator in the "{creator_niche}" niche.
    Your task is to analyze the following Instagram profile data and extract key information for a personalized collaboration outreach message.

    **Instagram Profile Data:**
    ```json
    {profile_data}
    ```

    **Analysis Task:**
    Based on the data provided, identify the following:
    1.  **Niche/Interests:** What are the main topics or interests of this creator?
    2.  **Personalization Hook:** What is a specific, recent post or bio detail you can compliment? Be genuine.
    3.  **Collaboration Angle:** Suggest a relevant collaboration idea that aligns with both your niche ("{creator_niche}") and their content.

    **Output Format:**
    Provide your analysis in a clean JSON format. Example:
    {{
      "niche_interests": ["Sustainable Fashion", "Thrifting", "Eco-conscious living"],
      "personalization_hook": "I loved your recent post about discovering hidden gems in Brick Lane's thrift stores. It's inspiring to see how you champion sustainable style.",
      "collaboration_angle": "Since we're both passionate about sustainable practices, a joint reel showcasing our favorite eco-friendly brands could be amazing."
    }}
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["profile_data", "creator_niche"],
    )

    parser = JsonOutputParser()
    chain = prompt | llm | parser
    return chain

def analyze_profile(username: str) -> dict:
    """
    Analyzes a single Instagram profile to extract personalization points.

    Args:
        username: The Instagram handle of the target user.

    Returns:
        A dictionary containing the analysis, or None if an error occurs.
    """
    profile_data = get_instagram_profile_data(username)
    if not profile_data:
        return None

    # In a real app, you would initialize your LLM here, e.g., with OpenAI(api_key=LLM_API_KEY)
    # For this example, we use a fake LLM for deterministic output.
    mock_llm_response = {
      "niche_interests": ["Sustainable Fashion", "Thrifting", "Eco-conscious living"],
      "personalization_hook": "I loved your recent post about discovering hidden gems in Brick Lane's thrift stores. It's inspiring to see how you champion sustainable style.",
      "collaboration_angle": "Since we're both passionate about sustainable practices, a joint reel showcasing our favorite eco-friendly brands could be amazing."
    }

    # We serialize the JSON object to a string for the FakeListLLM
    responses = [json.dumps(mock_llm_response)]
    llm = FakeListLLM(responses=responses)

    analysis_chain = create_profile_analysis_chain(llm)

    try:
        analysis_result = analysis_chain.invoke({
            "profile_data": json.dumps(profile_data, indent=2),
            "creator_niche": CREATOR_NICHE
        })
        return analysis_result
    except Exception as e:
        print(f"ERROR: Failed to analyze profile {username}. Reason: {e}")
        return None

# --- Main Execution Block for Testing ---
if __name__ == '__main__':
    print("--- Running Profile Analyzer Test ---")
    target_username = "stylebygreen"
    analysis = analyze_profile(target_username)

    if analysis:
        print("\n--- Analysis Result ---")
        print(f"Niche/Interests: {analysis.get('niche_interests')}")
        print(f"Personalization Hook: {analysis.get('personalization_hook')}")
        print(f"Collaboration Angle: {analysis.get('collaboration_angle')}")
        print("-----------------------")
    else:
        print("Analysis failed.")
    print("---------------------------------")
