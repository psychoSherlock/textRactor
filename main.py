import random
import telebot
import pytesseract
from PIL import Image
from random import randint
import logging

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


with open('api.key') as f:
    apiKey = f.read();


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', handlers=[logging.FileHandler('logs.log'), logging.StreamHandler()])

logging.warning('Bot started...')

bot = telebot.TeleBot(apiKey)

@bot.message_handler(commands=["start","help"]) # Message handlers for /start and /help
def greet(message):
    logging.info(f"👉 {message.text} from {message.from_user.first_name}")
    bot.reply_to(message, f"""
    Hello {message.from_user.first_name}
    """)

@bot.message_handler(content_types=['photo']) # Filters By photo messages
def photo(message):

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    image = bot.download_file(file_info.file_path) # Downloads the file
    user = message.from_user.first_name

    logging.warning(f"{user} send an image")

    bot.reply_to(message, f"Hmm..🕵️‍♂️ Let me read your image, {user} This might take a second or more ⏳")

    tr = textRactor()
    imageFile = tr.saveImage(image, user)
    imageData = tr.extractText(imageFile)
    bot.send_message(message.chat.id, '😊 Here you go...')
    try:
        bot.reply_to(message, imageData)
    except:
        imageData = "😖 Whoops, 🤷‍♂️ looks like the image doesn't contain any extractable text. Sorry 😬"
        bot.reply_to(message, imageData)

bot.polling()