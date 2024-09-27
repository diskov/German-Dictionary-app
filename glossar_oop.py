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

    def update_word_pair(self, german_word, new_translation):
        if german_word in self.word_pairs:
            self.word_pairs[german_word] = new_translation
            self.save_dictionary()
            return True
        else:
            return False

    def get_random_word(self):
        if not self.word_pairs:
            return None
        return random.choice(list(self.word_pairs.keys()))

    def get_translation(self, german_word):
        return self.word_pairs.get(german_word)

class DictionaryApp:
    def __init__(self):
        self.dictionary = Dictionary()

    def run(self):
        while True:
            self.display_menu()
            choice = input("Select an option (1-3): ").strip()
            self.handle_choice(choice)

    def display_menu(self):
        print("\n--- German-Greek Dictionary Program ---")
        print("1. Add a new word pair")
        print("2. Quiz me")
        print("3. Update a word pair")
        print("4. Exit")

    def handle_choice(self, choice):
        if choice == '1':
            self.add_word_pair()
        elif choice == '2':
            self.quiz()
        elif choice == '3':
            self.update_word_pair()
        elif choice == '4':
            print("Goodbye!")
            exit()
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

    def add_word_pair(self):
        german_word = input("Enter the German word: ").strip()
        greek_translation = input("Enter the Greek translation: ").strip()
        if german_word and greek_translation:
            self.dictionary.add_word_pair(german_word, greek_translation)
            print(f"Added: {german_word} - {greek_translation}")
        else:
            print("Both fields are required.")

    def update_word_pair(self):
        german_word = input("Enter the German word you want to update: ").strip()
        if self.dictionary.word_exists(german_word):
            new_translation = input("Enter the new Greek translation: ").strip()
            if new_translation:
                self.dictionary.update_word_pair(german_word, new_translation)
                print(f"Updated: {german_word} - {new_translation}")
            else:
                print("Translation cannot be empty.")
        else:
            print(f"The word '{german_word}' does not exist in the dictionary.")

    def quiz(self):
        german_word = self.dictionary.get_random_word()
        if not german_word:
            print("The dictionary is empty. Please add some words first.")
            return
        print(f"Translate this German word: {german_word}")
        user_answer = input("Your translation: ").strip()
        correct_answer = self.dictionary.get_translation(german_word)
        if user_answer.lower() == correct_answer.lower():
            print("Correct!")
        else:
            print(f"Incorrect. The correct translation is: {correct_answer}")
    # TODO --> check the following implementation for choice of language to be tested on
    # def quiz(self):
    #     if not self.dictionary.word_pairs:
    #         print("The dictionary is empty. Please add some words first.")
    #         return

    #     language = input("Which language do you want to be quizzed in (e.g., Greek, English)? ").strip()
    #     german_word = self.dictionary.get_random_word()
    #     if not german_word:
    #         print("No words available for the selected language.")
    #         return
    #     print(f"Translate this German word into {language}: {german_word}")
    #     user_answer = input("Your translation: ").strip()
    #     correct_answer = self.dictionary.get_translation(german_word).get(language)
    #     if not correct_answer:
    #         print(f"No translation available for {language}.")
    #         return
    #     if user_answer.lower() == correct_answer.lower():
    #         print("Correct!")
    #     else:
    #         print(f"Incorrect. The correct translation is: {correct_answer}")


def main():
    app = DictionaryApp()
    app.run()

if __name__ == "__main__":
    main()
