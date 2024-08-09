import os
import re
import json
import time
from hashlib import md5, sha1, sha256, sha512
from multiprocessing import Pool
from tqdm import tqdm

# Логотип
LOGO = """

  /$$$$$$                      /$$$$$$$                        /$$               /$$   /$$                     /$$      
 /$$__  $$                    | $$__  $$                      | $$              | $$  | $$                    | $$      
| $$  \__/  /$$$$$$  /$$$$$$$ | $$  \ $$  /$$$$$$  /$$   /$$ /$$$$$$    /$$$$$$ | $$  | $$  /$$$$$$   /$$$$$$$| $$$$$$$ 
| $$ /$$$$ /$$__  $$| $$__  $$| $$$$$$$  /$$__  $$| $$  | $$|_  $$_/   /$$__  $$| $$$$$$$$ |____  $$ /$$_____/| $$__  $$
| $$|_  $$| $$$$$$$$| $$  \ $$| $$__  $$| $$  \__/| $$  | $$  | $$    | $$$$$$$$| $$__  $$  /$$$$$$$|  $$$$$$ | $$  \ $$
| $$  \ $$| $$_____/| $$  | $$| $$  \ $$| $$      | $$  | $$  | $$ /$$| $$_____/| $$  | $$ /$$__  $$ \____  $$| $$  | $$
|  $$$$$$/|  $$$$$$$| $$  | $$| $$$$$$$/| $$      |  $$$$$$/  |  $$$$/|  $$$$$$$| $$  | $$|  $$$$$$$ /$$$$$$$/| $$  | $$
 \______/  \_______/|__/  |__/|_______/ |__/       \______/    \___/   \_______/|__/  |__/ \_______/|_______/ |__/  |__/
                                                                                                                                                                                                                             
"""

# Загрузка конфигурационного файла
with open("config.json", 'r') as config_file:
    config_data = json.load(config_file)

# Глобальные переменные
wordlist_passwords = []
WORDLIST_FILE = config_data["wordlist"]
FOUND_PASSWORD = None

# Функция для получения соли и хэша из строки
def extract_hash_and_salt(input_str: str) -> tuple:
    if '$' in input_str:
        if hash_salt_matches := re.findall(r"[^$SHA]\w{31,127}", input_str):
            if len(hash_salt_matches) > 1:
                return (hash_salt_matches[1], hash_salt_matches[0]) if len(hash_salt_matches[1]) > len(hash_salt_matches[0]) else (hash_salt_matches[0], hash_salt_matches[1])
            split_matches = re.findall(r"[^$SHA]\w+", input_str)
            salt_part = ''.join(x for x in split_matches if x != hash_salt_matches[0])
            if salt_part:
                return (hash_salt_matches[0], salt_part)
            return (hash_salt_matches[0], None)
        return (None, None)
    elif ':' in input_str:
        split_parts = input_str.split(':')
        return (split_parts[0], split_parts[1]) if len(split_parts[0]) > len(split_parts[1]) else (split_parts[1], split_parts[0])
    elif len(input_str) in [32, 40, 64, 128]:  # MD5, SHA1, SHA256, SHA512 without salt
        return (input_str, None)
    return (None, None)

# Функция для загрузки списка паролей
def load_wordlist(file_path: str):
    global wordlist_passwords
    with open(file_path, 'r', encoding='latin-1') as file:
        wordlist_passwords = [line.strip() for line in file]

# Функция для выполнения атаки методом перебора
def perform_bruteforce(password: str, hash_value: str, salt_value: str or None = None):
    global FOUND_PASSWORD
    if len(hash_value) == 32:  # MD5
        if salt_value:
            if md5(password.encode() + salt_value.encode()).hexdigest() == hash_value or \
               md5(salt_value.encode() + password.encode()).hexdigest() == hash_value or \
               md5(md5(password.encode()).hexdigest().encode() + salt_value.encode()).hexdigest() == hash_value:
                FOUND_PASSWORD = password
        else:
            if md5(password.encode()).hexdigest() == hash_value:
                FOUND_PASSWORD = password
    elif len(hash_value) == 40:  # SHA1
        if salt_value:
            if sha1(password.encode() + salt_value.encode()).hexdigest() == hash_value or \
               sha1(salt_value.encode() + password.encode()).hexdigest() == hash_value or \
               sha1(sha1(password.encode()).hexdigest().encode() + salt_value.encode()).hexdigest() == hash_value:
                FOUND_PASSWORD = password
        else:
            if sha1(password.encode()).hexdigest() == hash_value:
                FOUND_PASSWORD = password
    elif len(hash_value) == 64:  # SHA256
        if salt_value:
            if sha256(password.encode() + salt_value.encode()).hexdigest() == hash_value or \
               sha256(salt_value.encode() + password.encode()).hexdigest() == hash_value or \
               sha256(sha256(password.encode()).hexdigest().encode() + salt_value.encode()).hexdigest() == hash_value:
                FOUND_PASSWORD = password
        else:
            if sha256(password.encode()).hexdigest() == hash_value:
                FOUND_PASSWORD = password
    elif len(hash_value) == 128:  # SHA512
        if salt_value:
            if sha512(password.encode() + salt_value.encode()).hexdigest() == hash_value or \
               sha512(salt_value.encode() + password.encode()).hexdigest() == hash_value or \
               sha512(sha512(password.encode()).hexdigest().encode() + salt_value.encode()).hexdigest() == hash_value:
                FOUND_PASSWORD = password
        else:
            if sha512(password.encode()).hexdigest() == hash_value:
                FOUND_PASSWORD = password

# Основная функция для выполнения перебора
def start_bruteforce(hash_value: str, salt_value: str):
    global FOUND_PASSWORD
    if not hash_value:
        print("Ошибка: Невозможно извлечь хэш из введённой строки.")
        return
    FOUND_PASSWORD = None
    print("Загрузка словаря завершена, начинаем перебор...")
    start_time = time.time()
    for pwd in tqdm(wordlist_passwords, desc="Перебор паролей", unit="пароль"):
        if FOUND_PASSWORD is not None:
            break
        perform_bruteforce(pwd, hash_value, salt_value)
    end_time = time.time()
    if FOUND_PASSWORD is not None:
        print(f"Найдено за {end_time - start_time:.2f} секунд => {FOUND_PASSWORD}")
    else:
        print(f"Результатов не найдено, завершено за {end_time - start_time:.2f} секунд")

# Функция для ввода хэша вручную
def input_raw_hash():
    raw_hash = input("Введите хэш > ")
    hash_value, salt_value = extract_hash_and_salt(raw_hash)
    start_bruteforce(hash_value, salt_value)
    post_bruteforce_options()

# Функция для ввода хэша и соли вручную
def input_hash_and_salt():
    hash_value = input("Введите хэш > ")
    salt_value = input("Введите соль > ")
    start_bruteforce(hash_value, salt_value)
    post_bruteforce_options()

# Функция для выполнения перебора нескольких хэшей
def brute_multiple_hashes(file_path: str):
    global FOUND_PASSWORD
    with open(file_path, 'r') as file:
        hashes = [line.strip() for line in file if line.strip()]
    start_time = time.time()
    for hash_entry in hashes:
        hash_value, salt_value = extract_hash_and_salt(hash_entry)
        if hash_value:
            FOUND_PASSWORD = None
            for pwd in tqdm(wordlist_passwords, desc=f"Перебор {hash_entry[:10]}...", unit="пароль"):
                if FOUND_PASSWORD is not None:
                    break
                perform_bruteforce(pwd, hash_value, salt_value)
            end_time = time.time()
            if FOUND_PASSWORD is not None:
                print(f"\nНайдено за {end_time - start_time:.2f} секунд => {FOUND_PASSWORD}")
            else:
                print(f"\nРезультатов не найдено для {hash_entry[:10]}..., завершено за {end_time - start_time:.2f} секунд")
    post_bruteforce_options()

# Функция для отображения логотипа и опций после завершения перебора
def post_bruteforce_options():
    print(LOGO)
    print("1) Ввести новый хэш")
    print("2) Выйти из программы")
    choice = input("> ")
    if choice == "1":
        main_menu()
    elif choice == "2":
        exit()

# Главная функция
def main_menu():
    global WORDLIST_FILE
    if WORDLIST_FILE is None:
        WORDLIST_FILE = input("Введите путь к словарю > ")
        if not os.path.isfile(WORDLIST_FILE):
            exit()
        load_wordlist(WORDLIST_FILE)
    else:
        load_wordlist(WORDLIST_FILE)
        with open("config.json", 'w') as config_file:
            config_file.write(json.dumps({
                "wordlist": WORDLIST_FILE
            }, indent=4))
    while True:
        print(LOGO)
        print("1) Ввод хэша вручную")
        print("2) Ввод хэша и соли")
        print("3) Перебор нескольких хэшей")
        choice = input("> ")
        if choice == "1":
            input_raw_hash()
        elif choice == "2":
            input_hash_and_salt()
        elif choice == "3":
            file_path = input("Введите путь к файлу с хэшами > ")
            if os.path.isfile(file_path):
                brute_multiple_hashes(file_path)
            else:
                print("Файл не найден!")

if __name__ == "__main__":
    main_menu()
