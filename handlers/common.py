from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import get_main_menu_keyboard
import database

router = Router()

class WordStates(StatesGroup):
    waiting_for_word = State()

@router.message(CommandStart())
@router.message(Command("menu"))
@router.message(F.text == "Main menu")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Welcome to your German Learning Bot! 🇩🇪\n"
        "Use the buttons below to navigate.",
        reply_markup=get_main_menu_keyboard()
    )

@router.message(Command("help"))
@router.message(F.text == "Help")
async def cmd_help(message: Message):
    await message.answer(
        "This bot helps you learn German.\n\n"
        "Available buttons:\n"
        "- Add word: Add a new word to your vocabulary\n"
        "- My words: View your full word list\n"
        "- Quiz: Test yourself on saved words and dataset words\n"
        "- Learn Random Word: Discover a new word and save it with one click\n"
        "- Progress: See how many words you have saved\n"
        "- Reminder on/off: Toggle daily study reminders"
    )

@router.message(Command("add"))
@router.message(F.text == "Add word")
async def cmd_add(message: Message, state: FSMContext):
    await state.set_state(WordStates.waiting_for_word)
    await message.answer("To add a word, please send it in the format: word - translation")

@router.message(WordStates.waiting_for_word)
async def process_word_addition(message: Message, state: FSMContext):
    if " - " in message.text:
        parts = message.text.split(" - ", 1)
        word = parts[0].strip()
        translation = parts[1].strip()
        database.add_word(message.from_user.id, word, translation)
        await message.answer(f"✅ Saved: {word} -> {translation}")
        await state.clear()
    else:
        await message.answer("⚠️ Invalid format. Please use: word - translation\nExample: Apfel - Apple")

@router.message(Command("words"))
@router.message(F.text == "My words")
async def cmd_words(message: Message):
    words = database.get_words(message.from_user.id)
    if not words:
        await message.answer("Your word list is empty. Click 'Add word' to start!")
        return
    
    response = "📚 Your saved words:\n\n"
    for w, t in words:
        response += f"• {w} - {t}\n"
    await message.answer(response)

@router.message(Command("progress"))
@router.message(F.text == "Progress")
async def cmd_progress(message: Message):
    words = database.get_words(message.from_user.id)
    count = len(words)
    await message.answer(f"📊 Your stats:\nWords saved: {count}\nKeep learning!")

@router.message(Command("reminder_on"))
@router.message(F.text == "Reminder on")
async def cmd_reminder_on(message: Message):
    await message.answer("Daily reminders are now ON! 🔔")

@router.message(Command("reminder_off"))
@router.message(F.text == "Reminder off")
async def cmd_reminder_off(message: Message):
    await message.answer("Daily reminders are now OFF. 🔕")
