import bot

import subprocess

cmd = 'apt-get update && apt-get install -y gnupg2'
time = subprocess.Popen (cmd, shell=True)


if __name__=='__main__':
    # run the bot
    bot.run_discord_bot()
