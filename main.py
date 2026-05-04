import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

FILENAME = 'quotes.json'

# Предопределённые цитаты
predefined_quotes = [
    {"quote": "Будущее принадлежит тем, кто верит в красоту своей мечты.", "author": "Эллен Джонсон-Серлифф", "topic": "мотивация"},
    {"quote": "Самое лучшее время для посадки дерева — 20 лет назад. Второе лучшее — сегодня.", "author": "Китайская пословица", "topic": "мотивация"},
    {"quote": "Жизнь — это 10% того, что с тобой происходит, и 90% того, как ты на это реагируешь.", "author": "Чарльз Риттер", "topic": "философия"},
    # Можно добавить ещё
]

# Загрузка истории из файла
def load_history():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение истории в файл
def save_history(data):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.history = load_history()
        self.filtered_quotes = self.history.copy()

        self.create_widgets()
        self.update_quote_list()

    def create_widgets(self):
        # Кнопка генерации цитаты
        self.generate_btn = tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote)
        self.generate_btn.pack(pady=5)

        # Поле отображения текущей цитаты
        self.current_label = tk.Label(self.root, text="", wraplength=400, font=('Arial', 14))
        self.current_label.pack(pady=5)

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, padx=5)
        self.author_filter_entry = tk.Entry(filter_frame)
        self.author_filter_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=2, padx=5)
        self.topic_filter_entry = tk.Entry(filter_frame)
        self.topic_filter_entry.grid(row=0, column=3, padx=5)

        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=5)

        show_all_btn = tk.Button(filter_frame, text="Показать всё", command=self.show_all)
        show_all_btn.grid(row=0, column=5, padx=5)

        # Список истории
        self.history_listbox = tk.Listbox(self, height=10, width=80)
        self.history_listbox.pack(pady=10)

        # Добавление новой цитаты
        add_frame = tk.Frame(self)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Новая цитата:").grid(row=0, column=0, padx=5)
        self.new_quote_entry = tk.Entry(add_frame, width=40)
        self.new_quote_entry.grid(row=0, column=1, padx=5)

        tk.Label(add_frame, text="Автор:").grid(row=1, column=0, padx=5)
        self.new_author_entry = tk.Entry(add_frame, width=20)
        self.new_author_entry.grid(row=1, column=1, padx=5)

        tk.Label(add_frame, text="Тема:").grid(row=2, column=0, padx=5)
        self.new_topic_entry = tk.Entry(add_frame, width=20)
        self.new_topic_entry.grid(row=2, column=1, padx=5)

        add_btn = tk.Button(add_frame, text="Добавить цитату", command=self.add_quote)
        add_btn.grid(row=3, column=0, columnspan=2, pady=5)

    def generate_quote(self):
        quote = random.choice(predefined_quotes)
        self.current_label.config(text=f"\"{quote['quote']}\" \n— {quote['author']} ({quote['topic']})")
        self.history.append(quote)
        save_history(self.history)
        self.update_quote_list()

    def update_quote_list(self):
        self.history_listbox.delete(0, tk.END)
        for q in self.history:
            self.history_listbox.insert(tk.END, f"\"{q['quote']}\" — {q['author']} ({q['topic']})")

    def add_quote(self):
        quote_text = self.new_quote_entry.get().strip()
        author = self.new_author_entry.get().strip()
        topic = self.new_topic_entry.get().strip()

        if not quote_text or not author or not topic:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        new_quote = {"quote": quote_text, "author": author, "topic": topic}
        self.history.append(new_quote)
        save_history(self.history)
        self.new_quote_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_topic_entry.delete(0, tk.END)
        self.update_quote_list()

    def apply_filter(self):
        author_filter = self.author_filter_entry.get().strip().lower()
        topic_filter = self.topic_filter_entry.get().strip().lower()

        self.filtered_quotes = self.history.copy()

        if author_filter:
            self.filtered_quotes = [q for q in self.filtered_quotes if author_filter in q['author'].lower()]

        if topic_filter:
            self.filtered_quotes = [q for q in self.filtered_quotes if topic_filter in q['topic'].lower()]

        self.history_listbox.delete(0, tk.END)
        for q in self.filtered_quotes:
            self.history_listbox.insert(tk.END, f"\"{q['quote']}\" — {q['author']} ({q['topic']})")

    def show_all(self):
        self.author_filter_entry.delete(0, tk.END)
        self.topic_filter_entry.delete(0, tk.END)
        self.update_quote_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
