# 3D LED Tree

This project contains all the necessary code to detect the 3D coordinates of
addressable LEDs on a Christmas tree, and run 3D effects on the lights on your tree.

## Running effects

The main entrypoint for running effects is `run.py`. You can just provide the
coordinates CSV file and which effect to run like

```bash
python run.py coords.csv perlin
```

You can also supply a `-t` flag which signals to run the effect in a point cloud
viewer rather than on the actual LEDs (good for testing things out or doing
development without access to a full LED setup).

If you're running this on a real strand of LEDs on a raspberry pi, make sure to use
`sudo` (required by neopixel).

## Contributing effects

If you want to contribute an effect, there's no need to get the whole LED + rpi + tree setup,
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
sides. You will end up with 4 pictures for each LED you have, one for each direction.

### Image processing and point detection

To run the detector script on the generated images, simply run

```bash
python detector.py <path to csv output file>
```

This should take a few minutes (depending somewhat on how many lights you have),
and will create a CSV output file with the 3D coords of the lights on your tree.

### Error correction

At this point, you should have all you need to run 3D effects on your tree. However,
A few points will likely be inaccurate due to being obscured by branches or due to being moved around
during the detection process. To manually correct errors, this is the process I use:

- Use the `simple_plane` effect in each axis to locate and mark lights that have incorrect coordinates. Viewing the points in the point cloud viewer by running any effect with the -t flag can also be a good way of finding these, since some points may lie very obviously outside of the tree in the point cloud viewer.
- For each marked point, use the `binary` effect to take down the index of the light in binary and convert to decimal.
- Use the `single` effect with the index you got to verify you have the right point
- Find that point in your coordinate CSV file
- Manually correct the coordinates. I find `simple_plane` to be useful here to tell what needs to be fixed (i.e. `simple_plane` with AXIS=0 would show you if the x value needs adjusting, and you can look at the x values of the light's neighbors compared to its actual location on the tree and determine what adjustments need to be made).

It's likely that after error correction, your coordinates will no longer be in the [-1, 1] range in the X/Y directions.
This can cause some of the effect to not be properly centered which is not desirable. To fix this you can run

```bash
python renormalize.py <input_csv> <output_csv>
```

Once that's done, you should be good to go!

## Note On Dependencies

I'm sure there are much better ways of handling package management with python but I am inexperienced in
python so this is currently a bit of a mess. I'm using a virtualenv with python 3.9, and the following
libraries:

- numpy
- opencv (aka cv2)
- open3d (only needed if you're running in test mode/with the point cloud viewer)
  - Note: I had trouble installing this on a MacBook with an M2 processor with python >3.9, which is why I'm
    using python 3.9 and not any of the newer python versions.
- `rpi_ws281x` and `adafruit-circuitpython-neopixel` (only needed if you're running live on the raspberry pi)
- skikit-learn

I may be missing some in this list, my approach is to just start running things and as soon as you get an
ImportError, install the missing dependency ¯\\\_(ツ)\_/¯ It's a little hard to document these consistently
since in actuality different libraries may be needed on different machines (i.e. on the rpi vs on your
development machine/machine running the detector camera).

# Live videos

https://photos.app.goo.gl/k13BaMM5o8aXpEmq6
