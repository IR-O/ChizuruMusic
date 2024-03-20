from os import getenv


API_ID = int(getenv("API_ID", "11796331"))
API_HASH = getenv("API_HASH", "a089161b52f234bb90a6eb915551e8c0")
BOT_TOKEN = getenv("BOT_TOKEN", "6365132039:AAH8DJkhbtL8H7Gy1mGKKxUPDN92MusAJRQ")
OWNER_ID = int(getenv("OWNER_ID", "6045293810"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6045293810").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Michiko:michiko@michiko.oomgmrd.mongodb.net/?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "BQCz_2sAiSPxDaeRwzoIC_8QJkR_LoK7MND0f8iny6mloCk7dgaep1n2P28t-FdslyX_GWOiYqU4MKIrW2EPPfK79F4wU0lpIVma4c-_FQONDGslm2ICpDQUXQWD5i30XoDZywww71mKgSQXkq4AE_NWH_zW99vzDV_qQ3VpEZd3j__tHEWCqnzqW1AvALHJ8dz1Bo80N4WdSGP6SJ-7WwFDCFAOvccDustOZUoBxknCMNENmtMYLtmeKHnoxRrCwStmsuxd_Yn5n_f0hLg6-4rYLHgBCBo-QcR_hWfvcCjBvibU35zJwICSjabe3ltCz6LzWN4HlDoiXfMhPy_F16N_1ckRoAAAAAFoePH0AA")


