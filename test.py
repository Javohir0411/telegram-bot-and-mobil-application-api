import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        user="postgres",
        password="java0411",
        database="lesa_arenda_db",
        host="127.0.0.1",
        port=5432
    )
    print("Ulandi")
    await conn.close()

asyncio.run(test())