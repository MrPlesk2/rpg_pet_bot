from aiogram import types, F
from aiogram.fsm.context import FSMContext

from bot import dp, router
from keyboards import train_kb, train_menu_kb, menu_kb, fight_kb, get_spell_keyboard, equipment_kb

from services.user_service import UserService
from services.player_service import PlayerService
from services.spell_service import SpellService
from services.player_equipment_service import PlayerEquipmentService

from models.player_model import PlayerModel
from models.user_model import UserModel
from player import Player
from timers import timers
from figth import Fight
from equipment_page_generator import generate_page

import random
import math

@router.callback_query(F.data == "train")
async def train(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in timers:
        return
    train_obj = (await state.get_data())["train"]

    train_obj.tick()

    if train_obj.current_time_left <= 0:
        timers.pop(callback.from_user.id, None)

        player = Player(PlayerService.get_player_by_telegram_id(callback.from_user.id))

        player.raise_stat(train_obj.stat)
        await callback.message.answer(
                "Тренировка завершена ✅",
                reply_markup=train_menu_kb
            )
        await state.clear()


    await state.update_data(train = train_obj)

@router.callback_query(F.data == "attack")
async def attack(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    enemy = data["enemy"]
    player = data["player"]

    if enemy.action == "attack":
        if random.random() > player.dodje / 100:
            player.hp -= enemy.attack()
        enemy.hp -= player.attack()

    if enemy.action == "defens":
        enemy.hp -= max(0, player.attack() - enemy.defens())

    fight = Fight(enemy, player)

    if (enemy.hp <= 0):
        player.level_up()
        equipment = enemy.generate_equipment()
        if equipment is not None:
            if PlayerEquipmentService.get_equipment(player.model.id, equipment.id) is None:
                await callback.message.answer(
                    f"Вы получили предмет: {equipment.name}",
                )
                PlayerEquipmentService.add_equipment(player.model.id, equipment.id)
            else:
                await callback.message.answer(
                    f"Вы получили повторку: {equipment.name}",
                )
        


        print(equipment)

        await callback.message.edit_text(
            "Враг повержен",
        )
        await callback.message.answer(
            "Возвращаем в меню",
            reply_markup=menu_kb
        )

        return
    
    if (player.hp <= 0):
        await callback.message.edit_text(
            "Вы повержены",
        )
        await callback.message.answer(
            "Возвращаем в меню",
            reply_markup=menu_kb
        )

        return

    try:
        await callback.message.edit_text(
                fight.main_fight_message(),
                reply_markup=fight_kb
            )
    except:
        try:
            await callback.message.edit_text(
                    fight.main_fight_message_not_changed(),
                    reply_markup=fight_kb
                )
        except:
            None
    
@router.callback_query(F.data == "defens")
async def defens(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    enemy = data["enemy"]
    player = data["player"]

    if enemy.action == "attack":
        if random.random() > player.dodje / 100:
            player.hp -= max(0, enemy.attack() - player.defens())

    fight = Fight(enemy, player)

    if (enemy.hp <= 0):
        player.level_up()
        equipment = enemy.generate_equipment()
        if equipment is not None:
            if PlayerEquipmentService.get_equipment(player.model.id, equipment.id) is None:
                await callback.message.answer(
                    f"Вы получили предмет: {equipment.name}",
                )
                PlayerEquipmentService.add_equipment(player.model.id, equipment.id)
            else:
                await callback.message.answer(
                    f"Вы получили повторку: {equipment.name}",
                )

        await callback.message.edit_text(
            "Враг повержен",
        )
        await callback.message.answer(
            "Возвращаем в меню",
            reply_markup=menu_kb
        )
        
        return

    if (player.hp <= 0):
        await callback.message.edit_text(
            "Вы повержены",
        )
        await callback.message.answer(
            "Возвращаем в меню",
            reply_markup=menu_kb
        )

        return

    try:
        await callback.message.edit_text(
                fight.main_fight_message(),
                reply_markup=fight_kb
            )
    except:
        try:
            await callback.message.edit_text(
                    fight.main_fight_message_not_changed(),
                    reply_markup=fight_kb
                )
        except:
            None

@router.callback_query(F.data == "spell")
async def attack(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    enemy = data["enemy"]
    player = data["player"]

    fight = Fight(enemy, player)

    await callback.message.edit_reply_markup(
                    reply_markup=get_spell_keyboard(player)
                )

@router.callback_query(F.data == "escape")
async def attack(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Вы убежали",
    )
    await callback.message.answer(
        "Возвращаем в меню",
        reply_markup=menu_kb
    )

@router.callback_query(F.data == "spell_menu_back")
async def attack(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    enemy = data["enemy"]
    player = data["player"]

    fight = Fight(enemy, player)

    await callback.message.edit_reply_markup(
                reply_markup=fight_kb
            )

@router.callback_query(F.data == "not_enough_mana")
async def not_enough_mana(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Недостаточно маны", show_alert=True)

@router.callback_query(F.data[0:11] == "spell_cast_")
async def cast_spell(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    enemy = data["enemy"]
    player = data["player"]

    spell_tag = callback.data[11:]

    spell = SpellService.get_spell_by_tag(spell_tag)

    if enemy.action == "attack":
        if random.random() > player.dodje / 100:
            if spell_tag == "magic_shield":
                player.hp -= max(0, enemy.attack() - (spell.base_dmg + spell.mgk_pwr_coef * player.mgkpwr))
            else:
                player.hp -= max(0, enemy.attack())
        if spell_tag != "magic_shield":
            for i in range(spell.attack_num):
                enemy.hp -= max(0, spell.base_dmg + spell.mgk_pwr_coef * player.mgkpwr)
    else:
        if spell_tag != "magic_shield":
            for i in range(spell.attack_num):
                enemy.hp -= max(0, spell.base_dmg + spell.mgk_pwr_coef * player.mgkpwr)

    player.mp -= spell.manacost

    fight = Fight(enemy, player)

    if (enemy.hp <= 0):
        player.level_up()
        equipment = enemy.generate_equipment()
        if equipment is not None:
            if PlayerEquipmentService.get_equipment(player.model.id, equipment.id) is None:
                await callback.message.answer(
                    f"Вы получили предмет: {equipment.name}",
                )
                PlayerEquipmentService.add_equipment(player.model.id, equipment.id)
            else:
                await callback.message.answer(
                    f"Вы получили повторку: {equipment.name}",
                )

        await callback.message.edit_text(
            "Враг повержен",
        )
        await callback.message.answer(
            "Возвращаем в меню",
            reply_markup=menu_kb
        )
        
        return

    if (player.hp <= 0):
        await callback.message.edit_text(
            "Вы повержены",
        )
        await callback.message.answer(
            "Возвращаем в меню",
            reply_markup=menu_kb
        )

        return

    try:
        await callback.message.edit_text(
                fight.main_fight_message(),
                reply_markup=fight_kb
            )
    except:
        try:
            await callback.message.edit_text(
                    fight.main_fight_message_not_changed(),
                    reply_markup=fight_kb
                )
        except:
            None

@router.callback_query(F.data == "equipment_menu_prev_page")
async def equipment_menu_prev_page(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data["equipment_page"]

    if page - 1 >= 0:
        await state.update_data(equipment_page=page-1)

        player = PlayerService.get_player_by_telegram_id(callback.from_user.id)

        await callback.message.edit_text(
                    generate_page(page - 1, player.id),
                    reply_markup=equipment_kb
                )
        
    await callback.answer()
    
    
@router.callback_query(F.data == "equipment_menu_next_page")
async def equipment_menu_next_page(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data["equipment_page"]

    player = PlayerService.get_player_by_telegram_id(callback.from_user.id)
    equipment_len = len(PlayerEquipmentService.get_all_equipment(player.id))

    if page + 1 <= math.ceil(equipment_len / 5) - 1:
        await state.update_data(equipment_page=page+1)
        
        await callback.message.edit_text(
                    generate_page(page + 1, player.id),
                    reply_markup=equipment_kb
                )

    await callback.answer()
