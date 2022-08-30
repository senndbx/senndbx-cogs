from random import random, randint
from PIL import Image
from petpetgif.saveGif import save_transparent_gif
import math

__all__ = ["ShakeGif"]

frames = 20
resolution = (128, 128)
delay = 20
amplitude = randint(1, 12)

class ShakeGif(object):
    def __init__(self):
        pass

    def make(self, source, dest, is_gif=False):
        """

        :param source: A filename (string), pathlib.Path object or a file object. (This parameter corresponds
                    and is passed to the PIL.Image.open() method.)
        :param dest: A filename (string), pathlib.Path object or a file object. (This parameter corresponds
                    and is passed to the PIL.Image.save() method.)
        :return: None
        """
        images = []
        if is_gif:
            im = Image.open(source)
            for i in range(math.lcm(frames, im.n_frames)):
                dev = (round(amplitude - 2*amplitude*random()), round(amplitude - 2*amplitude*random()))

                canvas = Image.new('RGBA', size=resolution, color=(0, 0, 0, 0))
                im.seek(i % im.n_frames)
                frame_base = im.convert('RGBA').resize(resolution)
                canvas.paste(frame_base, box=dev)
                images.append(canvas)
        
        else:
            base = Image.open(source).convert('RGBA').resize(resolution)

            for i in range(frames):
                dev = (round(amplitude - 2*amplitude*random()), round(amplitude - 2*amplitude*random()))

                canvas = Image.new('RGBA', size=resolution, color=(0, 0, 0, 0))
                frame_base = base.resize(resolution)
                canvas.paste(frame_base, box=dev)
                images.append(canvas)

        save_transparent_gif(images, durations=40, save_file=dest)
