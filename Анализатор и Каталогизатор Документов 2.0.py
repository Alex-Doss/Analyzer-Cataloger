import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import openai
from PyPDF2 import PdfReader
import docx
import pandas as pd
import mimetypes
import re
import time

# Установите ваш API-ключ OpenAI
openai.api_key = 'Your data should be here'


def sanitize_filename(filename, max_length=255):
    """
    Удаляет или заменяет недопустимые символы для имени файла/папки в Windows и ограничивает длину.
    """
    filename = re.sub(r'[<>:"/\\|?*\n]+', '_', filename)
    return filename[:max_length]


def analyze_document(text, user_instructions=""):
    """
    Анализирует текст документа с использованием GPT и возвращает предложенную категорию и краткое описание.
    Если текст слишком длинный, разбивает его на части для обработки.
    """
    max_tokens = 4096
    text_chunks = [text[i:i + max_tokens] for i in range(0, len(text), max_tokens)]

    full_response = ""
    for chunk in text_chunks:
        prompt = f"Проанализируй следующий текст и предложи категорию для файла. Также создай краткое описание для него. {user_instructions}\n\nТекст:\n{chunk}"

        for attempt in range(3):  # Попробовать сделать до 3 попыток
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Ты помощник для анализа документов."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                full_response += response.choices[0].message['content'].strip() + "\n"
                break  # Выйти из цикла попыток, если запрос успешен
            except openai.error.APIError as e:
                if attempt < 2:  # Только повторить, если это не последняя попытка
                    time.sleep(5)  # Подождать 5 секунд перед повторной попыткой
                else:
                    raise e  # После 3 попыток, если не удалось, пробросить ошибку

    return full_response.strip()


def extract_text_from_file(file_path):
    """
    Извлекает текст из файлов различных форматов (PDF, DOCX, TXT, Excel, HTML и др.)
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == '.pdf':
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            text = "\n".join(page.extract_text() for page in reader.pages)
    elif ext in ['.doc', '.docx']:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
        text = df.to_string()
    elif ext in ['.txt', '.py', '.php', '.html', '.js', '.css']:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and mime_type.startswith('text'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

    return text


def process_file(file_path, user_instructions):
    """
    Обрабатывает файл, извлекает текст и передает его на анализ GPT.
    Возвращает категорию и краткое описание.
    """
    text = extract_text_from_file(file_path)
    if text:
        category = analyze_document(text, user_instructions)
        return category, text
    return None, None


def find_existing_folder_by_category(output_folder_path, category):
    """
    Ищет существующую папку, которая соответствует категории.
    """
    sanitized_category = sanitize_filename(category[:30]).lower()  # Ограничение до 30 символов
    for folder_name in os.listdir(output_folder_path):
        if sanitized_category in folder_name.lower():
            return os.path.join(output_folder_path, folder_name)
    return None


def organize_files(input_folder_path, output_folder_path, user_instructions):
    """
    Организует файлы по предложенным категориям, создавая каталоги и краткие описания.
    Если подходящий каталог уже существует, добавляет файлы в него.
    """
    description_file_path = os.path.join(output_folder_path, 'all_descriptions.txt')

    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            category, text = process_file(file_path, user_instructions)
            if category:
                existing_folder = find_existing_folder_by_category(output_folder_path, category)

                if existing_folder:
                    target_dir = existing_folder
                else:
                    sanitized_category = sanitize_filename(category[:50])  # Ограничение до 30 символов
                    target_dir = os.path.join(output_folder_path, sanitized_category)
                    os.makedirs(target_dir, exist_ok=True)

                # Ограничиваем длину имени файла
                sanitized_file_name = sanitize_filename(os.path.basename(file))[:100]

                # Ограничиваем длину полного пути
                target_file_path = os.path.join(target_dir, sanitized_file_name)
                if len(target_file_path) > 260:
                    target_file_path = target_file_path[:260]

                # Убедитесь, что каталог для файла существует
                os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

                try:
                    # Копируем файл в соответствующую папку
                    shutil.copy(file_path, target_file_path)
                except FileNotFoundError:
                    print(f"Не удалось скопировать файл: {file_path} -> {target_file_path}")
                    continue

                # Добавляем описание в общий файл описаний
                with open(description_file_path, 'a', encoding='utf-8') as desc_file:
                    desc_file.write(f"Файл: {file}\nКатегория: {category}\nОписание:\n{text[:1000]}...\n\n")


def select_folders():
    """
    Обработчик выбора папок. Запускает процесс организации файлов.
    """
    input_folder_path = filedialog.askdirectory(title="Выберите папку с документами для анализа")
    output_folder_path = filedialog.askdirectory(title="Выберите папку для сохранения организованных файлов")

    if input_folder_path and output_folder_path:
        user_instructions = instruction_text.get("1.0", tk.END).strip()
        organize_files(input_folder_path, output_folder_path, user_instructions)
        messagebox.showinfo("Завершено", "Файлы обработаны и рассортированы.")


# Создание графического интерфейса с использованием Tkinter
root = tk.Tk()
root.title("Анализатор и Каталогизатор Документов")

instruction_label = tk.Label(root, text="Введите инструкции для анализа (опционально):")
instruction_label.pack(pady=10)

instruction_text = tk.Text(root, height=10, width=50)
instruction_text.pack(pady=10)

select_button = tk.Button(root, text="Выбрать папки для обработки и сохранения", command=select_folders)
select_button.pack(pady=20)

root.mainloop()
