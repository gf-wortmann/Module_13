# Домашнее задание по теме "Асинхронность на практике"
# Цель: приобрести навык использования асинхронного запуска функций на практике


import time
import asyncio

time_seed_for_sleep = 10
count_of_spheres = 5


async def start_strongman(name, powercity):
    print(f'Силач {name} начал соревнования')
    for i in range(1, count_of_spheres+1):
        await asyncio.sleep(time_seed_for_sleep / powercity)
        print(f'Силач {name} поднял {i} шар')
    print(f'Силач {name} закончил соревнования')
    

async def start_tournament(competitors):
    tasks = []
    for strongman in competitors:
        task = asyncio.create_task(start_strongman(*strongman))
        tasks.append(task)
    for task in tasks:
        await task
    

strongmen = [
    ['Hercules', 5],
    ['Atlantic', 6],
    ['Colosseum', 4]
]
    
asyncio.run(start_tournament(strongmen))
