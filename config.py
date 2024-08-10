from os import getenv


API_ID = int(getenv("API_ID", "11796331"))
API_HASH = getenv("API_HASH", "a089161b52f234bb90a6eb915551e8c0")
BOT_TOKEN = getenv("BOT_TOKEN", "7260328743:AAE5cdFwgyFp9cYrxvcO1B0MRJrg7S4UMx0")
OWNER_ID = int(getenv("OWNER_ID", "6045293810"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6045293810").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Michiko:michiko@michiko.oomgmrd.mongodb.net/?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "BQG6AIcAHEVMl4zMzjOvu-hLUrkotaGcDGmNbm6ibJOwH1WE6iQCL2lc3NjYxUfmf6GNDXYMoYAirxx0Xi2GYxJ27NOqmc4fR38u7cXLjWHsigsI5kRYDhkhNf2kWlV1KkYkr2sCeFFLBaESqHIwsVhPgP-GzBrVNf83yUOQ-6g_6ej2h20KLm7Vrey1R4sgjLxU4JD3lOT1PrTYAsj1QiubNgO7lbvZzLrutW5H4xPHwS_vimYEARKbvAUGbHiE0dj4yzSdZXi5UwXpTyj6C_u1lK4liK7B1wEdmldWSBZVH6v-tN25fOg3-d2KsHJEoepSb97d2eUxApcdaOKMcOfJ-_DcGAAAAAG4_cSoAA")


