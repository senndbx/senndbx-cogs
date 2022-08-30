from PIL import Image
from petpetgif.saveGif import save_transparent_gif
from pkg_resources import resource_stream
import math

__all__ = ["PetGif"]

class PetGif(object):
    def __init__(self):
        self.frames = 10
        self.resolution = (128, 128)
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
                squeeze = t if t < self.frames/2 else self.frames - t
                width = 0.8 + squeeze * 0.02
                height = 0.8 - squeeze * 0.05
                offsetX = (1 - width) * 0.5 + 0.1
                offsetY = (1 - height) - 0.08

                canvas = Image.new('RGBA', size=self.resolution, color=(0, 0, 0, 0))
                im.seek(i % im.n_frames)
                frame_base = im.convert('RGBA')
                canvas.paste(frame_base.resize((round(width * self.resolution[0]), round(height * self.resolution[1]))), (round(offsetX * self.resolution[0]), round(offsetY * self.resolution[1])))
                pet = Image.open(resource_stream(__name__, f"img/pet/pet{t}.gif")).convert('RGBA').resize(self.resolution)
                canvas.paste(pet, mask=pet)
                images.append(canvas)

        else:
            base = Image.open(source).convert('RGBA').resize(self.resolution)

            for i in range(self.frames):
                squeeze = i if i < self.frames/2 else self.frames - i
                width = 0.8 + squeeze * 0.02
                height = 0.8 - squeeze * 0.05
                offsetX = (1 - width) * 0.5 + 0.1
                offsetY = (1 - height) - 0.08

                canvas = Image.new('RGBA', size=self.resolution, color=(0, 0, 0, 0))
                canvas.paste(base.resize((round(width * self.resolution[0]), round(height * self.resolution[1]))), (round(offsetX * self.resolution[0]), round(offsetY * self.resolution[1])))
                pet = Image.open(resource_stream(__name__, f"img/pet/pet{i}.gif")).convert('RGBA').resize(self.resolution)
                canvas.paste(pet, mask=pet)
                images.append(canvas)

        save_transparent_gif(images, durations=20, save_file=dest)
