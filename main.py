import json
import os

import typer
from dotenv import load_dotenv
from revChatGPT.V1 import Chatbot
from rich.console import Console
from rich.markdown import Markdown

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

load_dotenv()

app = typer.Typer(rich_markup_mode="markdown")
console = Console()


chatbot = Chatbot(
    config={
        "access_token": os.getenv("ACCESS_TOKEN"),
    }
)


def read_conversation(name: str) -> list:
    path = f"{CURR_DIR}/chat"
    dir = f"{path}/{name}.json"
    if os.path.exists(dir):
        with open(dir, "r") as f:
            conversation = json.load(f)
            return conversation
    return []


def save_conversation(name: str, conversation: list):
    path = f"{CURR_DIR}/chat"
    with open(f"{path}/{name}.json", "w") as f:
        f.write(json.dumps(conversation))


@app.command()
def chat(
    message: str = typer.Argument(..., help="Question for chatGPT"),
    name: str = typer.Argument(..., help="Name to load a conversation"),
):
    conversation: list = read_conversation(name)
    response = ""
    for data in chatbot.ask(message):
        response = data["message"]

    md = Markdown(f"**User**: {message}")
    console.print(md)
    md = Markdown(f"**Chat**: {response}")
    console.print(md)

    current = {}
    current["user"] = message
    current["chat"] = response
    conversation.append(current)
    save_conversation(name, conversation)


if __name__ == "__main__":
    app()
