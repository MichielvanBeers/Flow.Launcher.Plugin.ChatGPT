# -*- coding: utf-8 -*-

import os
import csv
import logging
from datetime import datetime
from flox import Flox  # noqa: E402
import webbrowser  # noqa: E402
import requests  # noqa: E402
import json  # noqa: E402
import pyperclip  # noqa: E402
from typing import Tuple, Optional

PROXIES = {
    "http": os.environ.get("HTTP_PROXY", ""),
    "https": os.environ.get("HTTPS_PROXY", ""),
}


class ChatGPT(Flox):
    def __init__(self):
        self.api_key = self.settings.get("api_key")
        self.model = self.settings.get("model")
        self.prompt_stop = self.settings.get("prompt_stop")
        self.default_system_prompt = self.settings.get("default_prompt")
        self.save_conversation_setting = self.settings.get("save_conversation")
        self.log_level = self.settings.get("log_level")
        self.api_endpoint = self.settings.get("api_endpoint")
        self.logger_level(self.log_level)

        try:
            self.csv_file = open("system_messages.csv", encoding="utf-8", mode="r")
            reader = csv.DictReader(self.csv_file, delimiter=";")
            self.prompts = list(reader)
            [logging.debug(f"Found prompt: {row}") for row in self.prompts]

        except FileNotFoundError:
            self.prompts = None
            logging.error("Unable to open system_messages.csv")

    def query(self, query: str) -> None:
        if not self.api_key:
            self.add_item(
                title="Unable to load the API key",
                subtitle=(
                    "Please make sure you've added a valid API key in the settings"
                ),
            )
            return
        if self.prompts is None:
            self.add_item(
                title="Unable to load the system prompts from CSV",
                subtitle="Please validate that the plugins folder contains a valid system_prompts.csv",  # noqa: E501
                method=self.open_plugin_folder,
            )
            return
        if query.endswith(self.prompt_stop):
            prompt, prompt_keyword, system_message = self.split_prompt(query)

            answer, prompt_timestamp, answer_timestamp = self.send_prompt(
                prompt, system_message
            )

            filename = None
            if self.save_conversation_setting:
                filename = self.save_conversation(
                    prompt_keyword, prompt, prompt_timestamp, answer, answer_timestamp
                )

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
                    parameters=[filename, answer],
                )


        else:
            self.add_item(
                title=f"Type your prompt and end with {self.prompt_stop}",
                subtitle=f"Current model: {self.model}",
            )
        return

    def send_prompt(
        self, prompt: str, system_message: str
    ) -> Tuple[str, datetime, datetime]:
        """
        Query the OpenAI end-point
        """
        url = self.api_endpoint

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

        prompt_timestamp = datetime.now()
        logging.debug(f"Sending request with data: {data}")
        try:
            response = requests.request(
                "POST", url, headers=headers, data=data, proxies=PROXIES
            )
        except UnicodeEncodeError as e:
            logging.error(f"UnicodeEncodeError: {e}")
            return "", prompt_timestamp, datetime.now()

        logging.debug(f"Response: {response}")
        answer_timestamp = datetime.now()

        result = ""
        response_json = response.json()
        if response.ok:
            for entry in response_json["choices"]:
                result += entry["message"]["content"]
        else:
            self.add_item(
                title="An error occurred", subtitle=response_json["error"]["message"]
            )
            logging.error(
                f"API returned {response.status_code} with message: {response_json}"
            )
        return result, prompt_timestamp, answer_timestamp

    def save_conversation(
        self,
        keyword: str,
        prompt: str,
        prompt_timestamp: datetime,
        answer: str,
        answer_timestamp: datetime,
    ) -> str:
        filename = f"Conversations '{keyword}' keyword.txt"
        formatted_prompt_timestamp = prompt_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        formatted_answer_timestamp = answer_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        new_content = f"[{formatted_prompt_timestamp}] User: {prompt}\n[{formatted_answer_timestamp}] ChatGPT: {answer}\n\n"  # noqa: E501

        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    existing_content = file.read()
            except PermissionError:
                logging.error(PermissionError)
        else:
            existing_content = ""

        new_content = new_content + existing_content

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(new_content)
        except PermissionError:
            logging.error(PermissionError)

        return filename

    def split_prompt(self, query: str) -> Tuple[str, str, str]:
        prompt = query.rstrip(self.prompt_stop).strip()
        prompt_array = prompt.split(" ")
        prompt_keyword = prompt_array[0].lower()

        system_message = ""

        for row in self.prompts:
            if row["Key Word"] == prompt_keyword:
                system_message = row["System Message"]
                prompt = prompt.split(" ", 1)[1]

        if not system_message:
            prompt_keyword = self.default_system_prompt

            for row in self.prompts:
                if row["Key Word"] == self.default_system_prompt:
                    system_message = row["System Message"]

        if len(prompt_array) == 1:
            prompt = prompt_array[0]

        logging.debug(
            f"""
        Prompt: {prompt}
        Prompt keyword: {prompt_keyword}
        System message: {system_message}
        """
        )

        return prompt, prompt_keyword, system_message

    def ellipsis(self, string: str, length: int):
        string = string.split("\n", 1)[0]
        return string[: length - 3] + "..." if len(string) > length else string

    def copy_answer(self, answer: str) -> None:
        """
        Copy answer to the clipboard.
        """
        pyperclip.copy(answer)

    def open_in_editor(self, filename: Optional[str], answer: Optional[str]) -> None:
        """
        Open the answer in the default text editor. If no filename is given,
        the conversation will be written to a new text file and opened.
        """
        if filename:
            webbrowser.open(filename)
            return

        if answer:
            temp_file = "temp_text.txt"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(answer)
            webbrowser.open(temp_file)
            return

    def display_answer(self, answer: str) -> None:
        """
        Display the answer directly.
        """
        self.add_item(
            title="Answer",
            subtitle=answer,
        )

    def open_plugin_folder(self) -> None:
        webbrowser.open(os.getcwd())

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.csv_file.close()


if __name__ == "__main__":
    ChatGPT()
