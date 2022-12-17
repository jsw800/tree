import asyncio
import time
import numpy as np
import websockets
import json


class Effect:
    def __init__(self, points):
        self.buffer = []
        self.loop = asyncio.get_event_loop()
        self.connected = False
        self.loop.run_until_complete(self.run())

    async def run(self):
        start_server = websockets.serve(self.websocket_handler, '0', 8765)
        return await asyncio.gather(start_server)

    def __iter__(self):
        return self

    def __next__(self):
        return self.render

    def render(self):
        while len(self.buffer) == 0:
            time.sleep(0.01)
        return self.buffer.pop(0)

    async def websocket_handler(self, websocket, path):
        print('handler!')
        if self.connected:
            await websocket.close()
            return
        self.connected = True
        print('Connected!')
        try:
            async for message in websocket:
                frame = np.array(json.loads(message), dtype=np.float64) / 255
                self.buffer.append(frame)
                await websocket.send(str(len(self.buffer)))
        finally:
            self.connected = False
