#!/usr/bin/env python3
"""
Interactive OtterAI API Runner

This script provides an interactive interface to explore and test OtterAI API endpoints.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax
from rich.table import Table

from otterai import OtterAI

# Load environment variables
load_dotenv()

console = Console()


class InteractiveRunner:
    def __init__(self):
        self.client = OtterAI()
        self.output_dir = Path("./output")
        self.available_apis = {
            "abstract_summary": {
                "name": "abstract_summary",
                "description": "Get abstract summary (placeholder - not implemented in API)",
                "requires_auth": True,
                "requires_otid": True,
                "method": lambda otid: {
                    "status": 200,
                    "data": {
                        "message": "Abstract summary placeholder - not implemented in current API"
                    },
                },
            },
            "applied_speech_template": {
                "name": "applied_speech_template",
                "description": "Get applied speech template (placeholder - not implemented in API)",
                "requires_auth": True,
                "requires_otid": True,
                "method": lambda otid: {
                    "status": 200,
                    "data": {
                        "message": "Applied speech template placeholder - not implemented in current API"
                    },
                },
            },
            "get_user": {
                "name": "get_user",
                "description": "Get current user information",
                "requires_auth": False,
                "requires_otid": False,
                "method": self.client.get_user,
            },
            "get_speakers": {
                "name": "get_speakers",
                "description": "Get all speakers",
                "requires_auth": True,
                "requires_otid": False,
                "method": self.client.get_speakers,
            },
            "get_speeches": {
                "name": "available_speeches",
                "description": "Get all speeches (available_speeches)",
                "requires_auth": True,
                "requires_otid": False,
                "method": self.client.get_speeches,
            },
            "get_speech": {
                "name": "get_speech",
                "description": "Get specific speech details",
                "requires_auth": True,
                "requires_otid": True,
                "method": self.client.get_speech,
            },
            "query_speech": {
                "name": "query_speech",
                "description": "Query/search within a speech",
                "requires_auth": True,
                "requires_otid": True,
                "method": self.client.query_speech,
            },
            "get_notification_settings": {
                "name": "get_notification_settings",
                "description": "Get notification settings",
                "requires_auth": False,
                "requires_otid": False,
                "method": self.client.get_notification_settings,
            },
            "list_groups": {
                "name": "list_groups",
                "description": "List user groups",
                "requires_auth": True,
                "requires_otid": False,
                "method": self.client.list_groups,
            },
            "get_folders": {
                "name": "get_folders",
                "description": "Get user folders",
                "requires_auth": True,
                "requires_otid": False,
                "method": self.client.get_folders,
            },
            "get_contacts_structured": {
                "name": "get_contacts_structured",
                "description": "Get contacts with structured response",
                "requires_auth": True,
                "requires_otid": False,
                "method": self.client.get_contacts_structured,
            },
            "get_folders_structured": {
                "name": "get_folders_structured",
                "description": "Get folders with structured response",
                "requires_auth": True,
                "requires_otid": False,
                "method": self.client.get_folders_structured,
            },
            "get_speech_mention_candidates_structured": {
                "name": "get_speech_mention_candidates_structured",
                "description": "Get speech mention candidates with structured response",
                "requires_auth": True,
                "requires_otid": True,
                "method": self.client.get_speech_mention_candidates_structured,
            },
            "list_groups_structured": {
                "name": "list_groups_structured",
                "description": "Get groups with structured response (TEMP.md endpoint)",
                "requires_auth": True,
                "requires_otid": False,
                "method": self.client.list_groups_structured,
            },
            "get_speakers_structured": {
                "name": "get_speakers_structured",
                "description": "Get speakers with structured response",
                "requires_auth": True,
                "requires_otid": False,
                "method": self.client.get_speakers_structured,
            },
            "create_speaker": {
                "name": "create_speaker",
                "description": "Create a new speaker",
                "requires_auth": True,
                "requires_otid": False,
                "method": lambda: self.client.create_speaker("Test Speaker"),
            },
            "set_speech_title": {
                "name": "set_speech_title",
                "description": "Set speech title",
                "requires_auth": True,
                "requires_otid": True,
                "method": lambda otid: self.client.set_speech_title(
                    otid, "Updated Title"
                ),
            },
            "move_to_trash_bin": {
                "name": "move_to_trash_bin",
                "description": "Move speech to trash",
                "requires_auth": True,
                "requires_otid": True,
                "method": self.client.move_to_trash_bin,
            },
            "download_speech": {
                "name": "download_speech",
                "description": "Download speech in various formats",
                "requires_auth": True,
                "requires_otid": True,
                "method": self.client.download_speech,
            },
        }

    def login(self) -> bool:
        """Login to OtterAI"""
        username = os.getenv("OTTERAI_USERNAME")
        password = os.getenv("OTTERAI_PASSWORD")

        if not username or not password:
            console.print("[red]❌ Missing credentials in .env file[/red]")
            return False

        console.print("[blue]🔐 Logging in to OtterAI...[/blue]")
        try:
            result = self.client.login(username, password)
            if result["status"] == 200:
                console.print("[green]✅ Login successful![/green]")
                return True
            else:
                console.print(f"[red]❌ Login failed: {result}[/red]")
                return False
        except Exception as e:
            console.print(f"[red]❌ Login error: {e}[/red]")
            return False

    def display_api_menu(self) -> List[str]:
        """Display available APIs and get user selection"""
        console.print(Panel.fit("🦦 OtterAI API Explorer", style="bold blue"))
        console.print("\n[bold]Which API would you like to access?[/bold]")

        # Create a table for better display
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan", width=8)
        table.add_column("API Name", style="green")
        table.add_column("Description", style="yellow")

        api_options = list(self.available_apis.keys())
        for i, api_key in enumerate(api_options):
            api_info = self.available_apis[api_key]
            table.add_row(f"[{i+1}]", api_info["name"], api_info["description"])

        console.print(table)

        # Get user selection
        selected_apis = []
        while True:
            choice = Prompt.ask(
                "\n[bold]Enter API numbers (comma-separated) or 'done' to continue[/bold]",
                default="done",
            )

            if choice.lower() == "done":
                break

            try:
                numbers = [int(x.strip()) for x in choice.split(",")]
                for num in numbers:
                    if 1 <= num <= len(api_options):
                        api_key = api_options[num - 1]
                        if api_key not in selected_apis:
                            selected_apis.append(api_key)
                            console.print(
                                f"[green]✅ Added: {self.available_apis[api_key]['name']}[/green]"
                            )
                        else:
                            console.print(
                                f"[yellow]⚠️ Already selected: {self.available_apis[api_key]['name']}[/yellow]"
                            )
                    else:
                        console.print(f"[red]❌ Invalid option: {num}[/red]")
            except ValueError:
                console.print(
                    "[red]❌ Please enter valid numbers separated by commas[/red]"
                )

        return selected_apis

    def ask_save_preference(self) -> bool:
        """Ask user if they want to save responses"""
        return Confirm.ask(
            "\n[bold]Would you like to save the responses to './output'?[/bold]"
        )

    def get_test_otid(self) -> Optional[str]:
        """Get test OTID from environment or user input"""
        otid = os.getenv("TEST_OTTERAI_SPEECH_OTID")
        if otid:
            return otid

        otid = Prompt.ask(
            "\n[bold]Enter a speech OTID for testing (or press Enter to skip APIs requiring OTID)[/bold]",
            default="",
        )
        return otid if otid else None

    def execute_api_call(self, api_key: str, otid: Optional[str] = None) -> Dict:
        """Execute a single API call"""
        api_info = self.available_apis[api_key]

        # Check if API requires OTID and we don't have one
        if api_info["requires_otid"] and not otid:
            return {
                "status": "skipped",
                "reason": "No OTID provided for API that requires it",
            }

        try:
            console.print(f"[blue]🔄 Calling {api_info['name']}...[/blue]")

            # Call the API method
            if api_info["requires_otid"]:
                if api_key == "query_speech":
                    # query_speech requires additional parameters
                    result = api_info["method"]("test query", otid)
                else:
                    result = api_info["method"](otid)
            else:
                result = api_info["method"]()

            return {"status": "success", "data": result, "endpoint": api_info["name"]}

        except Exception as e:
            return {"status": "error", "error": str(e), "endpoint": api_info["name"]}

    def display_response(self, response: Dict, api_name: str):
        """Display API response with rich formatting"""
        console.print(f"\n[bold magenta]📡 API Response for {api_name}:[/bold magenta]")

        if response["status"] == "success":
            # Display the JSON response
            json_str = json.dumps(response["data"], indent=2)
            syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
            console.print(
                Panel(syntax, title=f"✅ {api_name} Response", border_style="green")
            )
        elif response["status"] == "error":
            console.print(Panel(f"❌ Error: {response['error']}", border_style="red"))
        elif response["status"] == "skipped":
            console.print(
                Panel(f"⏭️ Skipped: {response['reason']}", border_style="yellow")
            )

    def save_response(self, response: Dict, api_name: str):
        """Save API response to file"""
        if response["status"] != "success":
            return

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(exist_ok=True)

        # Save to JSON file
        filename = self.output_dir / f"{api_name}.json"
        with open(filename, "w") as f:
            json.dump(response["data"], f, indent=2)

        console.print(f"[green]💾 Saved response to {filename}[/green]")

    def run(self):
        """Main runner method"""
        console.print(Panel.fit("🦦 OtterAI Interactive API Runner", style="bold blue"))

        # Check if we need to login
        needs_auth = False
        selected_apis = self.display_api_menu()

        if not selected_apis:
            console.print("[yellow]ℹ️ No APIs selected. Exiting.[/yellow]")
            return

        # Check if any selected API requires authentication
        for api_key in selected_apis:
            if self.available_apis[api_key]["requires_auth"]:
                needs_auth = True
                break

        # Login if needed
        if needs_auth and not self.login():
            console.print(
                "[red]❌ Cannot proceed without login for authenticated APIs[/red]"
            )
            return

        # Ask about saving responses
        save_responses = self.ask_save_preference()

        # Get OTID if needed
        otid = None
        needs_otid = any(
            self.available_apis[api_key]["requires_otid"] for api_key in selected_apis
        )
        if needs_otid:
            otid = self.get_test_otid()

        console.print("\n[bold green]🚀 Starting API calls...[/bold green]")

        # Execute API calls with delays
        for i, api_key in enumerate(selected_apis):
            if i > 0:
                console.print(
                    "[blue]⏱️ Waiting 2 seconds to avoid rate limits...[/blue]"
                )
                time.sleep(2)

            response = self.execute_api_call(api_key, otid)
            api_name = self.available_apis[api_key]["name"]

            self.display_response(response, api_name)

            if save_responses:
                self.save_response(response, api_name)

        console.print("\n[bold green]✅ All API calls completed![/bold green]")


if __name__ == "__main__":
    runner = InteractiveRunner()
    runner.run()
