import time
import signal
from helpers import load_coords, get_effect, parse_args


def main():
    args = parse_args()
    coords = load_coords(args.coords_file)
    effect = get_effect(args.effect)
    if args.test:
        from TestTree import TestTree
        tree = TestTree(coords)
    elif args.remote:
        from RemoteTree import RemoteTree
        tree = RemoteTree(args.url, coords)
    else:
        from LEDTree import LEDTree
        tree = LEDTree(coords, int(args.num_pixels))

    def sigint_handler(sig, frame):
        tree.off()
        print('Goodbye!')
        exit(0)

    signal.signal(signal.SIGINT, sigint_handler)
    for frame in effect(coords):
        tree.render_frame(frame)
        time.sleep(0.01)


if __name__ == '__main__':
    main()

