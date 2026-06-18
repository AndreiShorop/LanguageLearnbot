from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    buttons = [
        "Add word", "My words",
        "Quiz", "Learn Random Word",
        "Progress", "Help",
        "Reminder on", "Reminder off"
    ]
    
    for button in buttons:
        builder.add(KeyboardButton(text=button))
    
    # Adjusting the layout: 2 columns mostly, except for wider ones if needed.
    # .adjust(2) means 2 buttons per row.
    builder.adjust(2)
    
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Select an option from the menu"
    )
