from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import asyncio

from keyboards import contact_kb, menu_kb, train_menu_kb, train_kb, fight_kb, equipment_kb
from bot import dp, router
from train import Train
from timers import timers
from player import Player
from timer import training_timer
from enemy import Enemy
from figth import Fight
from equipment_page_generator import generate_page

from services.user_service import UserService
from services.player_service import PlayerService
from services.spell_service import SpellService
from services.player_equipment_service import PlayerEquipmentService
from services.equipment_service import EquipmentService

@router.message(Command("start"))
async def start(message: types.Message):
    user = UserService.get_user(message.from_user.id)
    if user:
        await message.answer(
            "Давно вас не было в уличных гонках!",
            reply_markup=menu_kb
        )
    else:
        await message.answer(
            "Для регистрации нажмите кнопку ниже 👇",
            reply_markup=contact_kb
        )

@router.message(F.contact)
async def get_contact(message: types.Message):
    contact = message.contact

    user_data = {
        "telegram_id": message.from_user.id,
        "name": message.from_user.full_name,
        "username": message.from_user.username,
        "phone": contact.phone_number
    }
    UserService.get_or_create_user(user_data)
    print(user_data)

    await message.answer(
        "Вы зарегистрированы!",
        reply_markup=menu_kb
    )

@router.message(F.text == "Главное меню")
async def main_menu(message: types.Message):
    await message.answer(
            text = "Вот главное меню",
            reply_markup=menu_kb
        )


@router.message(F.text == "Тренировка")
async def train_menu(message: types.Message):
    player = PlayerService.get_player_by_telegram_id(message.from_user.id)

    answer = f"Максимальное здоровье: {player.maxHp}\nМаксимальная мана: {player.maxMp}\n" \
             f"Атака: {player.attack}\nЗащита: {player.defens}\n" \
             f"Уворот: {player.dodje}\nМагическая сила: {player.mgkpwr}\n"

    await message.answer(
            text = answer,
            reply_markup=train_menu_kb
        )
    
@router.message(F.text == "Экипировка")
async def train_menu(message: types.Message, state: FSMContext):

    await state.update_data(equipment_page=0)

    player = PlayerService.get_player_by_telegram_id(message.from_user.id)

    message = await message.answer(
            text = generate_page(0, player.id),
            reply_markup=equipment_kb
        )
    await state.update_data(equipment_menu_message=message)
    
@router.message(F.text == "В бой!")
async def start_figth(message: types.Message, state: FSMContext):
    player = Player(PlayerService.get_player_by_telegram_id(message.from_user.id))
    enemy = Enemy(player.model.level)
    fight = Fight(enemy, player)

    await state.update_data(enemy=enemy, player=player, spell_page=0)

    await message.answer(
            "Бой начинается",
            reply_markup=ReplyKeyboardRemove()
        )

    await message.answer(
            fight.main_fight_message(),
            reply_markup=fight_kb
        )

@router.message(F.text == "Статистика")
async def stats(message: types.Message):
    player = PlayerService.get_player_by_telegram_id(message.from_user.id)

    answer = f"Ваш уровень: {player.level}\n" + \
             f"Максимальное здоровье: {player.maxHp}\nМаксимальная мана: {player.maxMp}\n" \
             f"Атака: {player.attack}\nЗащита: {player.defens}\n" \
             f"Уворот: {player.dodje}\nМагическая сила: {player.mgkpwr}\n"
    
    await message.answer(
            text = answer,
        )
    
@router.message(F.text.startswith("Тренировать"))
async def train(message: types.Message, state: FSMContext):
    text = message.text.split(" ")
    if len(text) > 3:
        await message.answer(
            text = "Ты отправил что-то не то"
        )
        return
    user = UserService.get_user(message.from_user.id)
    stat = PlayerService.get_stat(user.id, text[1] if len(text) == 2 else text[1] + " " + text[2])

    train_obj = Train(text[1] if len(text) == 2 else text[1] + " " + text[2], stat)

    await state.update_data(train = train_obj)

    await message.answer(
            "Начинаем тренировку",
            reply_markup=ReplyKeyboardRemove()
        )

    sent_message = await message.answer(
            f"Тренировка...\nОсталось: {train_obj.duration} сек",
            reply_markup=train_kb
        )
    
    task = asyncio.create_task(
        training_timer(user.telegram_id, sent_message, state)
    )

    timers[user.telegram_id] = task

@router.message(F.text.startswith("/equipment_stat_"))
async def equip(message: types.Message):
    equipment_id = int(message.text.split("_")[2])
    equipment = EquipmentService.get_equipment(equipment_id)

    await message.answer(
        f"{equipment.name}:\n" + \
        f"Максимальное здоровье: {10 * equipment.maxHp}\n" + \
        f"Максимальная мана: {10 * equipment.maxMp}\n" + \
        f"Атака: {equipment.attack}\n" + \
        f"Защита: {equipment.defens}\n" + \
        f"Уворот: {equipment.dodje}\n" + \
        f"Магическая сила: {equipment.mgkpwr}"
    )

@router.message(F.text.startswith("/equip_"))
async def equip(message: types.Message, state: FSMContext):
    equipment_id = int(message.text.split("_")[1])
    player = PlayerService.get_player_by_telegram_id(message.from_user.id)
    result = PlayerEquipmentService.equip(player.id, equipment_id)
    if result:
        data = await state.get_data()
        message = data["equipment_menu_message"]
        page = data["equipment_page"]
        await message.edit_text(
            generate_page(page, player.id),
            reply_markup=equipment_kb
        )
    else:
        await message.answer("Уже надето")

@router.message(F.text.startswith("/unequip_"))
async def equip(message: types.Message, state: FSMContext):
    equipment_id = int(message.text.split("_")[1])
    player = PlayerService.get_player_by_telegram_id(message.from_user.id)
    PlayerEquipmentService.unequip(player.id, equipment_id)

    data = await state.get_data()
    message = data["equipment_menu_message"]
    page = data["equipment_page"]
    await message.edit_text(
        generate_page(page, player.id),
        reply_markup=equipment_kb
    )
