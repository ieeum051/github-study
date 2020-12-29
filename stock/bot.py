import telegram

bot_token = '1406855830:AAHxMrhLzNtKK8veSbxkAF2c9E3WH6clXkY'
mybot = telegram.Bot(token = bot_token)
updates = mybot.getUpdates()
for u in updates:
    print(u.message)
