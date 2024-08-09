# GenBruteHash
This project is a script for sorting passwords by their hashes. It supports several types of hashing, including MD5, SHA1, SHA256, SHA512.

# EN:
## Installation
1. Clone the repository to your computer:
 ```bash
    git clone https://github.com/geniuszlyy/GenBruteHash.git
 ```
2. Go to the project directory:
 ```bash
    cd GenBruteHash
 ```
3. Install the necessary dependencies:
```bash
    pip install tqdm
```
4. Create a `config.json` file in the root directory of the project:
 ```json
    {
        "wordlist": "path/to/your/wordlist.txt"
    }
 ```
Make sure that the path to the password dictionary file (`wordlist.txt `) is specified correctly.

## Usage

### Running the script

To run the script, run the command:
```bash
python main.py
```
## Menu
After running the script, you will see the following menu:
![image](https://github.com/user-attachments/assets/679bcc5e-5487-4ccc-b146-29018c79c4f1)

## Choose one of the options:

1. Entering the hash manually:
- Enter the hash you want to decrypt.
- The program will automatically detect the hash type and start iterating.

2. Entering the hash and salt:
- Enter the hash.
- Enter the salt (if applicable).
- The program will start iterating with the specified hash and salt.

3. Iterating over multiple hashes:
- Enter the path to the file containing multiple hashes (one hash per line).
- The program will start iterating over each hash in the file.

## Supported hash types
The script supports the following types of hashes:
- MD5
- SHA1
- SHA256
- SHA512

# Usage example
1. Entering the hash manually:
```bash
Enter the hash > $SHA256$94b2c66131625ea7122095fb6a29d36e9b4b7b4c0d9229893b798a41fc084921
```
2. Entering the hash and salt:
```bash
Enter the hash > 94b2c66131625ea7122095fb6a29d36e9b4b7b4c0d9229893b798a41fc084921
Enter salt > shippuuden
```
3. Iterating over multiple hashes:
```bash
Enter the path to the file with the hashes > hashes.txt
```
![image](https://github.com/user-attachments/assets/27b93737-2063-4189-ba3c-4d071e2f5006)


# RU:
## Установка
1. Клонируйте репозиторий на ваш компьютер:
 ```bash
    git clone https://github.com/geniuszlyy/GenBruteHash.git
 ```
2. Перейдите в директорию проекта:
 ```bash
    cd GenBruteHash
 ```
3. Установите необходимые зависимости:
```bash
    pip install tqdm
```
4. Создайте файл `config.json` в корневой директории проекта:
 ```json
    {
        "wordlist": "path/to/your/wordlist.txt"
    }
 ```
Убедитесь, что путь к файлу словаря паролей (`wordlist.txt`) указан правильно.

## Использование

### Запуск скрипта

Для запуска скрипта выполните команду:
```bash
python main.py
```
## Меню
После запуска скрипта вы увидите следующее меню:
![image](https://github.com/user-attachments/assets/679bcc5e-5487-4ccc-b146-29018c79c4f1)

## Выберите один из вариантов:

1. Ввод хэша вручную:
- Введите хэш, который вы хотите расшифровать.
- Программа автоматически определит тип хэша и начнет перебор.

2. Ввод хэша и соли:
- Введите хэш.
- Введите соль (если применимо).
- Программа начнет перебор с указанными хэшом и солью.

3. Перебор нескольких хэшей:
- Введите путь к файлу, содержащему несколько хэшей (по одному хэшу на строку).
- Программа начнет перебор для каждого хэша в файле.

## Поддерживаемые типы хэшей
Скрипт поддерживает следующие типы хэшей:
- MD5
- SHA1
- SHA256
- SHA512

# Пример использования
1. Ввод хэша вручную:
```bash
Введите хэш > $SHA256$94b2c66131625ea7122095fb6a29d36e9b4b7b4c0d9229893b798a41fc084921
```
2. Ввод хэша и соли:
```bash
Введите хэш > 94b2c66131625ea7122095fb6a29d36e9b4b7b4c0d9229893b798a41fc084921
Введите соль > shippuuden
```
3. Перебор нескольких хэшей:
```bash
Введите путь к файлу с хэшами > hashes.txt
```
![image](https://github.com/user-attachments/assets/5d655a6c-6b81-4b41-a614-bf7860642663)
