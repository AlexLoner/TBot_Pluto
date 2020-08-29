import sqlalchemy
from sqlalchemy.orm import sessionmaker


# ------------------------------------------------------------------------------------------ #
class InitDB:

    # ----------------------------------------------------------------------------------------
    def __init__(self, db_name, user_name, password):
        self.db = db_name
        self.user = user_name
        self.pwd = password
        self.connection = self.connect()
        self.session = sessionmaker(bind=self.connection.engine)()

    # ----------------------------------------------------------------------------------------
    def connect(self):
        connection = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.pwd}@localhost:3306/', encoding='utf8').connect()
        connection.execute(f"CREATE DATABASE IF NOT EXISTS {self.db}")
        connection.close()

        connection = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.pwd}@localhost:3306/{self.db}', encoding='utf8').connect()
        return connection


# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import configuration as cfg
    db = InitDB(db_name=cfg.db_name, user_name=cfg.user_name, password=cfg.pwd)

