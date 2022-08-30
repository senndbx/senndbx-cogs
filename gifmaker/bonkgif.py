from PIL import Image
from petpetgif.saveGif import save_transparent_gif
from pkg_resources import resource_stream
import math

__all__ = ["BonkGif"]

class BonkGif(object):
    def __init__(self):
        self.frames = 10
        self.resolution = (195, 116)
        self.delay = 20

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
            for i in range(math.lcm(self.frames, im.n_frames)):
                t = i % self.frames
                squeeze = 0 if t < 7 else (t if t < self.frames/2 else self.frames - t)
                width = (0.8 + squeeze * 0.02) * 0.3
                height = (1 - squeeze * 0.1) * 0.4
                offsetX = (1 - width) * 0.5 + 0.25
                offsetY = (1 - height) - 0.08

                canvas = Image.new('RGBA', size=self.resolution, color=(0, 0, 0, 0))
                im.seek(i % im.n_frames)
                frame_base = im.convert('RGBA')
                canvas.paste(frame_base.resize((round(width * self.resolution[0]), round(height * self.resolution[1]))), (round(offsetX * self.resolution[0]), round(offsetY * self.resolution[1])))
                bonk = Image.open(resource_stream(__name__, f"img/bonk/bonk{t}.png")).convert('RGBA').resize(self.resolution)
                canvas.paste(bonk, mask=bonk)
                images.append(canvas)

        else:
            base = Image.open(source).convert('RGBA').resize(self.resolution)

            for i in range(self.frames):
                squeeze = 0 if i < 7 else (i if i < self.frames/2 else self.frames - i)
                width = (0.8 + squeeze * 0.02) * 0.3
                height = (1 - squeeze * 0.1) * 0.4
                offsetX = (1 - width) * 0.5 + 0.25
                offsetY = (1 - height) - 0.08

                canvas = Image.new('RGBA', size=self.resolution, color=(0, 0, 0, 0))
                canvas.paste(base.resize((round(width * self.resolution[0]), round(height * self.resolution[1]))), (round(offsetX * self.resolution[0]), round(offsetY * self.resolution[1])))
                bonk = Image.open(resource_stream(__name__, f"img/bonk/bonk{i}.png")).convert('RGBA').resize(self.resolution)
                canvas.paste(bonk, mask=bonk)
                images.append(canvas)

        durations = [20] * len(images)
        durations[len(durations)-1] = 5
        save_transparent_gif(images, durations=durations, save_file=dest)
