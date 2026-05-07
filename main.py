# Импорт библиотек
import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("450x550")

        self.history_file = "history.json"

        # Элементы интерфейса
        # Ползунок длины пароля
        tk.Label(root, text="Длина пароля:", font=("Arial", 10, "bold")).pack(pady=(15, 0))
        self.length_label = tk.Label(root, text="12")
        self.length_label.pack()

        # Проверка корректности (ограничена мин/макс значениями в слайдере)
        self.length_slider = tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL,
                                      command=self.update_length_label, length=300)
        self.length_slider.set(12)
        self.length_slider.pack(pady=5)

        # Чекбоксы для выбора символов
        self.var_digits = tk.BooleanVar(value=True)
        self.var_letters = tk.BooleanVar(value=True)
        self.var_spec = tk.BooleanVar(value=False)

        tk.Checkbutton(root, text="Цифры (0-9)", variable=self.var_digits).pack()
        tk.Checkbutton(root, text="Буквы (a-z, A-Z)", variable=self.var_letters).pack()
        tk.Checkbutton(root, text="Спецсимволы (!@#$%^&*)", variable=self.var_spec).pack()

        # Кнопка генерации
        self.btn_gen = tk.Button(root, text="Сгенерировать пароль", command=self.generate,
                                 bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.btn_gen.pack(pady=20)

        self.entry_result = tk.Entry(root, font=("Courier", 12), justify="center", width=30)
        self.entry_result.pack(pady=5)

        # Таблица истории (используем Treeview)
        tk.Label(root, text="История (последние 10):", font=("Arial", 10)).pack(pady=(15, 0))

        self.tree = ttk.Treeview(root, columns=("Password"), show="headings", height=8)
        self.tree.heading("Password", text="Сгенерированные пароли")
        self.tree.column("Password", anchor="center")
        self.tree.pack(pady=10, fill=tk.X, padx=20)

        # 3. Загрузка истории при старте
        self.load_history()

    def update_length_label(self, val):
        self.length_label.config(text=val)