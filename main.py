import os
import sys
from dotenv import load_dotenv

from agents.planner import generate_plan
from agents.executor import execute_plan
from agents.verifier import verify_results

# Load environment variables
load_dotenv()

def check_env():
    required_keys = ["OPENAI_API_KEY", "OPENWEATHER_API_KEY", "GITHUB_TOKEN"]
    missing = [key for key in required_keys if not os.getenv(key)]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        print("Please check your .env file.")
        sys.exit(1)

def main():
    print("AI Operations Assistant Initialized")
    check_env()
    
    while True:
        try:
            user_input = input("\nRequest (or 'exit' to quit): ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
                
            print("\n--- Phase 1: Planning ---")
            plan = generate_plan(user_input)
            if "error" in plan:
                print(f"Planning failed: {plan['error']}")
                continue
            print("Plan generated successfully.")
            
            print("\n--- Phase 2: Execution ---")
            results = execute_plan(plan)
            print("Execution completed.")
            
            print("\n--- Phase 3: Verification ---")
            final_response = verify_results(user_input, results)
            
            print("\n=== Final Response ===")
            print(final_response)
            print("======================")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
