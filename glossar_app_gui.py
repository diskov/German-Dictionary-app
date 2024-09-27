import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import random


class Dictionary:
    def __init__(self, file_name='dictionary.json'):
        self.file_name = file_name
        self.word_pairs = {}
        self.load_dictionary()

    def load_dictionary(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r', encoding='utf-8') as file:
                self.word_pairs = json.load(file)
        else:
            self.word_pairs = {}

    def save_dictionary(self):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(self.word_pairs, file, ensure_ascii=False, indent=4)

    def add_word_pair(self, german_word, greek_translation):
        self.word_pairs[german_word] = greek_translation
        self.save_dictionary()

    def get_random_word(self):
        if not self.word_pairs:
            return None
        return random.choice(list(self.word_pairs.keys()))

    def get_translation(self, german_word):
        return self.word_pairs.get(german_word)

    def update_word_pair(self, german_word, new_translation):
        if german_word in self.word_pairs:
            self.word_pairs[german_word] = new_translation
            self.save_dictionary()
            return True
        else:
            return False

    def word_exists(self, german_word):
        return german_word in self.word_pairs


class DictionaryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("German-Greek Dictionary")
        self.dictionary = Dictionary()
        self.current_word = None

        # Setting up the GUI components
        self.setup_gui()

    def setup_gui(self):
        # Menu Bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=file_menu)
        file_menu.add_command(label="Add Word Pair", command=self.add_word_pair)
        file_menu.add_command(label="Update Word Pair", command=self.update_word_pair)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Main Frame
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        # Quiz Components
        self.word_label = tk.Label(self.frame, text="Click 'Start Quiz' to begin", font=('Helvetica', 16))
        self.word_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.frame, font=('Helvetica', 14))
        self.answer_entry.pack(pady=5)

        self.check_button = tk.Button(self.frame, text="Check Answer", command=self.check_answer, state='disabled')
        self.check_button.pack(pady=5)

        # Start Quiz Button
        self.start_button = tk.Button(self.frame, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack(pady=10)

    def add_word_pair(self):
        german_word = simpledialog.askstring("Add Word Pair", "Enter the German word:")
        if german_word:
            greek_translation = simpledialog.askstring("Add Word Pair", f"Enter the Greek translation for '{german_word}':")
            if greek_translation:
                self.dictionary.add_word_pair(german_word.strip(), greek_translation.strip())
                messagebox.showinfo("Success", f"Added: {german_word} - {greek_translation}")
            else:
                messagebox.showwarning("Input Error", "Greek translation cannot be empty.")
        else:
            messagebox.showwarning("Input Error", "German word cannot be empty.")

    def update_word_pair(self):
        german_word = simpledialog.askstring("Update Word Pair", "Enter the German word to update:")
        if german_word:
            if self.dictionary.word_exists(german_word.strip()):
                new_translation = simpledialog.askstring("Update Word Pair", f"Enter the new Greek translation for '{german_word}':")
                if new_translation:
                    self.dictionary.update_word_pair(german_word.strip(), new_translation.strip())
                    messagebox.showinfo("Success", f"Updated: {german_word} - {new_translation}")
                else:
                    messagebox.showwarning("Input Error", "Greek translation cannot be empty.")
            else:
                messagebox.showwarning("Not Found", f"The word '{german_word}' does not exist in the dictionary.")
        else:
            messagebox.showwarning("Input Error", "German word cannot be empty.")

    def start_quiz(self):
        self.current_word = self.dictionary.get_random_word()
        if self.current_word:
            self.word_label.config(text=f"Translate this German word: {self.current_word}")
            self.answer_entry.delete(0, tk.END)
            self.check_button.config(state='normal')
            self.start_button.config(state='disabled')
        else:
            messagebox.showinfo("Dictionary Empty", "The dictionary is empty. Please add some words first.")

    def check_answer(self):
        user_answer = self.answer_entry.get().strip()
        correct_answer = self.dictionary.get_translation(self.current_word)
        if user_answer.lower() == correct_answer.lower():
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showinfo("Incorrect", f"The correct translation is: {correct_answer}")
        self.reset_quiz()

    def reset_quiz(self):
        self.current_word = None
        self.word_label.config(text="Click 'Start Quiz' to begin")
        self.answer_entry.delete(0, tk.END)
        self.check_button.config(state='disabled')
        self.start_button.config(state='normal')


def main():
    root = tk.Tk()
    app = DictionaryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
