import time
import signal
import matplotlib.colors
from helpers import load_coords, get_effect, parse_args
from BaseEffect import ColorMode


def main():
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

    def sigint_handler(sig, frame):
        tree.off()
        print('Goodbye!')
        exit(0)

    signal.signal(signal.SIGINT, sigint_handler)
    last_render = time.time()
    effect = Effect(coords)
    for frame in effect:
        if effect.color_mode == ColorMode.HSV:
            frame = matplotlib.colors.hsv_to_rgb(frame)
        tree.render_frame(frame)
        time_between_frames = time.time() - last_render
        last_render = time.time()
        expected_time_between_frames = 1 / effect.max_fps
        to_sleep = expected_time_between_frames - time_between_frames
        if to_sleep >= 0:
            time.sleep(to_sleep)


if __name__ == '__main__':
    main()

