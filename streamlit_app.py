from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy import MetaData, Table, Column, Integer, String
import time


engine = create_engine("mysql+pymysql://root:super_root_password@vmsdt-corentin-chanet.becode.org/test_db", echo=True, future=True)
conn = engine.connect()

meta = MetaData()
meta.reflect(bind=engine)

data = meta.tables['data']


s1 = select(data)


s2 = select(data).where(data.c.EnterpriseNumber == '0201.400.110')


start = time.time()
print(start)
result1 = conn.execute(s1)
print(time.time()-start)
result2 = conn.execute(s2)