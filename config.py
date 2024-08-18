from os import getenv


API_ID = int(getenv("API_ID", "28542531"))
API_HASH = getenv("API_HASH", "9f4889cd2437d72ede20428c07a909be")
BOT_TOKEN = getenv("BOT_TOKEN", "6365132039:AAF48I0KgZe4cyHmhMiRx_K634u6BEKApDQ")
OWNER_ID = int(getenv("OWNER_ID", "6045293810"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6045293810").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Michiko:michiko@michiko.oomgmrd.mongodb.net/?retryWrites=true&w=majority")
SESSION_STRING = getenv("SESSION_STRING", "BQE07uIAu2lugLfRpdmxPZKzXODuAXSozfMcUsCw-XAJ5zZBj-NWmwSqSqAubVIR4FN9xVob_4GR6E4yJ__K5axvcQQyKdCikFytYIzCahODagk38KM8Q9Q10LcyLTYqGtFZURvqz6jrD4V34mquIBHhl_FHwl8zhgP3WLIkmeHGMIEdTRIqokNA5xB1D2ze2ArIiN9oubAw-eVPfSSIo5rU1VFYya8zUqjtRNd4UX43YaRh55bPaOWKU47AJQrK4x5Q1i7bepWNutZYS6-RFFmJ5gOAOcmfZMPcT9u9nemNgpeA7yWy3ANQHoBs2BjVuF27UvEJPkHkGm3UWdICFRefgIJApwAAAAGxC4UDAA")


