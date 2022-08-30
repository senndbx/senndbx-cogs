from .rabotcogs import Rabotcogs


def setup(bot):
    bot.add_cog(Rabotcogs(bot))