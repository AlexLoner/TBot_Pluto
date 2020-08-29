"""
    Main file to run telegram bot
"""
import configuration as cfg
from bot_file import Tbot
from db_files.db_connect import InitDB
from db_files.table import THistory


if __name__ == "__main__":

    dbase = InitDB(db_name="test_db", user_name=cfg.user_name, password=cfg.pwd)
    table = THistory(base=dbase)

    bot = Tbot(db_table=table)
    bot.loop(1.0)
