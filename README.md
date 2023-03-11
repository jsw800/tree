# 3D LED Tree
This project contains all the necessary code to detect the 3D coordinates of
addressable LEDs on a Christmas tree, and run 3D effects on the lights on your tree.

## Running effects
The main entrypoint for running effects is `run.py`. You can just provide the
coordinates CSV file and which effect to run like

```bash
python run.py coords.csv simple_plane
```

You can also supply a `-t` flag which signals to run the effect in a point cloud
viewer rather than on the actual LEDs (good for testing things out or doing
development without access to a full tree setup).

If you're running this on a real strand of LEDs on a raspberry pi, make sure to use
`sudo` (required by neopixel).

## Contributing effects
If you want to contribute an effect, there's no need to get the whole tree setup,
just use the `-t` flag described above to test your effect in a point cloud viewer
rather than on a real tree setup.

Each effect is a file in the `effects` directory which contains a class named `Effect`
that extends an abstract base effect class and provides an `update` method to update
the colors that go on the tree, which is called between each frame. You can supply a
max frame rate and modify the color mode to be HSV or RGB (default RGB). I would
recommend using HSV with a saturation of 0.8-0.9 and a brightness of no more than 0.5
if you're doing dynamic colors in any way.


## Setting up the whole tree
I'm not going to explain the wiring here, I am a software person and would do a bad
job of it, but there are tutorials to get WS2811 LED strands wired up to a raspberry
pi online. Once you have that done, string your LEDs on the tree and get your pi
up and running.

### Image Capture
To detect the 3D coordinates of each LED, we need to take images of the tree with
each individual light on. I am doing this from 4 separate directions and getting
consensus between those 4 directions to get higher confidence in the LEDs being
detected correctly. See instructions in `detector_server.py` and `detector_camera.py`.

The basic concept is to have a computer with an onboard camera connect to a websocket
server on the pi and tell it which light to turn on, then take a picture with each LED
on - then rotate the tree a quarter turn and rinse and repeat until you have all 4
sides.

### Image processing and point detection
To run the detector script on the generated images, simply run

```bash
python detector.py <path to csv output file>
```

This should take a couple minutes and will create a CSV output file with the 3D coords
of the lights on your tree. I have found that a few of these will be inaccurate, so
I use the `simple_plane` effect in all 3 planes to manually pick out which lights are
inaccurate in each plane. Once you notice an inaccurate light, tag it with a piece
of sticky note or something. You can use the `binary` effect to have each light
blink out its index in binary to figure out which index the bad lights are, and then
you can manually correct the value in the csv file at that index.

Once that's done, you should be good to go!

# Live videos

Perlin noise:

https://drive.google.com/uc?export=download&id=1kCHi-PUhB6r8DEIrgCr12qjl-Enfwtjs


