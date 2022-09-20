import sys
import os
from rich import *
from rich.console import *
from rich.panel import *
from rich.markdown import *
from rich.prompt import *
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.padding import *
import shutil
import time
import tarfile
import pathlib

juice_console = Console()

VERSION = "0.0.1 (Alpha)"

MENU = """[bold]
1 New Passsword
2 Encrypt files
3 Decrypt files
4 Exit
"""

HELP_AND_CREDITS = """
"""

class Forms:
    
    @staticmethod
    def passowrd_form() -> dict:
        try:
            password_length = int(Prompt.ask("Enter password length {min=4}"))
            while password_length <= 4:
                password_length = int(Prompt.ask("[bold yellow]\tPassword length must be more than 4 :warning: "))

            alphabets_count = int(Prompt.ask("Enter alphabets count in password"))
            digits_count = int(Prompt.ask("Enter digits count in password"))
            special_characters_count = int(Prompt.ask("Enter special characters count in password"))
            
            characters_count = alphabets_count + digits_count + special_characters_count

            if characters_count > password_length:
                juice_console.print("[bold red]!Characters total count is greater than the password length :warning:")
                return None

            return {
                "password_length":password_length,
                "alphabets_count": alphabets_count,
                "digits_count": digits_count,
                "special_characters_count": special_characters_count
            }
        except ValueError:
            return None
    
    @staticmethod
    def encrypt_form() -> dict:
        ...

    @staticmethod
    def decrypt_form() -> dict:
        ...

class Display:
    
    @staticmethod
    def help_page() -> None:
        juice_console.rule("[bold green] Help", style="blue")
        juice_console.print(Panel.fit(HELP_AND_CREDITS, title="Help"))


def analyze_data(form):
    juice_console.print(Padding("[bold green] Your Data", (1, 1), expand=False))
    juice_console.print_json(data=form)
    return Confirm.ask("[bold yellow] Do you want continue? :warning:")