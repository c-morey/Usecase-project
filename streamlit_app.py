from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import declarative_base

engine = create_engine("mysql+pymysql://root:super_root_password@vmsdt-corentin-chanet.becode.org/test_db", echo = True, future= True)
Session = sessionmaker(bind=engine, future=True)


