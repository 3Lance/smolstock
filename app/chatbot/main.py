import asyncio
from websockets.server import serve

from chain import conversation

async def chatbot(websocket):
    print('connected')
    async for message in websocket:
        print(message)
        output = conversation({"input": message})
        await websocket.send(output['response'].strip())

async def main():
    async with serve(chatbot, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())

