from data.users import User
from data import db_session


db_session.global_init("db/almed.sqlite")
session = db_session.create_session()
user = User(email='admin@admin.ru')
user.set_password('admin')
session.add(user)
session.commit()