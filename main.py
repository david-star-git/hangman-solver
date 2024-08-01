import tkinter as tk
from tkinter import ttk
from collections import Counter
import codecs

class HangmanSolverApp:
    def __init__(self, root):
        """
        Initialize the HangmanSolverApp with the given root Tkinter window.
        Set up the UI components and layout.
        
        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Hangman Solver App")

        self.words = self.load_words('words.txt')

        # Number of fields entry
        self.num_label = ttk.Label(root, text="Enter number of fields:")
        self.num_label.grid(row=0, column=0, padx=5, pady=5)

        self.num_entry = ttk.Entry(root)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5)

        self.generate_button = ttk.Button(root, text="Generate Fields", command=self.generate_fields)
        self.generate_button.grid(row=0, column=2, padx=5, pady=5)

        self.fields_frame = ttk.Frame(root)
        self.fields_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.words_canvas = tk.Canvas(root)
        self.words_canvas.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.words_scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.words_canvas.yview)
        self.words_scrollbar.grid(row=2, column=3, sticky='ns')

        self.words_frame = ttk.Frame(self.words_canvas)
        self.words_frame.bind(
            "<Configure>",
            lambda e: self.words_canvas.configure(
                scrollregion=self.words_canvas.bbox("all")
            )
        )

        self.words_canvas.create_window((0, 0), window=self.words_frame, anchor="nw")
        self.words_canvas.configure(yscrollcommand=self.words_scrollbar.set)

        self.exclude_label = ttk.Label(root, text="Exclude letters:")
        self.exclude_label.grid(row=0, column=4, padx=5, pady=5)

        self.exclude_entry = ttk.Entry(root)
        self.exclude_entry.grid(row=0, column=5, padx=5, pady=5)
        self.exclude_entry.bind("<KeyRelease>", self.update_words)

        self.common_label = ttk.Label(root, text="Most common letters:")
        self.common_label.grid(row=1, column=4, columnspan=2, padx=5, pady=5)

        self.common_frame = ttk.Frame(root)
        self.common_frame.grid(row=2, column=4, columnspan=2, padx=5, pady=5)

        self.word_entries = []
        self.word_labels = []

        # Enable mouse wheel scrolling
        self.words_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _on_mouse_wheel(self, event):
        """
        Handle mouse wheel scrolling for the words canvas.
        
        Args:
            event (tk.Event): The mouse wheel event containing scroll delta.
        """
        self.words_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_words(self, filename):
        """
        Load words from a given file into a list.
        
        Args:
            filename (str): The path to the file containing the words.
        
        Returns:
            list: A list of words read from the file.
        """
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            words = file.read().splitlines()
        return words

    def generate_fields(self):
        """
        Create entry fields for each letter in the word pattern based on user input.
        Clears any previous fields and updates the display with the new fields.
        """
        for widget in self.fields_frame.winfo_children():
            widget.destroy()

        try:
            num_fields = int(self.num_entry.get())
        except ValueError:
            return

        self.word_entries = []
        for i in range(num_fields):
            word_entry = ttk.Entry(self.fields_frame, width=5)
            word_entry.grid(row=0, column=i, padx=2, pady=2)
            word_entry.bind("<KeyRelease>", self.update_words)
            self.word_entries.append(word_entry)

        self.display_words()

    def get_pattern(self):
        """
        Construct the current word pattern from the entry fields.
        
        Returns:
            str: The pattern string, where each entry is represented by its current value or '.' for empty entries.
        """
        pattern = []
        for entry in self.word_entries:
            char = entry.get()
            pattern.append(char if char else '.')
        return ''.join(pattern)

    def get_excluded_letters(self):
        """
        Retrieve the letters that should be excluded from the word list.
        
        Returns:
            set: A set of excluded letters based on user input.
        """
        return set(self.exclude_entry.get())

    def filter_words(self, pattern):
        """
        Filter the list of words to match the given pattern and exclude specified letters.
        
        Args:
            pattern (str): The pattern to match against the words.
        
        Returns:
            list: A list of words that match the pattern and do not contain excluded letters.
        """
        excluded_letters = self.get_excluded_letters()
        filtered_words = []
        for word in self.words:
            if len(word) == len(pattern):
                match = True
                for i, (p, w) in enumerate(zip(pattern, word)):
                    if p != '.' and p != w:
                        match = False
                        break
                if match:
                    # Check for unique occurrences of each specified letter in the pattern
                    counts = {char: pattern.count(char) for char in pattern if char != '.'}
                    for char, count in counts.items():
                        if word.count(char) != count:
                            match = False
                            break
                if match and not any(letter in word for letter in excluded_letters):
                    filtered_words.append(word)
        return filtered_words

    def update_words(self, event=None):
        """
        Update the displayed list of words based on the current pattern and excluded letters.
        This method also updates the display of the most common letters in the filtered words.
        
        Args:
            event (tk.Event, optional): An optional event argument for key release events.
        """
        pattern = self.get_pattern()
        filtered_words = self.filter_words(pattern)

        for widget in self.words_frame.winfo_children():
            widget.destroy()

        for i, word in enumerate(filtered_words):
            word_label = ttk.Label(self.words_frame, text=word)
            word_label.grid(row=i, column=0, padx=5, pady=2)
            word_label.configure(anchor="center")

        self.update_common_letters(filtered_words)

    def update_common_letters(self, words):
        """
        Update the display of the most common letters from the filtered list of words.
        
        Args:
            words (list): A list of filtered words used to determine the most common letters.
        """
        letter_counter = Counter()
        for word in words:
            unique_letters = set(word)
            letter_counter.update(unique_letters)

        excluded_letters = self.get_excluded_letters()
        for letter in excluded_letters:
            del letter_counter[letter]

        common_letters = letter_counter.most_common(10)

        for widget in self.common_frame.winfo_children():
            widget.destroy()

        for i, (letter, count) in enumerate(common_letters):
            common_label = ttk.Label(self.common_frame, text=f"{letter}: {count}")
            common_label.grid(row=i, column=0, padx=5, pady=2)

    def display_words(self):
        self.update_words()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanSolverApp(root)
    root.mainloop()
