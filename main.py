import random
import telebot
import pytesseract
from PIL import Image
from random import randint
import logging

with open('api.key') as f:
    apiKey = f.read();



class textRactor:
    def saveImage(self, image, name):
        randomNumber = random.randint(100, 9999999)
        fileName = f"images/{name}_{randomNumber}.jpg"

        with open(fileName, "wb") as img:
            img.write(image)
        return fileName


    def extractText(self, imagePath):
        img = Image.open(imagePath)
        imageData = pytesseract.image_to_string(img)
        return imageData




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
    image = bot.download_file(file_info.file_path) # Downloads the file


    user = message.from_user.first_name
    tr = textRactor()
    imageFile = tr.saveImage(image, user)
    imageData = tr.extractText(imageFile)
    bot.reply_to(message, imageData)
    # with open("images/test.jpg", 'wb') as new_file:
    #     new_file.write(downloaded_file)

bot.polling()