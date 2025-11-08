# src/agent.py

import argparse
import pandas as pd
import time
from datetime import datetime

from .profile_analyzer import analyze_profile
from .message_generator import generate_message
from .config import MAX_MESSAGES_PER_HOUR

class InstagramDMAgent:
    """
    An AI agent that analyzes Instagram profiles and generates personalized outreach DMs
    for content creators to send manually.
    """

    def __init__(self, target_handles: list):
        self.target_handles = target_handles
        self.outreach_plan = []
        # Calculate the delay needed to stay within the rate limit.
        self.request_delay_seconds = 3600 / MAX_MESSAGES_PER_HOUR

    def process_target(self, handle: str):
        """
        Processes a single target profile: analyzes it and generates a message.
        """
        print(f"\n--- Processing Target: {handle} ---")

        # 1. Analyze the profile
        print("Step 1: Analyzing profile...")
        analysis = analyze_profile(handle)

        if not analysis:
            print("Failed to analyze profile. Skipping.")
            return None

        # 2. Generate the message
        print("Step 2: Generating personalized message...")
        message = generate_message(analysis)

        if "Error:" in message:
            print("Failed to generate message. Skipping.")
            return None

        print("Successfully generated message.")

        # 3. Store the result
        result = {
            "target_handle": handle,
            "generated_message": message,
            "status": "Pending Review",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return result

    def run(self):
        """
        Executes the agent's workflow for all target handles.
        """
        print("--- Instagram DM Agent Initialized ---")
        print(f"Targets: {self.target_handles}")
        print(f"Rate Limit: {MAX_MESSAGES_PER_HOUR} messages/hour (delay: {self.request_delay_seconds:.2f}s)")

        for handle in self.target_handles:
            result = self.process_target(handle)
            if result:
                self.outreach_plan.append(result)

            # Apply rate limiting
            print(f"Waiting for {self.request_delay_seconds:.2f} seconds before next target...")
            time.sleep(self.request_delay_seconds)

        print("\n--- Agent Run Complete ---")
        return self.outreach_plan

    def save_outreach_plan_to_csv(self, filename: str = "outreach_plan.csv"):
        """
        Saves the generated outreach plan to a CSV file for manual review.
        """
        if not self.outreach_plan:
            print("No outreach plan was generated. Nothing to save.")
            return

        df = pd.DataFrame(self.outreach_plan)

        try:
            df.to_csv(filename, index=False)
            print(f"Outreach plan successfully saved to '{filename}'.")
            print("Please review the messages before sending them manually.")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

def main():
    """
    Main function to run the agent from the command line.
    """
    parser = argparse.ArgumentParser(description="AI Agent for Instagram DM Outreach")
    parser.add_argument(
        "-t", "--targets",
        required=True,
        type=str,
        help="A comma-separated list of Instagram handles to target (e.g., 'user1,user2,user3')."
    )
    args = parser.parse_args()

    # Split the comma-separated string of handles into a list
    target_handles = [handle.strip() for handle in args.targets.split(',')]

    # Initialize and run the agent
    agent = InstagramDMAgent(target_handles=target_handles)
    agent.run()
    agent.save_outreach_plan_to_csv()

if __name__ == "__main__":
    main()
