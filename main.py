import asyncio
from bot import pet_bot, dp
from db import engine, Base

import models

from services.equipment_service import EquipmentService
from services.spell_service import SpellService

async def main():
    #Base.metadata.drop_all(engine)
    
    Base.metadata.create_all(engine)
    
    #SpellService.create_spell("огненный шар", "fireball", 1, 5, 8, 20)
    #SpellService.create_spell("волшебные стрелы", "magic_missle", 3, 2, 3, 20)
    #SpellService.create_spell("волшебный щит", "magic_shield", 0, 10, 3, 20)
    
    #EquipmentService.add_equipment("деревянный меч", "hand", 0, 0, 0, 2, 1, -1, 0)
    #EquipmentService.add_equipment("железный меч", "hand", 1, 0, 0, 4, 2, 0, 0)
    #EquipmentService.add_equipment("стальной меч", "hand", 2, 0, 0, 7, 3, 0, 0)
    #EquipmentService.add_equipment("волшебный меч", "hand", 3, 0, 0, 9, 4, 0, 2)
    #EquipmentService.add_equipment("меч Абобия I", "hand", 4, 2, 2, 14, 6, 2, 2)

    #EquipmentService.add_equipment("кожанный шлем", "head", 0, 2, 0, 0, 0, 0, 0)
    #EquipmentService.add_equipment("железный шлем", "head", 1, 4, 0, 0, 1, -1, 0)
    #EquipmentService.add_equipment("стальной шлем", "head", 2, 7, 0, 0, 2, -1, 0)
    #EquipmentService.add_equipment("волшебный шлем", "head", 3, 9, 0, 0, 3, 1, 2)
    #EquipmentService.add_equipment("шлем Абобия I", "head", 4, 14, 2, 2, 2, 2, 2)

    #EquipmentService.add_equipment("кожанный нагрудник", "body", 0, 1, 0, 0, 2, 0, 0)
    #EquipmentService.add_equipment("железный доспех", "body", 1, 2, 0, 0, 4, -2, 0)
    #EquipmentService.add_equipment("стальной доспех", "body", 2, 4, 0, 0, 7, -2, 0)
    #EquipmentService.add_equipment("волшебный доспех", "body", 3, 6, 0, 0, 9, 1, 2)
    #EquipmentService.add_equipment("доспех Абобия I", "body", 4, 7, 2, 2, 14, 2, 2)

    #EquipmentService.add_equipment("кожанные сапоги", "feet", 0, 0, 0, 0, 1, 1, 0)
    #EquipmentService.add_equipment("железные сапоги", "feet", 1, 0, 0, 0, 2, 2, 0)
    #EquipmentService.add_equipment("стальные сапоги", "feet", 2, 0, 0, 0, 4, 5, 0)
    #EquipmentService.add_equipment("волшебныe сапоги", "feet", 3, 0, 0, 0, 5, 10, 2)
    #EquipmentService.add_equipment("сапоги Абобия I", "feet", 4, 2, 2, 2, 6, 24, 2)

    #EquipmentService.add_equipment("кожанные штаны", "legs", 0, 0, 0, 0, 1, 0, 0)
    #EquipmentService.add_equipment("железные поножи", "legs", 1, 0, 0, 0, 2, 0, 0)
    #EquipmentService.add_equipment("стальные поножи", "legs", 2, 0, 0, 0, 4, 0, 0)
    #EquipmentService.add_equipment("волшебныe поножи", "legs", 3, 0, 0, 0, 5, 0, 2)
    #EquipmentService.add_equipment("поножи Абобия I", "legs", 4, 2, 2, 2, 12, 2, 2)

    #EquipmentService.add_equipment("деревянная палка", "hands", 0, 0, 0, 1, 0, -1, 2)
    #EquipmentService.add_equipment("простой посох", "hands", 1, 0, 0, 2, 0, 0, 4)
    #EquipmentService.add_equipment("качественный посох", "hands", 2, 0, 0, 3, 0, 0, 7)
    #EquipmentService.add_equipment("мощный посох", "hands", 3, 0, 0, 4, 0, 0, 9)
    #EquipmentService.add_equipment("посох Абобия I", "hands", 4, 2, 2, 5, 2, 2, 14)

    await dp.start_polling(pet_bot)


if __name__ == "__main__":
    print("starting bot")
    asyncio.run(main())
