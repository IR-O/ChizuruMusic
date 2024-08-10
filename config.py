from os import getenv


API_ID = int(getenv("API_ID", "11796331"))
API_HASH = getenv("API_HASH", "a089161b52f234bb90a6eb915551e8c0")
BOT_TOKEN = getenv("BOT_TOKEN", "6110625685:AAEJgFdjFQrGWueA2CuelPFSquaqC33ASI4")
OWNER_ID = int(getenv("OWNER_ID", "6045293810"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6045293810").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Michiko:michiko@michiko.oomgmrd.mongodb.net/?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "BQF0ARUAKBiLdP-Ps4NuECtJZvkh1iUGPzj2w4fMdULUWkwwq5ODOLmuqQpnehYJTaVPu-mB0wmhsq-qeyDSuNyw8F0apS91akx2Qgj1Ofd2Nivb8UCIsHQm4glevawweUcGfDZIdBlZ37RjFQaUU5EoZfQZtcbXGafLCQanRSrekB5qvA37Qe-6vIFrE_4_ae1nkn_-tWheeJF2PjXnEQ0QdVv_O-IRBkP-B-Ykkpd9L5ljSC8ZndcvMwdPcBS-wFsmQeW-gaZkEzCAWfoZsw-4xpVM45vO-GLWqpX5kBPAe53xEEad5B0OxR80ZOJeYKfFW-DEhukQs5KJ2FByD8Hcp_sWKwAAAAGyGtWFAA")


