# Hangman Solver App

## Overview

The Hangman Solver App is a Tkinter-based GUI application designed to help users solve Hangman puzzles. The app allows users to input the number of letters in the word, specify known letters and excluded letters, and then displays possible word matches from a provided word list. Additionally, it shows the most common letters in the filtered word list to assist users in guessing the word.

## Features

- Input the number of letters in the word.
- Dynamically generate entry fields for each letter.
- Enter known letters and excluded letters.
- View a list of possible words that match the pattern.
- Display the most common letters from the filtered list of possible words.

## Requirements

- Python 3.x
- Tkinter (included with Python)

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/david-star-git/hangman-solver.git
    cd hangman-solver
    ```

2. **Download Word Lists**:
   - You can download word lists from the [GitHub repository's `wordLists` folder](https://github.com/david-star-git/hangman-solver/tree/main/wordLists).
   - Place your word list files in the `wordLists` directory. Each word list file should be a plain text file (`.txt`) with one word per line.

3. **Run the Application**:
    ```bash
    python main.py
    ```

## Usage

1. **Enter the Number of Fields**:
   - Input the number of letters in the Hangman word in the "Enter number of fields" entry box.

2. **Select Word List**:
   - Use the dropdown menu to select the word list file you want to use (you can change this later). The app will load words from the selected file.

3. **Generate Fields**:
   - Click the "Generate Fields" button to create entry fields corresponding to the number of letters in the word.

4. **Input Known Letters**:
   - Enter known letters in the generated fields. Use `.` (dot) for unknown letters.

5. **Exclude Letters**:
   - Enter letters to exclude from the list of possible words in the "Exclude letters" entry box.

6. **View Possible Words**:
   - The app will display a list of words that match the given pattern and exclude the specified letters.

7. **Most Common Letters**:
   - View the most common letters in the filtered list of possible words.

## Code Structure

- `HangmanSolverApp` class: Main application class that handles the UI and logic.
  - `__init__(self, root)`: Initializes the application and sets up the UI.
  - `_on_mouse_wheel(self, event)`: Handles mouse wheel scrolling for the word list canvas.
  - `load_words(self, filename)`: Loads words from a file into a list.
  - `generate_fields(self)`: Creates and displays entry fields based on user input.
  - `get_pattern(self)`: Retrieves the current word pattern from the entry fields.
  - `get_excluded_letters(self)`: Retrieves the set of excluded letters.
  - `filter_words(self, pattern)`: Filters the list of words based on the pattern and excluded letters.
  - `update_words(self, event=None)`: Updates the displayed list of words and common letters.
  - `update_common_letters(self, words)`: Updates the display of the most common letters from the filtered words.
  - `display_words(self)`: Refreshes the list of displayed words.

## Contributing

Feel free to submit issues, suggestions, or pull requests to improve the app.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
