import telebot

with open('api.key') as f:
    apiKey = f.read();

bot = telebot.TeleBot(apiKey)

@bot.message_handler(commands=["start","help"]) # Message handlers for /start and /help
def greet(message):
    print(f"{message.text} : {message.from_user.first_name}")
    bot.reply_to(message, """
    Hello, the bot is in development
    """)

@bot.message_handler(content_types=['photo']) # Filters By photo messages
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path) # Downloads the file

    with open("images/test.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

bot.polling()