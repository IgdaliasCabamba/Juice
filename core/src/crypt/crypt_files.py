from cryptography.fernet import Fernet
import pathlib
import glob
import os
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn


class JEncrypt:

    def encrypt_file(key: bytes, file_with_path: str) -> bool:
        try:
            fernet = Fernet(key)

            with open(file_with_path, 'rb') as file:
                original_content = file.read()

            encrypted_content = fernet.encrypt(original_content)

            with open(file_with_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_content)

            return True
        except Exception as e:
            print(e)
            return False

    def decrypt_file(key: bytes, file_with_path: str) -> bool:
        try:
            fernet = Fernet(key)

            with open(file_with_path, 'rb') as enc_file:
                encrypted_content = enc_file.read()

            decrypted_content = fernet.decrypt(encrypted_content)

            with open(file_with_path, 'wb') as dec_file:
                dec_file.write(decrypted_content)

            return True
        except Exception as e:
            print(e)
            return False

    def encrypt_directory(key: bytes, directory_path: str) -> bool:
        path = str(pathlib.Path(os.path.normpath(directory_path)).joinpath("**"))
        fernet = Fernet(key)
        files = list(glob.iglob(path, recursive=True))

        with Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            transient=True) as progress:

            task = progress.add_task("[green]Encrypting...", total=len(files))

            for file_with_path in files:
                if pathlib.Path(file_with_path).is_file():

                    with open(file_with_path, 'rb') as file:
                        original_content = file.read()

                    encrypted_content = fernet.encrypt(original_content)

                    with open(file_with_path, 'wb') as encrypted_file:
                        encrypted_file.write(encrypted_content)

                progress.update(task, advance=1)

        return True

    def decrypt_directory(key: bytes, directory_path: str) -> bool:
        path = str(pathlib.Path(os.path.normpath(directory_path)).joinpath("**"))
        fernet = Fernet(key)
        files = list(glob.iglob(path, recursive=True))

        with Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            transient=True) as progress:

            task = progress.add_task("[green]Decrypting...", total=len(files))

            for file_with_path in files:
                if pathlib.Path(file_with_path).is_file():

                    with open(file_with_path, 'rb') as enc_file:
                        encrypted_content = enc_file.read()

                    decrypted_content = fernet.decrypt(encrypted_content)

                    with open(file_with_path, 'wb') as decrypted_file:
                        decrypted_file.write(decrypted_content)

                progress.update(task, advance=1)

        return True
