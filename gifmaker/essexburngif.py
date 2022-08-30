from PIL import Image
from petpetgif.saveGif import save_transparent_gif
from pkg_resources import resource_stream
import math
from io import BytesIO

__all__ = ["EssexBurnGif"]

class EssexBurnGif(object):
    def __init__(self):
        self.essex = Image.open(resource_stream(__name__, "img/essexburn-small.gif"))
        self.resolution = self.essex.size
        self.width = 0.2
        self.height = 0.2
        self.offsetX = (1 - self.width) - 0.08
        self.offsetY = (1 - self.height)

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
            for i in range(math.lcm(self.essex.n_frames, im.n_frames)):
                canvas = Image.new('RGBA', size=self.resolution, color=(0, 0, 0, 0))
                im.seek(i % im.n_frames)
                frame_base = im.convert('RGBA')
                canvas.paste(frame_base.resize((round(self.width * self.resolution[0]), round(self.height * self.resolution[1]))), (round(self.offsetX * self.resolution[0]), round(self.offsetY * self.resolution[1])))
                self.essex.seek(i % self.essex.n_frames)
                essex_frame = BytesIO()
                self.essex.save(essex_frame, format='png')
                essex_frame = Image.open(essex_frame).convert('RGBA').resize(self.resolution)
                canvas.paste(essex_frame, mask=essex_frame)
                images.append(canvas)

        else:
            base = Image.open(source).convert('RGBA')

            for i in range(self.essex.n_frames):
                canvas = Image.new('RGBA', size=self.resolution, color=(0, 0, 0, 0))
                canvas.paste(base.resize((round(self.width * self.resolution[0]), round(self.height * self.resolution[1]))), (round(self.offsetX * self.resolution[0]), round(self.offsetY * self.resolution[1])))
                self.essex.seek(i)
                essex_frame = BytesIO()
                self.essex.save(essex_frame, format='png')
                essex_frame = Image.open(essex_frame).convert('RGBA')
                canvas.paste(essex_frame, mask=essex_frame)
                images.append(canvas)

        save_transparent_gif(images, durations=self.essex.info['duration'], save_file=dest)
