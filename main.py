import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import random

class RandomQuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.history = []

        # Предопределённые цитаты
        self.quotes = [
            {"text": "Знание — сила", "author": "Фрэнсис Бэкон", "topic": "Мудрость"},
            {"text": "Быть или не быть — вот в чём вопрос", "author": "Уильям Шекспир", "topic": "Философия"},
            {"text": "Познай самого себя", "author": "Сократ", "topic": "Самопознание"},
            {"text": "Я мыслю, следовательно, существую", "author": "Рене Декарт", "topic": "Философия"},
            {"text": "Через тернии к звёздам", "author": "Сенека", "topic": "Мотивация"}
        ]

        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Кнопка генерации цитаты
        tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote).pack(pady=10)

        # Отображение текущей цитаты
        self.quote_text = tk.Label(self.root, text="", wraplength=400, justify="left")
        self.quote_text.pack(pady=5)
        self.author_text = tk.Label(self.root, text="", justify="left")
        self.author_text.pack(pady=5)
        self.topic_text = tk.Label(self.root, text="", justify="left")
        self.topic_text.pack(pady=5)

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0)
        self.author_filter = ttk.Combobox(filter_frame, state="readonly")
        self.author_filter.grid(row=0, column=1, padx=5)
        self.author_filter.bind("<<ComboboxSelected>>", self.apply_filters)

        tk.Label(filter_frame, text="Фильтр по теме:").grid(row=1, column=0)
        self.topic_filter = ttk.Combobox(filter_frame, state="readonly")
        self.topic_filter.grid(row=1, column=1, padx=5)
        self.topic_filter.bind("<<ComboboxSelected>>", self.apply_filters)

        # История цитат
        tk.Label(self.root, text="История цитат:").pack(pady=(10, 0))
        self.history_display = scrolledtext.ScrolledText(self.root, height=10, width=50)
        self.history_display.pack(pady=5, padx=10)

        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Очистить историю", command=self.clear_history).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Сохранить данные", command=self.save_data).grid(row=0, column=1, padx=5)

        self.update_filters()
        self.update_history_display()

    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Предупреждение", "Список цитат пуст!")
            return

        quote = random.choice(self.quotes)
        self.history.append(quote)

        self.quote_text.config(text=f"\"{quote['text']}\"")
        self.author_text.config(text=f"— {quote['author']}")
        self.topic_text.config(text=f"Тема: {quote['topic']}")

        self.update_history_display()

    def apply_filters(self, event=None):
        author = self.author_filter.get()
        topic = self.topic_filter.get()

        filtered_quotes = self.quotes
        if author:
            filtered_quotes = [q for q in filtered_quotes if q['author'] == author]
        if topic:
            filtered_quotes = [q for q in filtered_quotes if q['topic'] == topic]

        if filtered_quotes:
            quote = random.choice(filtered_quotes)
            self.quote_text.config(text=f"\"{quote['text']}\"")
            self.author_text.config(text=f"— {quote['author']}")
            self.topic_text.config(text=f"Тема: {quote['topic']}")
        else:
            messagebox.showinfo("Информация", "Подходящие цитаты не найдены.")

    def update_filters(self):
        authors = sorted(set(q['author'] for q in self.quotes))
        topics = sorted(set(q['topic'] for q in self.quotes))

        self.author_filter['values'] = [""] + authors
        self.topic_filter['values'] = [""] + topics

    def update_history_display(self):
        self.history_display.delete(1.0, tk.END)
        for i, quote in enumerate(self.history[-10:], 1):  # Последние 10 цитат
            self.history_display.insert(tk.END, f"{i}. \"{quote['text']}\"\n— {quote['author']} ({quote['topic']})\n\n")

    def clear_history(self):
        self.history = []
        self.update_history_display()

    def save_data(self):
        data = {
            "quotes": self.quotes,
            "history": self.history
        }
        with open("quotes_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в quotes_data.json")

    def load_data(self):
        if os.path.exists("quotes_data.json"):
            try:
                with open("quotes_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.quotes = data.get("quotes", self.quotes)
                self.history = data.get("history", [])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomQuoteGenerator(root)
    root.mainloop()
