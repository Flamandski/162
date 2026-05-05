import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")

        self.history_file = "password_history.json"
        self.password_history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Генератор случайных паролей",
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Ползунок длины пароля
        length_frame = tk.Frame(self.root)
        length_frame.pack(pady=10)

        tk.Label(length_frame, text="Длина пароля (8–32):",
                font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        self.length_var = tk.IntVar(value=12)
        self.length_slider = tk.Scale(length_frame, from_=8, to=32,
                                     orient=tk.HORIZONTAL, variable=self.length_var)
        self.length_slider.pack(side=tk.LEFT, padx=5)

        # Чекбоксы для выбора символов
        checkbox_frame = tk.Frame(self.root)
        checkbox_frame.pack(pady=10)

        self.digits_var = tk.BooleanVar(value=True)
        self.letters_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=False)

        tk.Checkbutton(checkbox_frame, text="Цифры (0-9)",
                     variable=self.digits_var, font=("Arial", 12)).pack(anchor=tk.W)
        tk.Checkbutton(checkbox_frame, text="Буквы (a-z, A-Z)",
                     variable=self.letters_var, font=("Arial", 12)).pack(anchor=tk.W)
        tk.Checkbutton(checkbox_frame, text="Спецсимволы (!@#$%)",
                     variable=self.special_var, font=("Arial", 12)).pack(anchor=tk.W)

        # Кнопка генерации
        generate_button = tk.Button(
            self.root,
            text="Сгенерировать пароль",
            command=self.generate_password,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20
        )
        generate_button.pack(pady=20)

        # Поле вывода пароля
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10)

        tk.Label(result_frame, text="Сгенерированный пароль:",
                font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(result_frame,
                                   textvariable=self.password_var,
                                   width=30,
                                   font=("Arial", 12),
                                   state="readonly")
        self.password_entry.pack(side=tk.LEFT, padx=10)

        # Таблица истории
        history_label = tk.Label(self.root, text="История паролей:",
                           font=("Arial", 12, "bold"))
        history_label.pack(pady=(20, 5))

        columns = ("ID", "Пароль", "Длина", "Дата создания")
        self.history_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)

        self.history_tree.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        # Обновление таблицы истории
        self.update_history_table()

    def generate_password(self):
        # Проверка выбора хотя бы одного типа символов
        if not (self.digits_var.get() or self.letters_var.get() or self.special_var.get()):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        # Получение параметров
        length = self.length_var.get()

        # Формирование набора символов
        chars = ""
        if self.digits_var.get():
            chars += "0123456789"
        if self.letters_var.get():
            chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.special_var.get():
            chars += "!@#$%^&*"

        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))

        # Сохранение в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            "id": len(self.password_history) + 1,
            "password": password,
            "length": length,
            "timestamp": timestamp
        }
        self.password_history.append(new_entry)

        # Сохранение истории в файл
        self.save_history()

        # Обновление интерфейса
        self.password_var.set(password)
        self.update_history_table()

    def load_history(self):
        """Загрузка истории из JSON-файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_history(self):
        """Сохранение истории в JSON-файл"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.password_history, f, ensure_ascii=False, indent=4)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def update_history_table(self):
        """Обновление таблицы истории"""
        # Очистка таблицы
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Заполнение таблицы данными
        for entry in reversed(self.password_history[-50:]):  # Последние 50 записей
            self.history_tree.insert("", tk.END, values=(
                entry["id"],
                entry["password"],
                entry["length"],
                entry["timestamp"]
            ))

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
