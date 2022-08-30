from PIL import Image
from petpetgif.saveGif import save_transparent_gif
import math

__all__ = ["RollGif"]

frames = 20
resolution = (128, 128)
delay = 20

class RollGif(object):
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
                t = frames * (1 - math.cos(math.pi / 2 * i / frames))
                angle = t * 360 / frames

                canvas = Image.new('RGBA', size=resolution, color=(0, 0, 0, 0))
                im.seek(i % im.n_frames)
                frame_base = im.convert('RGBA').resize(resolution)
                frame_base = frame_base.rotate(angle)
                canvas.paste(frame_base)
                images.append(canvas)

        else:
            base = Image.open(source).convert('RGBA').resize(resolution)
            for i in range(frames):
                t = frames * (1 - math.cos(math.pi / 2 * i / frames))
                angle = t * 360 / frames

                canvas = Image.new('RGBA', size=resolution, color=(0, 0, 0, 0))
                frame_base = base.resize(resolution)
                frame_base = frame_base.rotate(angle)
                canvas.paste(frame_base)
                images.append(canvas)

        save_transparent_gif(images, durations=40, save_file=dest)
