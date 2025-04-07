import aiosqlite
import asyncio
import websockets
import json

DATABASE = "data.db"
WEBSOCKET_URL = "wss://your-websocket-server.com"

# Create the SQLite table
async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER,
                ltp1 REAL,
                ltp2 REAL
            )
        """)
        await db.commit()

# Function to store received WebSocket data
async def store_data(timestamp, ltp1, ltp2):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("INSERT INTO market_data (timestamp, ltp1, ltp2) VALUES (?, ?, ?)", 
                         (timestamp, ltp1, ltp2))
        await db.commit()

# Function to handle WebSocket communication
async def websocket_handler():
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)

            timestamp = data.get("timestamp")  # Ensure it's in milliseconds
            ltp1 = data.get("ltp1")
            ltp2 = data.get("ltp2")

            await store_data(timestamp, ltp1, ltp2)
            print(f"Stored: {timestamp}, LTP1: {ltp1}, LTP2: {ltp2}")

            await asyncio.sleep(1)  # Regulate data insertion rate

async def main():
    await init_db()  # Ensure DB is initialized
    await websocket_handler()  # Start WebSocket handling

# Run the asynchronous event loop
asyncio.run(main())