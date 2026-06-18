# German Learning Telegram Bot 🇩🇪

This is a beginner-friendly Telegram bot designed to help users learn German vocabulary through a button-driven interface. The bot prioritizes `ReplyKeyboardMarkup` for navigation to ensure ease of use for beginners, with `InlineKeyboardMarkup` used for interactive exercises.

## 🛠 Tech Stack

- **Language**: Python 3.12
- **Framework**: [aiogram 3.x](https://docs.aiogram.dev/) (Asynchronous Telegram Bot API)
- **Database**: SQLite3 (Local storage)
- **Data Processing**: `pandas`
- **Environment Management**: `python-dotenv`

---

## 📁 Project Structure

```text
Telegrambot_portfolio/
├── .env                  # Environment variables (Bot Token)
├── .gitignore            # Files excluded from version control
├── bot.py                # Main entry point: Bot initialization & execution
├── config.py             # Configuration loader (loads .env)
├── database.py           # SQLite database layer (SQL queries & logic)
├── dataset_logic.py      # Logic for processing CSV word datasets
├── handlers/             # Bot logic & message handling
│   ├── common.py         # Main menu, Start, Help, & Add Word (FSM)
│   └── learning.py       # Quiz, Grammar, Learn Random Word, & exercises
├── keyboards/            # Telegram keyboard layouts
│   └── reply.py          # Main bottom-menu (ReplyKeyboardMarkup)
├── words_dataset/        # CSV files containing vocabulary lists
├── test_db.py            # Unit tests for the database layer
├── requirements.txt      # Python dependencies
└── vocab.db              # SQLite Database file (Generated at runtime)
```

---

## 📄 File Descriptions

### 1. `bot.py`

The heart of the project. It:

- Initializes the `Bot` and `Dispatcher`.
- Registers routers from the `handlers/` directory.
- Configures global logging and starts the long-polling process.

### 2. `database.py`

Handles all data persistence:

- **`init_db()`**: Creates `users` and `words` tables if they don't exist.
- **`add_word()`**: Saves a new German word and its translation for a specific user.
- **`get_words()`**: Retrieves the full vocabulary list for a user.
- **`get_random_word()`**: Fetches a random word for quiz generation.

### 3. `dataset_logic.py`

Processes the CSV files in `words_dataset/`:

- **`get_random_dataset_word()`**: Picks a random entry from any CSV.
- **`get_multiple_dataset_translations()`**: Generates distractors (wrong answers) for the Quiz.

### 4. `handlers/common.py`

Contains the core user interaction logic:

- **Command Handlers**: `/start`, `/help`, `/menu`, `/add`.
- **Button Handlers**: "Add word", "My words", "Help", etc.
- **FSM (Finite State Machine)**: Manages the "Add word" flow by putting the user in a state where the bot waits for their `word - translation` input.

### 5. `handlers/learning.py`

Manages the educational components:

- **Quiz**: Generates a dynamic question based on both the user's saved words and the CSV datasets.
- **Learn Random Word**: Displays a new word from the datasets with a "One-Click Save" option.
- **Inline Query Handlers**: Processes quiz answers and word saving requests.

### 6. `keyboards/reply.py`

Defines the `get_main_menu_keyboard()` function.

- Uses `ReplyKeyboardBuilder` to create a permanent menu at the bottom of the chat.
- Contains buttons: Add word, My words, Quiz, Learn Random Word, Daily word, Grammar practice, Mistake correction, Progress, Help, Reminder on, Reminder off.

---

## 🚀 Key Features

- **Button-First UI**: Users never _have_ to type a command.
- **Dynamic Quiz**: Quizzes pull from both your personal list and the `words_dataset` CSVs.
- **Learn Random Word**: Discover new words from external datasets with a single click.
- **One-Click Save**: Add words from the random generator directly to your personal "My Words" list.
- **Persistent Progress**: Words are saved in a local SQLite database and persist across sessions.
- **Robustness**: Includes a `test_db.py` suite to ensure data is never corrupted or lost.

---

## 🔥 Ideas for ChatGPT Innovation

_Copy-paste this section into ChatGPT to brainstorm:_

- "How can I implement a Spaced Repetition System (SRS) using the `database.py` logic?"
- "What's the best way to integrate an external Dictionary API to automatically fetch translations?"
- "How can I add an 'Audio' button to the Quiz to hear the pronunciation of the German word?"
- "Design a 'Level System' for the `Progress` button based on the number of words learned."
