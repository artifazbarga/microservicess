from sqlalchemy.orm import sessionmaker
from services.tabledef import *
from services.tabledef import User
engine = create_engine('sqlite:///database.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("admin", "password")
session.add(user)

# commit the record the database
session.commit()

session.commit()
