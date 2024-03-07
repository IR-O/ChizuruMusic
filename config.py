from os import getenv


API_ID = int(getenv("API_ID", "11796331"))
API_HASH = getenv("API_HASH", "a089161b52f234bb90a6eb915551e8c0")
BOT_TOKEN = getenv("BOT_TOKEN", "5663640542:AAH5S36XQEVWcpvsdeDWNFY5E6pDxNeTP2Y")
OWNER_ID = int(getenv("OWNER_ID", "6045293810"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6045293810").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://pikachu:randi@cluster0.tndvlel.mongodb.net/?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "BQCz_2sAVpuAnp_5fom4qxYpCUmYjfK5wYqPx_a6ivgJMyjhmMZQXvR77vkaU-iqRRD1yLCU5JUwK-ONr2tPmiPc4FmAQdIgSt8ceTLdWkuxsEjfuyck6gP8elz9OSkcMieMTxmu73Mi2UuHXQV_Z7fPSI3y4xElH5CsZE_susNm-OSmqpgCIFaRC0_7xoTPqFv372b79wzukcn3VCtPuHVTXrdVWbFBhX8-GeAQ8ibNx7youmnhVqQYfS3tOBDY82kx04Ewl9zWOV50CVhRgzBcj4n8hyF3ibFNU3oh0yHEZhVHg6QSpWe6etjZmvAGq8mvDRWZVZFdSL6TK818ETqJ_H6l7AAAAAGRxJUeAA")


