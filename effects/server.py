import asyncio
import time
import numpy as np
import websockets
import json

MAX_FPS = 20
MAX_SPF = 1 / MAX_FPS

loop = asyncio.get_event_loop()

connected = False

buffer = []

async def websocket_handler(websocket, path):
    global connected
    # only one connection at a time - we only have one tree
    if connected:
        await websocket.close()
        return
    connected = True
    print('Connected!')
    try:
        async for message in websocket:
            frame = np.array(json.loads(message), dtype=np.float64) / 255
            buffer.append(frame)
            await websocket.send(str(len(buffer)))
    finally:
        connected = False
        print('Disconnected!')


async def effect():
    def render():
        frame = buffer.pop(0)
        return frame

    while True:
        start = time.time()
        if len(buffer) > 0:
            yield render

        end = time.time()
        await asyncio.sleep(max(0, MAX_SPF - (end - start)))


async def run():
    start_server = websockets.serve(websocket_handler, 'localhost', 8765)
    return await asyncio.gather(start_server, effect())

try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print('Goodbye!')
finally:
    loop.close()
