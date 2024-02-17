import bot

import subprocess

cmd = 'sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add'
time = subprocess.Popen (cmd, shell=True)


if __name__=='__main__':
    # run the bot
    bot.run_discord_bot()
