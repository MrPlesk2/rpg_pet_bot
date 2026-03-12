from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from player import Player
from services.player_service import PlayerService


contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Поделиться контактом", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Тренировка")],
        [KeyboardButton(text="Экипировка")],
        [KeyboardButton(text="В бой!")]
    ],
    resize_keyboard=True,
)

train_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Статистика")],
        
        [
            KeyboardButton(text="Тренировать здоровье"),
            KeyboardButton(text="Тренировать ману")
        ],
        [
            KeyboardButton(text="Тренировать атаку"),
            KeyboardButton(text="Тренировать защиту")
        ],
        [
            KeyboardButton(text="Тренировать увороты"),
            KeyboardButton(text="Тренировать магическую силу")
        ],

        [KeyboardButton(text="Главное меню")]
    ],
    resize_keyboard=True,
)

train_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ускорить тренировку", callback_data="train")]
    ],
)

fight_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Атаковать", callback_data="attack")],
        [InlineKeyboardButton(text="Защищаться", callback_data="defens")],
        [InlineKeyboardButton(text="Заклинания", callback_data="spell")],
        [InlineKeyboardButton(text="Бежать", callback_data="escape")],
    ],
)

equipment_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="←", callback_data="equipment_menu_prev_page"),
         InlineKeyboardButton(text="→", callback_data="equipment_menu_next_page")],
    ],
)

def get_spell_keyboard(player: Player):
    inline_keyboard=[]

    for spell in PlayerService.get_player_spell_list(player.model.id):
        inline_keyboard.append([InlineKeyboardButton(text=f"{spell.name} {spell.manacost} маны", \
                                                     callback_data=f"spell_cast_{spell.tag}" if spell.manacost <= player.mp \
                                                     else "not_enough_mana")])

    if False:
        inline_keyboard.append([InlineKeyboardButton(text="←", callback_data="spell_menu_prev_page"), 
                                InlineKeyboardButton(text="→", callback_data="spell_menu_next_page")])

    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="spell_menu_back")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)