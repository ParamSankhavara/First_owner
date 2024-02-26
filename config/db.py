from sqlalchemy import create_engine,NullPool
from sqlalchemy.orm import sessionmaker
import os

DB_DRIVER = "mysql+pymysql"
if os.getenv('DB_ENV') == 'pro':
    DB_USER = 'mysql_database'
    DB_PASSWORD = 'db1200'
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_NAME = 'first_owner'
else:
    DB_USER = 'mysql_database'
    DB_PASSWORD = 'db1200'
    DB_HOST = '65.2.125.31'
    DB_PORT = 3306
    DB_NAME = 'first_owner'


print("Connecting to db..........",'%s://%s:%s@%s:%s/%s' % (DB_DRIVER,DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME))
engine = create_engine('%s://%s:%s@%s:%s/%s' % (DB_DRIVER,DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME),poolclass=NullPool,pool_pre_ping=True)

Session = sessionmaker(bind=engine)
db1 = Session()