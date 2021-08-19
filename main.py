import random
import telebot
import pytesseract
from PIL import Image
from random import randint
import logging
from os import remove as delete
from pydub import AudioSegment
import speech_recognition as sr

def generateRandom():
    return random.randint(100, 9999999)

r = sr.Recognizer()
class textRactor:
    def saveFile(self, data, name, fType):

        randomNumber = generateRandom()
        if fType=="image":
            fileName = f"images/{name}_{randomNumber}.jpg"
            with open(fileName, "wb") as img:
                img.write(data)
            return fileName


    def extractText(self, imagePath):
        img = Image.open(imagePath)
        imageData = pytesseract.image_to_string(img)
        return imageData
    
    def saveAudio(self, audio, name):
        randomNumber = generateRandom()
        fileName = f"audios/{name}_{randomNumber}.jpg"
    
    def recogniseOgg(self,data, name):
        output = "test.wav"
        randomNumber = generateRandom()
        fileName = f"audios/{name}_{randomNumber}.ogg"
        with open(fileName, 'wb') as ogg:
            ogg.write(data)
        
        dest = fileName + '.wav'
        sound = AudioSegment.from_ogg(fileName).export(dest, format="wav")
        
        with sr.AudioFile(dest) as source:
            audio_data = r.record(source)
            textData = r.recognize_google(audio_data)
        delete(fileName)
        return textData, dest

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

tr = textRactor()

@bot.message_handler(content_types=['photo']) # Filters By photo messages
def photo(message):

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    image = bot.download_file(file_info.file_path) # Downloads the file
    user = message.from_user.first_name

    logging.warning(f"{user} send an image")

    bot.reply_to(message, f"Hmm..🕵️‍♂️ Let me read your image, {user} This might take a second or more ⏳")

    imageFile = tr.saveFile(image, user, 'image')
    imageData = tr.extractText(imageFile)
    delete(imageFile) # Delete the file recieved (I consider my users privacy important)
    bot.send_message(message.chat.id, '😊 Here you go...')
    try:
        bot.reply_to(message, imageData)
    except:
        imageData = "😖 Whoops, 🤷‍♂️ looks like the image doesn't contain any extractable text. Sorry 😬"
        bot.reply_to(message, imageData)



@bot.message_handler(content_types=['voice'])
def voice(message):
    user = message.from_user.first_name
    fileID = message.voice.file_id
    file_info = bot.get_file(fileID)
    voice = bot.download_file(file_info.file_path) # Downloads the file
    logging.warning(f"{user} send a voice")
    bot.reply_to(message, "🤨 What did you say?👂 Lemme listen carefully")
    
    converted, dest = tr.recogniseOgg(voice, user)
    bot.reply_to(message, converted)

    delete(dest)

if __name__ == '__main__':
    bot.polling()