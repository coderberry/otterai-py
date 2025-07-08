import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from otterai.otterai import OtterAI, OtterAIException

load_dotenv()


class OtterAIRunner:
    """Interactive runner for OtterAI methods with rich output and file saving."""

    def __init__(self):
        self.otter = OtterAI()
        self.authenticated = False
        self.test_speech_otid = os.getenv("TEST_OTTERAI_SPEECH_OTID")

        # Available methods with their descriptions and parameter requirements
        self.methods = {
            "1": {
                "name": "get_user",
                "desc": "Get current user information",
                "params": [],
            },
            "2": {"name": "get_speakers", "desc": "Get all speakers", "params": []},
            "3": {
                "name": "get_speeches",
                "desc": "Get speeches list",
                "params": ["folder", "page_size", "source"],
            },
            "4": {
                "name": "get_speech",
                "desc": "Get specific speech by OTID",
                "params": ["otid"],
            },
            "5": {
                "name": "query_speech",
                "desc": "Query speech content",
                "params": ["query", "otid", "size"],
            },
            "6": {
                "name": "get_notification_settings",
                "desc": "Get notification settings",
                "params": [],
            },
            "7": {"name": "list_groups", "desc": "List all groups", "params": []},
            "8": {"name": "get_folders", "desc": "Get all folders", "params": []},
            "9": {
                "name": "set_speech_title",
                "desc": "Set speech title",
                "params": ["otid", "title"],
            },
            "10": {
                "name": "create_speaker",
                "desc": "Create new speaker",
                "params": ["speaker_name"],
            },
            "11": {
                "name": "move_to_trash_bin",
                "desc": "Move speech to trash",
                "params": ["otid"],
            },
            "12": {
                "name": "download_speech",
                "desc": "Download speech",
                "params": ["otid", "name", "fileformat"],
            },
            "13": {
                "name": "get_contacts_structured",
                "desc": "Get contacts (structured)",
                "params": [],
            },
            "14": {
                "name": "get_folders_structured",
                "desc": "Get folders (structured)",
                "params": [],
            },
            "15": {
                "name": "get_speech_mention_candidates_structured",
                "desc": "Get mention candidates (structured)",
                "params": ["otid"],
            },
        }

    def login(self) -> bool:
        """Authenticate with OtterAI."""
        username = os.getenv("OTTERAI_USERNAME")
        password = os.getenv("OTTERAI_PASSWORD")

        if not username or not password:
            print("❌ OTTERAI_USERNAME and OTTERAI_PASSWORD must be set in .env")
            return False

        try:
            print(f"🔐 Authenticating as {username}...")
            response = self.otter.login(username, password)
            if response["status"] == 200:
                print("✅ Login successful!")
                self.authenticated = True
                return True
            else:
                print(f"❌ Login failed: {response}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def display_menu(self):
        """Display the interactive menu."""
        print("\n" + "=" * 60)
        print("🦦 OtterAI Interactive Method Runner")
        print("=" * 60)
        print("\nAvailable Methods:")

        for key, method in self.methods.items():
            params_str = (
                f" (requires: {', '.join(method['params'])})"
                if method["params"]
                else ""
            )
            print(f"  {key:>2}. {method['name']:<35} - {method['desc']}{params_str}")

        print("\n  0. Exit")
        print("\n" + "-" * 60)

    def get_user_input(self, prompt: str, required: bool = True) -> Optional[str]:
        """Get user input with validation."""
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value if value else None
            print("❌ This field is required. Please enter a value.")

    def get_method_parameters(self, method_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get parameters for a method from user input."""
        params = {}

        for param in method_info["params"]:
            if param == "otid":
                default_otid = self.test_speech_otid
                if default_otid:
                    value = self.get_user_input(
                        f"Enter {param} (default: {default_otid}): ", required=False
                    )
                    params[param] = value or default_otid
                else:
                    params[param] = self.get_user_input(f"Enter {param}: ")
            elif param == "folder":
                value = self.get_user_input(
                    f"Enter {param} (default: 0): ", required=False
                )
                params[param] = int(value) if value else 0
            elif param == "page_size":
                value = self.get_user_input(
                    f"Enter {param} (default: 45): ", required=False
                )
                params[param] = int(value) if value else 45
            elif param == "size":
                value = self.get_user_input(
                    f"Enter {param} (default: 500): ", required=False
                )
                params[param] = int(value) if value else 500
            elif param == "source":
                value = self.get_user_input(
                    f"Enter {param} (default: owned): ", required=False
                )
                params[param] = value or "owned"
            elif param == "fileformat":
                value = self.get_user_input(
                    f"Enter {param} (default: txt,pdf,mp3,docx,srt): ", required=False
                )
                params[param] = value or "txt,pdf,mp3,docx,srt"
            else:
                params[param] = self.get_user_input(f"Enter {param}: ")

        return params

    def format_output(self, result: Any, method_name: str) -> str:
        """Format the output for display."""
        formatted = f"\n🔍 Method: {method_name}\n"
        formatted += f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        formatted += "\n" + "=" * 60 + "\n"

        if isinstance(result, dict):
            formatted += json.dumps(result, indent=2, ensure_ascii=False)
        else:
            formatted += str(result)

        formatted += "\n" + "=" * 60 + "\n"
        return formatted

    def save_to_file(self, content: str, method_name: str) -> Optional[str]:
        """Save content to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"otterai_{method_name}_{timestamp}.txt"

        save_choice = self.get_user_input(
            f"💾 Save to file? (y/N, default filename: {filename}): ", required=False
        )
        if save_choice and save_choice.lower().startswith("y"):
            custom_filename = self.get_user_input(
                f"Enter filename (default: {filename}): ", required=False
            )
            final_filename = custom_filename or filename

            try:
                with open(final_filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Saved to {final_filename}")
                return final_filename
            except Exception as e:
                print(f"❌ Error saving file: {e}")

        return None

    def execute_method(self, method_name: str, params: Dict[str, Any]) -> Any:
        """Execute a method with given parameters."""
        method = getattr(self.otter, method_name)

        if params:
            return method(**params)
        else:
            return method()

    def run(self):
        """Main interactive loop."""
        print("🦦 Welcome to OtterAI Interactive Runner!")

        if not self.login():
            return

        while True:
            self.display_menu()

            choice = self.get_user_input("\nSelect a method (0 to exit): ")

            if choice == "0":
                print("👋 Goodbye!")
                break

            if choice not in self.methods:
                print("❌ Invalid choice. Please try again.")
                continue

            method_info = self.methods[choice]
            method_name = method_info["name"]

            print(f"\n🚀 Executing: {method_name}")
            print(f"📝 Description: {method_info['desc']}")

            try:
                # Get parameters if needed
                params = self.get_method_parameters(method_info)

                print(f"\n⏳ Calling {method_name}...")
                result = self.execute_method(method_name, params)

                # Format and display output
                formatted_output = self.format_output(result, method_name)
                print(formatted_output)

                # Offer to save to file
                self.save_to_file(formatted_output, method_name)

            except OtterAIException as e:
                print(f"❌ OtterAI Error: {e}")
            except Exception as e:
                print(f"❌ Unexpected error: {e}")

            input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    runner = OtterAIRunner()
    runner.run()


if __name__ == "__main__":
    main()
