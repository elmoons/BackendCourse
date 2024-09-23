import asyncio
import aiohttp


async def get_data(id: int, endpoint: str):
    print(f"Начал выполение {id}")
    url = f"http://127.0.0.1:8000/{endpoint}/{id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f"Закончил выполение {id}")


async def main():
    tasks = [get_data(i, "sync") for i in range(300)]
    res = await asyncio.gather(*tasks)
    return res

asyncio.run(main())







