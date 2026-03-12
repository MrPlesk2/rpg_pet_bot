import asyncio
from aiogram.fsm.context import FSMContext
from keyboards import train_kb, train_menu_kb
from timers import timers
from services.player_service import PlayerService
from player import Player

async def training_timer(user_id, message, state: FSMContext):
    while True:
        await asyncio.sleep(1)
        data = await state.get_data()
        train = data["train"]

        time_left = train.current_time_left

        if time_left <= 0:
            await message.answer(
                "Тренировка завершена ✅",
                reply_markup=train_menu_kb
            )

            player = Player(PlayerService.get_player_by_telegram_id(user_id))

            player.raise_stat(data["train"].stat)

            await state.clear()
            timers.pop(user_id, None)
            break

        
        train.tick()
        time_left -= 1

        await state.update_data(train = train)

        await message.edit_text(
            f"Тренировка...\nОсталось: {time_left} сек",
            reply_markup=train_kb
        )
