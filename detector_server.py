import asyncio
import websockets
import numpy as np

import board
import neopixel

"""
    This file is run on the raspberry pi
    it listens for a websocket connection
    Once it receives a websocket connection, for each message it receives,
    it will cast the message to an int and turn on the light at that index (and turn all others off)

    Note that this server is NOT secure in any way, simply meant as a quick way to get each light to
    turn on when you need it.
"""

pixels = neopixel.NeoPixel(board.D18, 100, auto_write=False)

def main():
    loop = asyncio.get_event_loop()

    connected = False

    async def websocket_handler(websocket, path):
        nonlocal connected
        # only one connection at a time - we only have one tree
        if connected:
            await websocket.close()
            return
        connected = True
        print('Connected!')
        try:
            async for message in websocket:
                index = int(message)
                pixels.fill((0, 0, 0))
                pixels[index] = (255, 255, 255)
                pixels.show()
        finally:
            connected = False
            print('Disconnected!')
            pixels.fill((0, 0, 0))
            pixels.show()

    async def run():
        start_server = websockets.serve(websocket_handler, '0', 8765)
        return await asyncio.gather(start_server)

    try:
        loop.run_until_complete(run())
        loop.run_forever()
    except KeyboardInterrupt:
        print("Goodbye!")
    finally:
        loop.close()

if __name__ == "__main__":
    main()
