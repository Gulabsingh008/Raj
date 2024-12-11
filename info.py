import re
import os
from os import environ
from Script import script
from collections import defaultdict
from pyrogram import Client

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

#main variables
API_ID = int(environ.get('API_ID', '24519654'))
API_HASH = environ.get('API_HASH', '1ccea9c29a420df6a6622383fbd83bcd')
BOT_TOKEN = environ.get('BOT_TOKEN', '7778538687:AAEkghhb5pBmTpuix_Vhj5WofeBA6qH5dAk')
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1114789110').split()]
USERNAME = environ.get('USERNAME', "https://telegram.me/Af_mhakal")
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002030723564'))
MOVIE_GROUP_LINK = environ.get('MOVIE_GROUP_LINK', 'https://t.me/+Xz6Art-q091lODg1')
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002194109031').split()]
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://fplonq:CXBRdJeEAdtKbV6y@cluster0.q7dfa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI2 = environ.get('DATABASE_URI2', "mongodb+srv://2o8jsj:IHSJ8FC65WChypWS@cluster0.5tmub.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = environ.get('DATABASE_NAME', "cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'cluster0')
LOG_API_CHANNEL = int(environ.get('LOG_API_CHANNEL', '-1002030723564'))
QR_CODE = environ.get('QR_CODE', 'https://graph.org/file/d7c9c7906833797aa0244.jpg')
START_IMG = environ.get('START_IMG', 'https://graph.org/file/82e2895b4740905b054b9.gif')
#this vars is for when heroku or koyeb acc get banned, then change this vars as your file to link bot name
BIN_CHANNEL = int(environ.get('BIN_CHANNEL','-1002030723564'))
URL = environ.get('URL', 'efficient-carlye-myfilestream-c9938a22.koyeb.app')
ONEPAGEYAM = 'krownlinks.com'
STICKERS_IDS = ('CAACAgQAAxkBAAEK99dlfC7LDqnuwtGRkIoacot_dGC4zQACbg8AAuHqsVDaMQeY6CcRojME').split()

# verify system vars
IS_VERIFY = is_enabled('IS_VERIFY', True)
LOG_VR_CHANNEL = int(environ.get('LOG_VR_CHANNEL', '-1002030723564'))
TUTORIAL = environ.get("TUTORIAL", "https://t.me/howto_open_short_link/12")
TUTORIAL2 = environ.get("TUTORIAL2", "https://t.me/howto_open_short_link/12")
TUTORIAL3 = environ.get("TUTORIAL3", "https://t.me/howto_open_short_link/12")
VERIFY_IMG = environ.get("VERIFY_IMG", "https://graph.org/file/1669ab9af68eaa62c3ca4.jpg")
SHORTENER_API = environ.get("SHORTENER_API", "4dbeb3373153a8396dd23d2e9da53c8f24f4b449")
SHORTENER_WEBSITE = environ.get("SHORTENER_WEBSITE", ONEPAGEYAM)
SHORTENER_API2 = environ.get("SHORTENER_API2", "4dbeb3373153a8396dd23d2e9da53c8f24f4b449")
SHORTENER_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", ONEPAGEYAM)
SHORTENER_API3 = environ.get("SHORTENER_API3", "4dbeb3373153a8396dd23d2e9da53c8f24f4b449")
SHORTENER_WEBSITE3 = environ.get("SHORTENER_WEBSITE3", ONEPAGEYAM)
TWO_VERIFY_GAP = int(environ.get('TWO_VERIFY_GAP', "14400"))
THREE_VERIFY_GAP = int(environ.get('THREE_VERIFY_GAP', "14400"))
FILE_AUTO_DEL_TIMER = int(environ.get('FILE_AUTO_DEL_TIMER', '600'))

# languages search
LANGUAGES = ["hindi", "english", "telugu", "tamil", "kannada", "malayalam", "bengali", "marathi", "gujarati", "punjabi"]
QUALITIES = ["HdRip","web-dl" ,"bluray", "hdr", "fhd" , "240p", "360p", "480p", "540p", "720p", "960p", "1080p", "1440p", "2K", "2160p", "4k", "5K", "8K"]
YEARS = [f'{i}' for i in range(2024 , 2002,-1 )]
SEASONS = [f'season {i}'for i in range (1 , 23)]
REF_PREMIUM = 30
PREMIUM_POINT = 1500
auth_channel = environ.get('AUTH_CHANNEL', '-1002281015574')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
SUPPORT_GROUP = int(environ.get('SUPPORT_GROUP', '0'))

# hastags request features
request_channel = environ.get('REQUEST_CHANNEL', '-1002281015574')
REQUEST_CHANNEL = int(request_channel) if request_channel and id_pattern.search(request_channel) else None
UPI_PAY_LOGS = int(environ.get('UPI_PAY_LOGS', '-1002030723564'))

# bot settings
IGNORE_WORDS = (list(os.environ.get("IGNORE_WORDS").split(",")) if os.environ.get("IGNORE_WORDS") else [])
IGNORE_WORDS=["movies", "Movies", ",", "episode", "Episode", "episodes", "Episodes", "south indian", "south indian movie", "South Indian Movie", "south movie", "South Movie", "South Indian", "web-series", "punjabi", "marathi", "hindi me bhejo", "hindi", "gujrati", "combined", "!", "kro", "jaldi", "Audio", "audio", "movi", "language", "Language", "Hollywood", "All", "all", "bollywood", "Bollywood", "South", "south", "HD", "hd", "karo", "Karo", "fullepisode", "please", "plz", "Please", "Plz", "send", "link", "Link", "full", "Full", "dabbed", "dubbed", "gujarati", "gujrati", "Gujarati", "Gujrati", "season", "Season", "web", "series", "Web", "Series", "webseries", "WebSeries", "upload", "HD", "Hd", "bhejo", "ful", "Send", "Bhejo", "movie"]
IS_PM_SEARCH = is_enabled('IS_PM_SEARCH', False)
AUTO_FILTER = is_enabled('AUTO_FILTER', True)
PORT = os.environ.get('PORT', '8080')
MAX_BTN = int(environ.get('MAX_BTN', '8'))
AUTO_DELETE = is_enabled('AUTO_DELETE', True)
DELETE_TIME = int(environ.get('DELETE_TIME', 300))
IMDB = is_enabled('IMDB', False)
FILE_CAPTION = environ.get('FILE_CAPTION', f'{script.FILE_CAPTION}')
IMDB_TEMPLATE = environ.get('IMDB_TEMPLATE', f'{script.IMDB_TEMPLATE_TXT}')
LONG_IMDB_DESCRIPTION = is_enabled('LONG_IMDB_DESCRIPTION', False)
PROTECT_CONTENT = is_enabled('PROTECT_CONTENT', False)
SPELL_CHECK = is_enabled('SPELL_CHECK', True)
LINK_MODE = is_enabled('LINK_MODE', True)
SETTINGS = {
            'spell_check': SPELL_CHECK,
            'auto_filter': AUTO_FILTER,
            'file_secure': PROTECT_CONTENT,
            'auto_delete': AUTO_DELETE,
            'template': IMDB_TEMPLATE,
            'caption': FILE_CAPTION,
            'tutorial': TUTORIAL,
            'tutorial_two': TUTORIAL2,
            'tutorial_three': TUTORIAL3,
            'shortner': SHORTENER_WEBSITE,
            'api': SHORTENER_API,
            'shortner_two': SHORTENER_WEBSITE2,
            'api_two': SHORTENER_API2,
            'log': LOG_VR_CHANNEL,
            'imdb': IMDB,
            'link': LINK_MODE, 
            'is_verify': IS_VERIFY, 
            'verify_time': TWO_VERIFY_GAP,
            'shortner_three': SHORTENER_WEBSITE3,
            'api_three': SHORTENER_API3,
            'third_verify_time': THREE_VERIFY_GAP
    }
