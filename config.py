from os import getenv


API_ID = int(getenv("API_ID", "11796331"))
API_HASH = getenv("API_HASH", "a089161b52f234bb90a6eb915551e8c0")
BOT_TOKEN = getenv("BOT_TOKEN", "5964346248:AAGtWqikxHyNjT9qKPMpEeN7rSqhy1XWWwc")
OWNER_ID = int(getenv("OWNER_ID", "6045293810"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6045293810").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Michiko:michiko@michiko.oomgmrd.mongodb.net/?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "BQCz_2sAuBBk-g1dCC7WApKyOO9dCb25eA06g2gBAuoF_sXWkmnv9mkNNngYM_GdX1146EJRQgqwh5PS1fRXHxTgXGYgJhqBIC9GF4f7IBLoGuKWtp3epkkGAmTuNjzUW9Evpt3QaFkSwxqNH_Kx3W76hVP-hxeycnA5fzqfDfgwMsHApBKi1pvKqWWLjfBqy8DA_Ki4fy_mU7k8jo5ImZTyVJMkBL8b6XmQM_42JCwHL_lMeBXvMZH_N0h6vIBS9kV42Pu5UFmt4LUS9riocT5NIxQZy0Bv7pL3xQKcSET6LIitlvBNURYHQRgvS7DeZo6aBV3r2WeKnyHovhRrxlOAK9d0tgAAAAGNHRvJAA")


