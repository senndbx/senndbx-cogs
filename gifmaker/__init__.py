from .gifmaker import Gifmaker

from .petgif import *
from .rollgif import *
from .shakegif import *
from .wobblegif import *

def setup(bot):
    bot.add_cog(Gifmaker(bot))
