# 🇩🇪 German Vocabulary Learning Bot

A beginner-friendly Telegram bot for learning German vocabulary. Designed with a **button-first UI** — no commands need to be typed manually.

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [File Reference](#file-reference)
5. [Design Principles](#design-principles)
6. [Setup & Running](#setup--running)
7. [Running Tests](#running-tests)

---

## Features

| Feature               | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| **Add word**          | FSM-driven flow to save a German ↔ Russian word pair           |
| **My words**          | List all saved words for the current user                      |
| **Quiz**              | 4-option multiple-choice from your vocabulary + dataset        |
| **Learn Random Word** | Discover a word from the built-in dataset, save with one click |
| **Progress**          | Word count statistics                                          |
| **Reminder on/off**   | Toggle daily study reminders                                   |

---

## Architecture

```
┌───────────────────────────────────────────────────────┐
│                         bot.py                        │
│   Initialises Bot, Dispatcher, DB, and all routers    │
└──────────────┬────────────────────┬───────────────────┘
               │                    │
   ┌───────────▼──────────┐ ┌───────▼──────────────────┐
   │  handlers/common.py  │ │  handlers/learning.py     │
   │  /start, /help,      │ │  /quiz, Learn Random Word │
   │  /add (FSM),         │ │  Inline callback handlers │
   │  /words, /progress,  │ │                           │
   │  /reminder_on/off    │ └───────────────────────────┘
   └───────────┬──────────┘
               │
   ┌───────────▼──────────────────────────────────────┐
   │                    database.py                   │
   │   SQLite via context manager (DRY, safe close)   │
   └──────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────┐
   │                 dataset_logic.py                 │
   │   Loads all CSVs once at import time (cached).   │
   │   Provides random words and distractor options.  │
   └──────────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────────┐
   │               keyboards/reply.py                │
   │   ReplyKeyboardMarkup — permanent bottom menu    │
   └──────────────────────────────────────────────────┘
```

---

## Project Structure

```
Telegrambot_portfolio/
├── .env                     # BOT_TOKEN (never commit this)
├── .gitignore
├── bot.py                   # Entry point
├── config.py                # Env loading + validation
├── database.py              # SQLite data access layer
├── dataset_logic.py         # CSV vocabulary dataset loader
├── handlers/
│   ├── __init__.py
│   ├── common.py            # Core menu handlers + FSM
│   └── learning.py          # Quiz & random word handlers
├── keyboards/
│   ├── __init__.py
│   └── reply.py             # Main menu ReplyKeyboardMarkup
├── words_dataset/
│   ├── adjectives.csv
│   ├── nouns.csv
│   ├── verbs.csv
│   └── others.csv
├── test_db.py               # Unit tests (database layer)
├── requirements.txt
└── vocab.db                 # Generated at runtime
```

---

## File Reference

### `bot.py`

Entry point. Configures global logging at **module level** (not inside `main()`), initialises the database once, registers all routers, and starts long-polling.

### `config.py`

Loads `.env` via `python-dotenv` and exposes `BOT_TOKEN`. Exits with a clear error message if the token is missing — fail-fast at startup rather than crashing later.

### `database.py`

Pure data-access layer. Uses a `@contextmanager` (`get_connection`) so every function opens and closes its own connection without repeating `conn.close()` boilerplate.  
Public API:

- `init_db()` — Create tables if they don't exist.
- `add_word(user_id, word, translation)` — Insert a word pair.
- `get_words(user_id) → list[tuple]` — Return all pairs for a user.
- `get_random_word(user_id) → tuple | None` — Return one random pair.

### `dataset_logic.py`

Loads and merges all CSV files in `words_dataset/` **once at import time** into a module-level `_DATASET` DataFrame. All subsequent calls read from memory — no disk I/O on each message. Malformed lines are silently skipped (`on_bad_lines='skip'`).  
Public API:

- `get_random_dataset_word() → (de, ru) | None`
- `get_multiple_dataset_translations(count, exclude) → list[str]`

### `handlers/common.py`

Handles all non-learning interactions. Uses aiogram's **FSM** (`StatesGroup`) for the multi-step "Add word" flow. Every handler responds to both its `/command` and the matching button text.

### `handlers/learning.py`

Handles the Quiz and Random Word features. Uses `|` as the callback data separator (safe — never appears in German/Russian text) to avoid `BUTTON_DATA_INVALID` errors from Telegram's 64-byte limit.

### `keyboards/reply.py`

Defines the permanent `ReplyKeyboardMarkup`. Call `get_main_menu_keyboard()` to get the markup object to pass to `reply_markup=`.

---

## Design Principles

### SOLID Applied

| Principle                     | How it's applied                                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **S** — Single Responsibility | `database.py` only does SQL. `dataset_logic.py` only reads CSVs. Handlers only handle messages.                           |
| **O** — Open/Closed           | New features are added as new handlers/routers, not by modifying existing ones.                                           |
| **D** — Dependency Inversion  | Handlers depend on the `database` and `dataset_logic` modules (stable abstractions), not on concrete DB drivers directly. |

### Other patterns

- **DRY**: The `get_connection()` context manager eliminates repeated connection-management code in `database.py`.
- **Fail-Fast**: `config.py` validates `BOT_TOKEN` at startup and exits immediately if it is missing.
- **Module-level caching**: `dataset_logic._DATASET` is loaded once, not on every user interaction — avoids repeated file I/O.
- **Safe separator**: Callback data uses `|` instead of `_` or `:` to prevent accidental data corruption when word strings contain those characters.

---

## Setup & Running

### 1. Clone and create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure your bot token

```bash
# Edit .env and replace the placeholder with your real token from @BotFather
echo "BOT_TOKEN=your_token_here" > .env
```

### 3. Run the bot

```bash
python bot.py
```

---

## Running Tests

```bash
source .venv/bin/activate
python test_db.py
```

Three tests validate the database layer:

- `test_add_and_get_words` — Words saved are returned correctly.
- `test_get_random_word` — Random word retrieval works.
- `test_empty_words` — Correct behaviour for a user with no words.
# LanguageLearnbot
