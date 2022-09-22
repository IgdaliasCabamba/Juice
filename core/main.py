from src.utils import *
from src.generator.pass_gen import PasswordGenerator
from src.crypt.crypt_files import JEncrypt

def finish() -> None:
    exit_confirmation = Confirm.ask("[bold yellow]Do you want quit? [yellow]:warning:")
    console.rule(f"[bold red italic] *goodbye good riddance*", style="blue")
    if exit_confirmation:
        os._exit(0)
    else:
        return menu()


class Main:

    @staticmethod
    def edit_middleware(data: dict, function: Callable, *args, **kwargs) -> Any:
        while not analyze_data(data):
            option = Prompt.ask("Enter an option",
                                choices=["menu", "edit"],
                                default="edit")

            if option == "menu":
                menu()

            elif option == "edit":
                data = function(*args, **kwargs)
        
        return data

    @staticmethod
    def new_password() -> None:
        data = Forms.passowrd_form()
        
        if data is None:
            return Main.new_password()
        
        data = Main.edit_middleware(data, Forms.passowrd_form)

        password = PasswordGenerator.generate_random_password(**data)
        juice_console.print(f"[bold italic green] {password}")
    
    @staticmethod
    def encrypt_file():
        data = Forms.encrypt_file_form()
        
        if data is None:
            return Main.encrypt_file()

        data = Main.edit_middleware(data, Forms.encrypt_file_form)

        result = JEncrypt.encrypt_file(**data)
        if result:
            Display.encrypt_results(data['key'].decode(), data['file_with_path'])
        else:
            juice_console.print(f"[bold orange] Failed to decrypt {data['file_with_path']} :moai:")
    
    @staticmethod
    def decrypt_file():
        data = Forms.decrypt_file_form()
        
        if data is None:
            return Main.decrypt_file()

        data = Main.edit_middleware(data, Forms.decrypt_file_form)

        result = JEncrypt.decrypt_file(**data)
        if result:
            juice_console.print(f"[bold italic green] Decrypted {data['file_with_path']}")
            juice_console.print(f":relieved_face:")
        else:
            juice_console.print(f"[bold orange] Failed to decrypt {data['file_with_path']} :moai:")
    
    @staticmethod
    def encrypt_directory():
        data = Forms.encrypt_directory_form()
        
        if data is None:
            return Main.encrypt_file()

        data = Main.edit_middleware(data, Forms.encrypt_directory_form)

        result = JEncrypt.encrypt_directory(**data)
        if result:
            Display.encrypt_results(data['key'].decode(), data['directory_path'])
        else:
            juice_console.print(f"[bold orange] Failed to decrypt {data['directory_path']} :moai:")
    
    @staticmethod
    def decrypt_directory():
        data = Forms.decrypt_directory_form()
        
        if data is None:
            return Main.decrypt_directory()

        data = Main.edit_middleware(data, Forms.decrypt_directory_form)

        result = JEncrypt.decrypt_directory(**data)
        if result:
            juice_console.print(f"[bold italic green] Decrypted {data['directory_path']}")
            juice_console.print(f":relieved_face:")
        else:
            juice_console.print(f"[bold orange] Failed to decrypt {data['directory_path']} :moai:")


def menu():
    while True:
        console.print(Panel.fit(static.MENU, title="Menu"))
        option = Prompt.ask("Enter an option",
                            choices=["1", "2", "3", "4", "5", "6", "7"],
                            default="1")

        if option == "1":
            Main.new_password()
        
        elif option == "2":
            Main.encrypt_file()
        
        elif option == "3":
            Main.decrypt_file()
        
        elif option == "4":
            Main.encrypt_directory()
        
        elif option == "5":
            Main.decrypt_directory()

        elif option == "6":
            Display.help_page()

        else:
            return finish()


def init():
    console.rule(f"[bold #72c3f0] Juice {static.VERSION}", style="blue")
    menu()

if __name__ == "__main__":
    console = Console()
    init()
