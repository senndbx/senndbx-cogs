from redbot.core import commands
from typing import Union, Optional
from io import BytesIO
import discord, urllib, aiohttp
from PIL import Image

from .petgif import PetGif
from .rollgif import RollGif
from .shakegif import ShakeGif
from .wobblegif import WobbleGif
from .bonkgif import BonkGif
from .essexburngif import EssexBurnGif

class ImageFindError(Exception):
    """Generic error for the _get_image function."""
    pass

class Gifmaker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imagetypes = ['png', 'jpg', 'jpeg']
        self.videotypes = ['gif', 'webp']

    # stolen and modified from deepfry cog https://github.com/Flame442/FlameCogs
    async def _get_image(self, ctx, link: Union[discord.Member, str]):
        """Helper function to find an image."""
        
        if not ctx.message.attachments and not link:
            async for msg in ctx.channel.history(limit=10):
                for a in msg.attachments:
                    path = urllib.parse.urlparse(a.url).path
                    if (
                        any(path.lower().endswith(x) for x in self.imagetypes)
                        or any(path.lower().endswith(x) for x in self.videotypes)
                    ):
                        link = a.url
                        break
                if link:
                    break
            if not link:
                raise ImageFindError('Please provide an attachment.')
        if type(link) == discord.PartialEmoji:
            emoji = await link.url_as(format='gif' if link.animated else 'png').read() # retrieve the image bytes
            img = emoji
            isgif = link.animated
        elif isinstance(link, discord.Member): #member avatar
            if discord.version_info.major == 1:
                avatar = link.avatar_url_as(static_format="png")
            else:
                avatar = link.display_avatar.with_static_format("png").url
            # dpy will add a ?size= flag to the end, so for this one case we only need to check gif in
            if ".gif" in str(avatar):
                isgif = True
            else:
                isgif = False
            data = await avatar.read()
            img = data
        elif link: #linked image
            path = urllib.parse.urlparse(link).path
            if any(path.lower().endswith(x) for x in self.imagetypes):
                isgif = False
            elif any(path.lower().endswith(x) for x in self.videotypes):
                isgif = True
            else:
                raise ImageFindError(
                    f'That does not look like an image of a supported filetype. Make sure you provide a direct link.'
                )
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(link) as response:
                        r = await response.read()
                        img = r
                except (OSError, aiohttp.ClientError):
                    raise ImageFindError(
                        'An image could not be found. Make sure you provide a direct link.'
                    )
        else: #attached image
            path = urllib.parse.urlparse(ctx.message.attachments[0].url).path
            if any(path.lower().endswith(x) for x in self.imagetypes):
                isgif = False
            elif any(path.lower().endswith(x) for x in self.videotypes):
                isgif = True
            else:
                raise ImageFindError(f'That does not look like an image of a supported filetype.')
            # if ctx.message.attachments[0].size > 8000000:
            #     raise ImageFindError('That image is too large.')
            temp_orig = BytesIO()
            await ctx.message.attachments[0].save(temp_orig)
            temp_orig.seek(0)
            img = temp_orig.read()
        pil_img = Image.open(BytesIO(img))
        if max(pil_img.size) > 3840:
            raise ImageFindError('That image is too large.')
        duration = None
        if isgif and 'duration' in pil_img.info:
            duration = pil_img.info['duration']
        return img, isgif, duration
    
    @commands.command()
    @commands.bot_has_permissions(attach_files=True)
    async def pet(self, ctx, link: Optional[Union[discord.PartialEmoji, discord.Member, str]]):
        image, isgif, duration = await self._get_image(ctx, link)

        source = BytesIO(image) # file-like container to hold the emoji in memory
        dest = BytesIO() # container to store the petpet gif in memory
        PetGif().make(source, dest, is_gif=isgif)
        dest.seek(0) # set the file pointer back to the beginning so it doesn't upload a blank file.

        try:
            await ctx.send(file=discord.File(dest, filename=f"petpet.gif"))
        except discord.errors.HTTPException:
            return await ctx.send('That image is too large.')

    @commands.command()
    @commands.bot_has_permissions(attach_files=True)
    async def barrelroll(self, ctx, link: Optional[Union[discord.PartialEmoji, discord.Member, str]]):
        image, isgif, duration = await self._get_image(ctx, link)

        source = BytesIO(image)
        dest = BytesIO()
        RollGif().make(source, dest, is_gif=isgif)
        dest.seek(0)

        try:
            await ctx.send(file=discord.File(dest, filename=f"barrelroll.gif"))
        except discord.errors.HTTPException:
            return await ctx.send('That image is too large.')
            
    @commands.command()
    @commands.bot_has_permissions(attach_files=True)
    async def wobble(self, ctx, link: Optional[Union[discord.PartialEmoji, discord.Member, str]]):
        image, isgif, duration = await self._get_image(ctx, link)

        source = BytesIO(image)
        dest = BytesIO()
        WobbleGif().make(source, dest, is_gif=isgif)
        dest.seek(0)

        try:
            await ctx.send(file=discord.File(dest, filename=f"wobble.gif"))
        except discord.errors.HTTPException:
            return await ctx.send('That image is too large.')

    @commands.command()
    @commands.bot_has_permissions(attach_files=True)
    async def shake(self, ctx, link: Optional[Union[discord.PartialEmoji, discord.Member, str]]):
        image, isgif, duration = await self._get_image(ctx, link)

        source = BytesIO(image)
        dest = BytesIO()
        ShakeGif().make(source, dest, is_gif=isgif)
        dest.seek(0)

        try:
            await ctx.send(file=discord.File(dest, filename=f"shake.gif"))
        except discord.errors.HTTPException:
            return await ctx.send('That image is too large.')

    @commands.command()
    @commands.bot_has_permissions(attach_files=True)
    async def bonk(self, ctx, link: Optional[Union[discord.PartialEmoji, discord.Member, str]]):
        image, isgif, duration = await self._get_image(ctx, link)

        source = BytesIO(image)
        dest = BytesIO()
        BonkGif().make(source, dest, is_gif=isgif)
        dest.seek(0)

        try:
            await ctx.send(file=discord.File(dest, filename=f"bonk.gif"))
        except discord.errors.HTTPException:
            return await ctx.send('That image is too large.')

    @commands.command()
    @commands.bot_has_permissions(attach_files=True)
    async def essexburn(self, ctx, link: Optional[Union[discord.PartialEmoji, discord.Member, str]]):
        image, isgif, duration = await self._get_image(ctx, link)

        source = BytesIO(image)
        dest = BytesIO()
        EssexBurnGif().make(source, dest, is_gif=isgif)
        dest.seek(0)

        try:
            await ctx.send(file=discord.File(dest, filename=f"burn.gif"))
        except discord.errors.HTTPException:
            return await ctx.send('That image is too large.')