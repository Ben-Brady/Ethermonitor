import os
from dotenv import load_dotenv
load_dotenv()

from Modules.bot import bot
from Commands import help,register,stats,leaderboard

bot.run(os.getenv("BOTTOKEN"))