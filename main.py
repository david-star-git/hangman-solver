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

        # Validation function
        self.validate_cmd = root.register(self.validate_number)

        # Number of fields entry
        self.num_label = ttk.Label(root, text="Enter number of fields:")
        self.num_label.grid(row=0, column=0, padx=5, pady=5)

        self.num_entry = tk.Entry(root, bg=self.widget_color, fg=self.fg_color, insertbackground='white',
                                 borderwidth=0, validate="key", validatecommand=(self.validate_cmd, '%P'))
        self.num_entry.grid(row=0, column=1, padx=5, pady=5)

        # Word list dropdown menu
        self.word_list_label = ttk.Label(root, text="Select word list:")
        self.word_list_label.grid(row=0, column=2, padx=5, pady=5)

        self.word_list_var = tk.StringVar()
        self.word_list_menu = ttk.Combobox(root, textvariable=self.word_list_var)
        self.word_list_menu['values'] = self.get_word_lists()
        self.word_list_menu.grid(row=0, column=3, padx=5, pady=5)
        self.word_list_menu.bind("<<ComboboxSelected>>", self.load_selected_word_list)

        # Generate Fields button
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

        # Frame for displaying words (replaced canvas with frame to avoid scrolling)
        self.words_frame = ttk.Frame(root)
        self.words_frame.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')

        # Pagination controls
        self.pagination_frame = ttk.Frame(root)
        self.pagination_frame.grid(row=4, column=0, columnspan=5, padx=5, pady=5)

        self.prev_button = tk.Button(self.pagination_frame, text="Previous", command=self.prev_page, state=tk.DISABLED,
                                     bg=self.widget_color, fg=self.fg_color, borderwidth=0,
                                     activebackground="#24283b", relief="flat")
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = tk.Button(self.pagination_frame, text="Next", command=self.next_page,
                                     bg=self.widget_color, fg=self.fg_color, borderwidth=0,
                                     activebackground="#24283b", relief="flat")
        self.next_button.grid(row=0, column=1, padx=5)

        # Configure column and row weights
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(5, weight=1)
        root.grid_columnconfigure(6, weight=1)
        root.grid_columnconfigure(4, weight=0)

        # Pagination settings
        self.words_per_page = 10
        self.current_page = 0

        # Load default word list if available
        self.load_default_word_list()

    def validate_number(self, new_value):
        """
        Validate if the new value is a number.

        Args:
            new_value (str): The new value to validate.

        Returns:
            bool: True if the new value is a number, otherwise False.
        """
        if new_value == "" or new_value.isdigit():
            return True
        return False

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
        Construct the current pattern based on the entries in the fields_frame.

        Returns:
            str: The pattern string with letters and '.' for empty fields.
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

    def display_words(self):
        """
        Display the words in the words_frame with pagination.
        """
        self.update_words()

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

        # Display words for the current page
        self.show_words(filtered_words)

    def show_words(self, words):
        """
        Show the filtered words with pagination.
        
        Args:
            words (list): A list of filtered words to display.
        """
        # Calculate pagination
        start_index = self.current_page * self.words_per_page
        end_index = start_index + self.words_per_page
        page_words = words[start_index:end_index]

        # Display words for the current page
        y_position = 10  # Initial vertical position
        for word in page_words:
            word_label = tk.Label(self.words_frame, text=word, bg=self.bg_color, fg=self.fg_color)
            word_label.grid(row=y_position // 25, column=0, padx=5, pady=5, sticky='w')
            y_position += 25  # Adjust vertical spacing between words

        # Update pagination buttons
        self.update_pagination_buttons(words)

    def update_pagination_buttons(self, words):
        """
        Update the state of the pagination buttons based on the current page.
        
        Args:
            words (list): The full list of words to determine the pagination state.
        """
        total_pages = (len(words) + self.words_per_page - 1) // self.words_per_page
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_page < total_pages - 1 else tk.DISABLED)

    def prev_page(self):
        """
        Go to the previous page of words.
        """
        if self.current_page > 0:
            self.current_page -= 1
            self.display_words()

    def next_page(self):
        """
        Go to the next page of words.
        """
        if self.current_page < (len(self.words) + self.words_per_page - 1) // self.words_per_page - 1:
            self.current_page += 1
            self.display_words()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanSolverApp(root)
    root.mainloop()
