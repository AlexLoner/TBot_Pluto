from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# ------------------------------------------------------------------------------------------ #
class Requests(Base):

    __tablename__ = 'users_requests'
    __table_args__ = {'mysql_charset': 'utf8' }

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False)
    req_date = Column(DateTime, nullable=False)
    origin_link = Column(String(2000), nullable=False)
    short_link = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(150), nullable=True)

    # ----------------------------------------------------------------------------------------
    def __init__(self, telegram_id, chat_id, req_date, origin_link, short_link, first_name, last_name=None):
        self.telegram_id = telegram_id
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.req_date = req_date
        self.origin_link = origin_link
        self.short_link = short_link

    # ----------------------------------------------------------------------------------------
    def __repr__(self):
        return f"Requests({self.telegram_id}, {self.chat_id}, {self.req_date}, {self.origin_link}, " \
               f"{self.short_link}, {self.first_name}, {self.last_name})"
