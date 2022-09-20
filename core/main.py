from src.utils import *
from src.generator.pass_gen import PasswordGenerator

def finish():
    exit_confirmation = Confirm.ask("Do you want quit? [yellow]:warning:")
    if exit_confirmation:
        os._exit(0)
    else:
        menu()


class Main:

    @staticmethod
    def new_password() -> None:
        data = Forms.passowrd_form()
        
        if data is None:
            return Main.new_password()

        while not analyze_data(data):
            option = Prompt.ask("Enter an option",
                                choices=["menu", "edit"],
                                default="edit")

            if option == "menu":
                menu()

            elif option == "edit":
                data = Forms.passowrd_form()

        password = PasswordGenerator.generate_random_password(**data)
        juice_console.print(f"[bold italic green] {password}")


def menu():
    console.print(Panel.fit(MENU, title="Menu"))
    option = Prompt.ask("Enter an option",
                        choices=[
                            "1",  "2",  "3",  "4",    "5",
                            "np", "ef", "df", "help", "exit"
                        ],
                        default="1")

    if option in {"1", "np"}:
        Main.new_password()

    elif option in {"4", "help"}:
        Display.help_page()

    else:
        finish()


def init():
    console.rule(f"[bold #72c3f0] Juice {VERSION}", style="blue")
    menu()

if __name__ == "__main__":
    console = Console()
    init()
