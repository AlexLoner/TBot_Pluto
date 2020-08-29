import sqlalchemy
from db_files.db_connect import InitDB
from db_files.entity import Requests, Base


# ------------------------------------------------------------------------------------------ #
class THistory:

    # ----------------------------------------------------------------------------------------
    def __init__(self, base: InitDB):
        self.base = base
        self.create_table(Requests.__tablename__)

    # ----------------------------------------------------------------------------------------
    def create_table(self, name):
        '''Create a table called name in db if its not exists'''
        if not self.base.connection.engine.dialect.has_table(self.base.connection.engine, name):
            Base.metadata.tables[name].create(self.base.connection.engine)

    # ----------------------------------------------------------------------------------------
    def add_request(self, req):
        self.base.session.add(req)
        self.check(req.telegram_id)
        self.base.session.commit()

    # ----------------------------------------------------------------------------------------
    def delete_request(self, lower_id):
        self.base.session.query(Requests).filter(Requests.id < lower_id).delete()
        self.base.session.commit()

    # ----------------------------------------------------------------------------------------
    def show_history(self, telegram_id):
        return self.base.session.query(Requests).filter(Requests.telegram_id == telegram_id).all()

    # ----------------------------------------------------------------------------------------
    def check(self, telegram_id):
        """ Checking that only 10 requests from one user are stored"""
        lst = self.show_history(telegram_id)
        if len(lst) > 10:
            lower_id = lst[1].id
            self.delete_request(lower_id)


# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import configuration as cfg

    db = InitDB(db_name="test_db", user_name=cfg.user_name, password=cfg.pwd)
    table = THistory(base=db)

