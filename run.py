import asyncio
import threading
import time
import signal
import matplotlib.colors
from helpers import load_coords, get_effect, parse_args
from BaseEffect import ColorMode


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    args = parse_args()
    coords = load_coords(args.coords_file)
    Effect = get_effect(args.effect)
    if args.test:
        from TestTree import TestTree
        tree = TestTree(coords)
    elif args.remote:
        from RemoteTree import RemoteTree
        tree = RemoteTree(args.url, coords)
    else:
        from LEDTree import LEDTree
        tree = LEDTree(coords)

    def sigint_handler():
        tree.off()
        print('Goodbye!')
        exit(0)

    loop.add_signal_handler(signal.SIGINT, sigint_handler)
    effect = Effect(coords)

    async def game_loop():
        effect_iter = aiter(effect)
        while True:
            start = time.time()
            frame = await anext(effect_iter)
            await tree.render_frame(frame)
            end = time.time()
            time_to_sleep = max(0, (1 / effect.max_fps) - (end - start))
            await asyncio.sleep(time_to_sleep)

    async def run():
        effect_coroutine = effect.coroutine()
        return await asyncio.gather(effect_coroutine, game_loop())

    try:
        loop.run_until_complete(run())
    finally:
        loop.close()

if __name__ == '__main__':
    main()

