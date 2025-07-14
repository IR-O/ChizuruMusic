from os import getenv


API_ID = int(getenv("API_ID", "28542531"))
API_HASH = getenv("API_HASH", "9f4889cd2437d72ede20428c07a909be")
BOT_TOKEN = getenv("BOT_TOKEN", "5964346248:AAGtWqikxHyNjT9qKPMpEeN7rSqhy1XWWwc")
OWNER_ID = int(getenv("OWNER_ID", "6045293810"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6045293810").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://String:iro@string.bfl5lcm.mongodb.net/?retryWrites=true&w=majority&appName=String")
SESSION_STRING = getenv("SESSION_STRING", "BQDEFKsAgiokuBQL9u39ZqrvaCaQO3LKSggOy37pSrHZT5zVqgjq142NHplMweczk3QX9d7zyZtJRnkbAf68dI1UwZL6Zt8E-easqg2itztgxj1x9va6IZsqNUh9L6g8vo56oMeRC9zQ2B3ZIKQUAr-SQmbwKy4yaoZNV2dLrOa0CUC_F1gDWEcLdk-hdoUsQIfEeKVpVKJz8Qgj9YEd8YNgHjbt-TFE5WGcLhV12kjkCw8PCsx1sbALnoNk22TVrhc8HJQRuB5gdJxJeer8a1B4JBrSso6B84LPI0SjAHgu-xCiDI8Mi3h4YhM4c5EN-ajrSJZczpCYkp633E6eYan31cr2FgAAAAHmorCNAA")


