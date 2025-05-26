from os import getenv


API_ID = int(getenv("API_ID", "28542531"))
API_HASH = getenv("API_HASH", "9f4889cd2437d72ede20428c07a909be")
BOT_TOKEN = getenv("BOT_TOKEN", "7953139932:AAFLRe5L0HSdbboNYDKzchLEBFQx4vJrIZA")
OWNER_ID = int(getenv("OWNER_ID", "6045293810"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6045293810").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://nishamusic:Nothing0000@nishamusicbot.dg20jss.mongodb.net/?retryWrites=true&w=majority&appName=NishaMusicBot")
SESSION_STRING = getenv("SESSION_STRING", "BQAf70YAVf30uzzX36VSAjwLDGMJq1hF6vXK0CNsnW_9tZcFu_c5FK13yVVKMHUNBFnX3GhHzNRkE4E-GmARk6sK_K8n9kEj_TEpTe5rPDkqViEqO4K-3MQiijl0-84kgPhrG9TTQzHuBqhJ6Nn0SDHe0QaE1_3EP3O3AJgRHZdkLueW9iqHXaMjrE2GA06RWncL98r5J90wIjPa2zrdYKwi9stN-RgqFexLuXMT2n0PEG-fxXnKdQXkV_C98UJjdT6y5KinDpSCDFn0D2Ctwdd69R5LIE7qm5Ufs4Zk2x5KhBfMU5JO_75r-OWAlME-okodxdd35tS3XNYHuEIHvX0dpS23agAAAAGExJmlAA")


