from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
import database
import random
import dataset_logic

router = Router()

# Telegram callback_data hard limit is 64 bytes.
_CB_WORD_LEN = 15
_CB_TRANS_LEN = 20


@router.message(Command("quiz"))
@router.message(F.text == "Quiz")
async def cmd_quiz(message: Message, state: FSMContext):
    # Load recently seen words for this user to avoid repeats
    data = await state.get_data()
    seen: list[str] = data.get("quiz_seen", [])

    # Prefer dataset; only fall back to user's saved words if dataset is empty
    word_data = dataset_logic.get_random_dataset_word(exclude_words=seen)
    if not word_data:
        word_data = database.get_random_word(message.from_user.id)

    if not word_data:
        await message.answer(
            "Add at least one word first, or make sure the dataset files are present."
        )
        return

    word, correct_translation = word_data

    # Track last 50 seen words; reset when full to avoid indefinite exclusion
    seen.append(word)
    if len(seen) > 50:
        seen = seen[-50:]
    await state.update_data(quiz_seen=seen)

    wrong_options = dataset_logic.get_multiple_dataset_translations(
        count=3, exclude=correct_translation
    )

    options = [correct_translation] + wrong_options
    random.shuffle(options)

    w_trunc = word[:_CB_WORD_LEN]
    t_trunc = correct_translation[:_CB_TRANS_LEN]

    buttons = [
        [InlineKeyboardButton(
            text=str(opt),
            callback_data="quiz_ok" if str(opt) == str(correct_translation)
                          else f"qwr|{w_trunc}|{t_trunc}"
        )]
        for opt in options
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(f"What is the translation for: **{word}**?", reply_markup=keyboard)


@router.message(F.text == "Learn Random Word")
async def cmd_random_word(message: Message):
    word_data = dataset_logic.get_random_dataset_word()
    if not word_data:
        await message.answer("Sorry, couldn't find a random word right now.")
        return

    word_de, word_ru = word_data
    # Use | as separator — safe because it never appears in Russian or German words
    cb = f"sv|{word_de[:_CB_WORD_LEN]}|{word_ru[:_CB_TRANS_LEN]}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Add to My Words", callback_data=cb)]
    ])
    await message.answer(
        f"🆕 Random Word:\n\n🇩🇪 **{word_de}**\n🇷🇺 {word_ru}",
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith("sv|"))
async def save_random_word(callback: CallbackQuery):
    parts = callback.data.split("|")
    if len(parts) == 3:
        _, word, translation = parts
        database.add_word(callback.from_user.id, word, translation)
        await callback.message.edit_text(f"✅ Saved to your list:\n**{word}** — {translation}")
    else:
        await callback.message.edit_text("⚠️ Could not save — data was malformed.")
    await callback.answer()


@router.callback_query(F.data == "quiz_ok")
async def quiz_correct(callback: CallbackQuery):
    await callback.message.edit_text("✅ Correct! Well done!")
    await callback.answer()


@router.callback_query(F.data.startswith("qwr|"))
async def quiz_wrong(callback: CallbackQuery):
    parts = callback.data.split("|")
    if len(parts) == 3:
        _, word_de, correct_ans = parts
        await callback.message.edit_text(
            f"❌ Wrong. **{word_de}** in Russian is: **{correct_ans}**"
        )
    else:
        await callback.message.edit_text("❌ Wrong. Try again!")
    await callback.answer()
