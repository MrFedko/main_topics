import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "topics app"
    DB_NAME = "topics.db"
    PROJECT_DESCRIPTION = "Education app for restaurant staff"

    BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
    EMAIL_CONTROLLER = str(os.getenv("EMAIL_CONTROLLER"))
    SHEET_ID = str(os.getenv("SHEET_ID"))

    admins = [
        os.getenv("ADMIN_ID"),
    ]

    worksheet_ids = {
    "Salone pasta&bar": 1926688551,
    "Goose Goose ": 664085816,
    "ХИТЧ": 145386066,
    }

    rests_by_worksheet_ids = {
        1926688551: "Salone pasta&bar",
        664085816: "Goose Goose",
        145386066: "ХИТЧ",
    }



    PROJECT_PATH = "//Users/mac/Desktop/my_projects/main_topics/main_topics/"
    CREDS_PATH = PROJECT_PATH + os.getenv("CREDS_PATH")

    # PROJECT_PATH = "/home/salone_spb_education/"
    DB_PATH = PROJECT_PATH + DB_NAME

settings = Settings()
