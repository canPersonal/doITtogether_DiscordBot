import bot

import subprocess

cmd = '/home/container/chromedriver.sh'
time = subprocess.Popen (cmd, shell=True)


if __name__=='__main__':
    # run the bot
    bot.run_discord_bot()
