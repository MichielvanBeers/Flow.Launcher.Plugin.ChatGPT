# -*- coding: utf-8 -*-

import os
import csv
from flox import Flox  # noqa: E402
import webbrowser  # noqa: E402
import requests  # noqa: E402
import json  # noqa: E402
import pyperclip  # noqa: E402


class ChatGPT(Flox):
    def __init__(self):
        self.api_key = self.settings.get("api_key")
        self.model = self.settings.get("model")
        self.prompt_stop = self.settings.get("prompt_stop")
        self.default_system_prompt = self.settings.get("default_prompt")

        try:
            self.csv_file = open("system_messages.csv", encoding="utf-8", mode="r")
            self.prompts = csv.DictReader(self.csv_file, delimiter=";")
        except FileNotFoundError:
            self.prompts = None

    def send_prompt(self, prompt: str, system_message: str) -> str:
        """
        Query the OpenAI end-point
        """
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
        }

        body = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_message,
                },
                {"role": "user", "content": prompt},
            ],
        }

        data = json.dumps(body)

        response = requests.request("POST", url, headers=headers, data=data)

        result = ""
        response_json = response.json()
        if response.ok:
            for entry in response_json["choices"]:
                result += entry["message"]["content"]
        else:
            self.add_item(
                title="An error occurred", subtitle=response_json["error"]["message"]
            )
        return result


    def query(self, query: str) -> None:
        if not self.api_key:
            self.add_item(
                title="Unable to load the API key",
                subtitle="""
                Please make sure you've added 
                a valid API key in the settings.
                """,
            )
            return
        if self.prompts is None:
            self.add_item(
                title="Unable to load the system prompts from CSV",
                subtitle="""
                Please validate that the plugins folder
                contains a valid system_prompts.csv
                """,
                method=self.open_plugin_folder,
            )
            return
        if query.endswith(self.prompt_stop):
            prompt = query.rstrip(self.prompt_stop)
            prompt_key_word = prompt.split(" ")[0].lower()

            system_message = ""

            for row in self.prompts:
                if row["Key Word"] == prompt_key_word:
                    system_message = row["System Message"]
                    prompt = prompt.split(" ", 1)[1]

            if not system_message:
                for row in self.prompts:
                    if row["Key Word"] == self.default_system_prompt:
                        system_message = row["System Message"]

            answer = self.send_prompt(prompt, system_message)

            if answer:
                answer = answer.lstrip("\n").lstrip("\n")
                short_answer = self.ellipsis(answer, 30)

                self.add_item(
                    title="Copy to clipboard",
                    subtitle=f"Answer: {short_answer}",
                    method=self.copy_answer,
                    parameters=[answer],
                )
                self.add_item( 
                    title="Open in text editor",
                    subtitle=f"Answer: {short_answer}",
                    method=self.open_in_editor,
                    parameters=[answer],
                )
        else:
            self.add_item(
                title=f"Type your prompt and end with {self.prompt_stop}",
                subtitle=f"Current model: {self.model}",
            )
        return
    
    def ellipsis(self, string: str, length: int):
        string = string.split('\n', 1)[0]
        return string[:length-3] + '...' if len(string) > length else string

    def copy_answer(self, answer: str) -> None:
        """
        Copy answer to the clipboard.
        """
        pyperclip.copy(answer)

    def open_in_editor(self, answer: str) -> None:
        # Create a temporary file to store the content
        temp_file = "temp_text.txt"
        with open(temp_file, "w") as f:
            f.write(answer)

        # Open the default editor and paste the content
        webbrowser.open(temp_file)

    def open_plugin_folder(self) -> None:
        webbrowser.open(os.getcwd())

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.csv_file.close()


if __name__ == "__main__":
    ChatGPT()
