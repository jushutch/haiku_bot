#!/usr/bin/bash
cd /home/pi/Desktop/haiku_bot
python3 twitter_bot.py >> log.txt
git add log.txt
git commit -m "Auto-generated commit for logging"
git push haiku_bot main