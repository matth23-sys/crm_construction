from decouple import config

CRON_TOKEN = config("CRON_TOKEN", default="")