import sys
import os
from rich import *
from rich.console import *
from rich.panel import *
from rich.markdown import *
from rich.prompt import *
from rich.padding import *
import pathlib
from cryptography.fernet import Fernet
from . import static


class CryptUtils:

    @staticmethod
    def new_key() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def save_key(key: bytes, file_key: str) -> None:
        with open(file_key, 'wb') as filekey:
            filekey.write(key)


juice_console = Console()


class BaseForms:

    def _verify_path(path, dir_mode: bool = False) -> bool:
        def existence_verification(x): return pathlib.Path(x).exists()
        if dir_mode:
            def type_verification(x): return pathlib.Path(x).is_dir()
        else:
            def type_verification(x): return pathlib.Path(x).is_file()
        
        return not existence_verification(path) or not type_verification(path)

    @staticmethod
    def _encrypt_form(path_text: str, bad_path_text: str, dir_mode: bool = False, default_key_mode: str = "new") -> tuple:
        return_path = Prompt.ask(path_text)

        while (BaseForms._verify_path(return_path, dir_mode)):
            return_path = Prompt.ask(f"[bold yellow]\t{bad_path_text} :warning: ")

        key_mode = Prompt.ask("Enter a key option",
                              choices=["new", "text", "file"],
                              default=default_key_mode)

        if key_mode == "new":
            key = CryptUtils.new_key()

        elif key_mode == "text":
            text_key = Prompt.ask("Enter the key")
            key = text_key.encode()

        else:
            file_key = Prompt.ask("Enter the key file path")
            while (BaseForms._verify_path(file_key)):
                file_key = Prompt.ask(
                    "[bold yellow]\tPlease enter a valid key file path :warning: ")

            with open(file_key, 'rb') as filekey:
                key = filekey.read()

        return (key, return_path)

    @staticmethod
    def _decrypt_form(path_text: str, bad_path_text: str, dir_mode: bool = False) -> tuple:
        return_path = Prompt.ask(path_text)
        
        while (BaseForms._verify_path(return_path, dir_mode)):
            return_path = Prompt.ask(f"[bold yellow]\t{bad_path_text} :warning: ")

        key_mode = Prompt.ask("Enter a key option",
                                choices=["1", "2", "text", "file"],
                                default="text")

        if key_mode in {"1", "text"}:
            text_key = Prompt.ask("Enter the key")
            key = text_key.encode()

        else:
            file_key = Prompt.ask("Enter the key file path")
            
            while (BaseForms._verify_path(file_key)):
                file_key = Prompt.ask(
                    "[bold yellow]\tPlease enter a valid key file path :warning: ")

            with open(file_key, 'rb') as filekey:
                key = filekey.read()

        return (key, return_path)


class Forms(BaseForms):

    @staticmethod
    def passowrd_form() -> dict:
        try:
            password_length = int(Prompt.ask("Enter password length {min=4}"))
            while password_length <= 4:
                password_length = int(Prompt.ask(
                    "[bold yellow]\tPassword length must be more than 4 :warning: "))

            alphabets_count = int(Prompt.ask(
                "Enter alphabets count in password"))
            digits_count = int(Prompt.ask("Enter digits count in password"))
            special_characters_count = int(Prompt.ask(
                "Enter special characters count in password"))

            characters_count = alphabets_count + digits_count + special_characters_count

            if characters_count > password_length:
                juice_console.print(
                    "[bold red]!Characters total count is greater than the password length :warning:")
                return None

            return {
                "password_length": password_length,
                "alphabets_count": alphabets_count,
                "digits_count": digits_count,
                "special_characters_count": special_characters_count
            }
        except ValueError:
            return None

    @staticmethod
    def encrypt_file_form() -> dict:
        try:
            key, file_with_path = Forms._encrypt_form(
                path_text = "Enter the file path",
                bad_path_text = "Please enter a valid file path"
            )
            return {"key": key, "file_with_path": file_with_path}

        except ValueError:
            return None

    @staticmethod
    def encrypt_directory_form() -> dict:
        try:
            key, directory_path = Forms._encrypt_form(
                path_text = "Enter the directory path",
                bad_path_text = "Please enter a valid directory path",
                dir_mode = True
            )
            return {"key": key, "directory_path": directory_path}
        except ValueError:
            return None

    @staticmethod
    def decrypt_file_form() -> dict:
        try:
            key, directory_path = Forms._decrypt_form(
                path_text = "Enter the directory path",
                bad_path_text = "Please enter a valid directory path",
            )
            return {"key": key, "file_with_path": directory_path}

        except ValueError:
            return None

    @staticmethod
    def decrypt_directory_form() -> dict:
        try:
            key, directory_path = Forms._decrypt_form(
                path_text = "Enter the directory path",
                bad_path_text = "Please enter a valid directory path",
                dir_mode = True
            )
            return {"key": key, "directory_path": directory_path}

        except ValueError:
            return None


class Display:

    @staticmethod
    def help_page() -> None:
        juice_console.rule("[bold green] Help", style="blue")
        juice_console.print(Panel.fit(static.HELP_AND_CREDITS, title="Help"))
    
    @staticmethod
    def encrypt_results(key, file) -> None:
        juice_console.print(f"[bold italic green]:locked_with_key: Encrypted {file}")
        juice_console.print(f"[bold red] SAVE[/bold red] [bold yellow]AND DONT[/bold yellow] [bold red]SHARE[/bold red] :shushing_face: :clown_face: [bold yellow]THIS[/bold yellow] :person_facepalming:")
        juice_console.print(f"[bold red italic]:key:{key}")
        juice_console.print(f"[bold yellow] YOU WERE WARNED :moai:")



def analyze_data(form: dict):
    form_repr = {}
    for key, value in form.items():
        if isinstance(value, (str, bool, int, float)) or value is None:
            form_repr[key] = value
        elif isinstance(value, bytes):
            form_repr[key] = value.decode()

    juice_console.print(
        Padding("[bold green] Your Data", (1, 1), expand=False))
    juice_console.print_json(data=form_repr)
    return Confirm.ask("[bold yellow] Do you want continue? :warning:")