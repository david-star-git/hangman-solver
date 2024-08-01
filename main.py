import tkinter as tk
from tkinter import ttk
from collections import Counter
import codecs
import os

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

        # Disable window resizing
        self.root.resizable(False, False)

        # Color configuration
        self.bg_color = "#24283b"  # Background color
        self.fg_color = "#7dcfff"  # Foreground color
        self.widget_color = "#1a1b26"  # Widget color

        # Set up UI components with colors
        self.root.configure(bg=self.bg_color)

        # Set up styles for ttk widgets
        self.style = ttk.Style()
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TButton', background=self.widget_color, foreground=self.fg_color)
        self.style.map('TButton',
                       background=[('pressed', '#24283b'), ('active', '#1a1b26')],
                       foreground=[('pressed', 'white'), ('active', self.fg_color)])

        self.word_list_dir = 'wordLists'  # Directory containing word list files
        self.words = []  # List to hold words from the selected word list

        # Initialize word_entries as an empty list for entry widgets
        self.word_entries = []

        # Number of fields entry
        self.num_label = ttk.Label(root, text="Enter number of fields:")
        self.num_label.grid(row=0, column=0, padx=5, pady=5)

        self.num_entry = tk.Entry(root, bg=self.widget_color, fg=self.fg_color, insertbackground='white', borderwidth=0)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5)

        # Word list dropdown menu
        self.word_list_label = ttk.Label(root, text="Select word list:")
        self.word_list_label.grid(row=0, column=2, padx=5, pady=5)

        self.word_list_var = tk.StringVar()
        self.word_list_menu = ttk.Combobox(root, textvariable=self.word_list_var)
        self.word_list_menu['values'] = self.get_word_lists()
        self.word_list_menu.grid(row=0, column=3, padx=5, pady=5)
        self.word_list_menu.bind("<<ComboboxSelected>>", self.load_selected_word_list)

        self.generate_button = tk.Button(root, text="Generate Fields", command=self.generate_fields, 
                                        bg=self.widget_color, fg=self.fg_color, borderwidth=0, 
                                        activebackground="#24283b", relief="flat")
        self.generate_button.grid(row=0, column=4, padx=5, pady=5)

        # Frame for entry fields
        self.fields_frame = ttk.Frame(root)
        self.fields_frame.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

        # Exclude letters section
        self.exclude_label = ttk.Label(root, text="Exclude letters:")
        self.exclude_label.grid(row=1, column=5, padx=5, pady=5, sticky='w')

        self.exclude_entry = tk.Entry(root, bg=self.widget_color, fg=self.fg_color, insertbackground='white', borderwidth=0)
        self.exclude_entry.grid(row=1, column=6, padx=5, pady=5, sticky='w')
        self.exclude_entry.bind("<KeyRelease>", self.update_words)

        # Most common letters section
        self.common_label = ttk.Label(root, text="Most common letters:")
        self.common_label.grid(row=2, column=5, padx=5, pady=(0, 5), sticky='w')

        self.common_frame = ttk.Frame(root)
        self.common_frame.grid(row=3, column=5, padx=5, pady=5, sticky='n')

        # Scrollable canvas for displaying words
        self.words_canvas = tk.Canvas(root, background=self.bg_color, bd=0, highlightthickness=0)
        self.words_canvas.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')

        self.words_scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.words_canvas.yview)
        self.words_scrollbar.grid(row=3, column=4, sticky='ns', padx=5, pady=5)

        self.words_frame = ttk.Frame(self.words_canvas, style='TFrame')
        self.words_frame.bind(
            "<Configure>",
            lambda e: self.words_canvas.configure(
                scrollregion=self.words_canvas.bbox("all")
            )
        )

        self.words_canvas.create_window((0, 0), window=self.words_frame, anchor="nw")
        self.words_canvas.configure(yscrollcommand=self.words_scrollbar.set)

        # Configure column and row weights
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(5, weight=1)
        root.grid_columnconfigure(6, weight=1)
        root.grid_columnconfigure(4, weight=0)

        # Enable mouse wheel scrolling
        self.words_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        # Load default word list if available
        self.load_default_word_list()

    def _on_mouse_wheel(self, event):
        """
        Handle mouse wheel scrolling for the words canvas.
        
        Args:
            event (tk.Event): The mouse wheel event containing scroll delta.
        """
        self.words_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def get_word_lists(self):
        """
        Retrieve a list of word list files from the word list directory.
        
        Returns:
            list: A list of word list filenames with a '.txt' extension.
        """
        return sorted([f for f in os.listdir(self.word_list_dir) if f.endswith('.txt')])

    def load_selected_word_list(self, event):
        """
        Load words from the selected word list file and display them.

        Args:
            event (tk.Event): The event triggered by selecting a word list from the dropdown menu.
        """
        selected_file = self.word_list_var.get()
        if not selected_file:
            # No selection, so default to the first file alphabetically
            word_lists = self.get_word_lists()
            if word_lists:
                selected_file = word_lists[0]
                self.word_list_var.set(selected_file)
        file_path = os.path.join(self.word_list_dir, selected_file)
        self.words = self.load_words(file_path)
        self.display_words()

    def load_default_word_list(self):
        """
        Load the default word list if available when the application starts.
        """
        word_lists = self.get_word_lists()
        if word_lists:
            default_file = word_lists[0]
            self.word_list_var.set(default_file)
            self.load_selected_word_list(None)

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
            word_entry = tk.Entry(self.fields_frame, width=5, bg=self.widget_color, fg=self.fg_color, insertbackground='white', borderwidth=0)
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

        # Clear previous word display
        for widget in self.words_frame.winfo_children():
            widget.destroy()

        # Display filtered words
        for i, word in enumerate(filtered_words):
            word_label = tk.Label(self.words_frame, text=word, bg=self.bg_color, fg=self.fg_color)
            word_label.grid(row=i, column=0, padx=5, pady=2)
            word_label.configure(anchor="center")

        # Update most common letters display
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

        # Clear previous common letters display
        for widget in self.common_frame.winfo_children():
            widget.destroy()

        # Display most common letters
        for i, (letter, count) in enumerate(common_letters):
            common_label = tk.Label(self.common_frame, text=f"{letter}: {count}", bg=self.bg_color, fg=self.fg_color)
            common_label.grid(row=i, column=0, padx=5, pady=2)

    def display_words(self):
        self.update_words()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanSolverApp(root)
    root.mainloop()
