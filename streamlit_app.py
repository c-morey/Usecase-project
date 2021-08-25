from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.sql.expression import func
from sqlalchemy import insert
import time

engine = create_engine("mysql+pymysql://knn:knn@10.0.0.193/clean_db", echo=True, future=True)
Session = sessionmaker(engine)

dummy_batch = [{'id': i, 'algo_key': '19883789739837090930940'} for i in range(1,50000)]

def write_batch(batch):

    meta = MetaData()
    meta.reflect(bind=engine)
    results = meta.tables['results']

    with engine.connect() as conn:
        _ = conn.execute(insert(results), batch)
        conn.commit()

def fetch_records(Session, EnterpriseNumber:str):

    meta = MetaData()
    meta.reflect(bind=engine)
    data = meta.tables['data']

    input_session = Session()

    stmnt = select(data).where(data.c.EnterpriseNumber == EnterpriseNumber)

    rows = input_session.execute(stmnt).all()

    input_session.close()

    if rows:
        return rows
    else:
        return False

def fetch_key(Session, input_rows, type_of_address:str):

    meta = MetaData()
    meta.reflect(bind=engine)
    results = meta.tables['results']

    input_session = Session()

    key = ()

    filtered_rows = []

    # Check for the type_of_address priority
    if any(row[3] == type_of_address for row in input_rows):
        for row in input_rows:
            if row[3] == type_of_address or row[3] == '':
                filtered_rows.append(row)
    else:
        filtered_rows = input_rows

    # Check if the denomination is longest and try to fetch the key from id
    for row in filtered_rows:
        if all(len(row[2]) >= len(r[2]) for r in filtered_rows):
            stmnt = select(results).where(results.c.id == row[0])
            key = input_session.execute(stmnt).one_or_none()
            break

    input_session.close()

    if key:
        return key

    else:
        return False

def fetch_batch(Session):

    check_session = Session()
    last_id = _check_results(check_session)
    check_session.close()

    fetch_session = Session()

    meta = MetaData()
    meta.reflect(bind=engine)
    data = meta.tables['data']

    stmnt = select(data).where(data.c.id > last_id).limit(50000)

    batch = fetch_session.execute(stmnt).all()

    fetch_session.close()

    return batch

def _check_results(check_session):

    meta = MetaData()
    meta.reflect(bind=engine)
    results = meta.tables['results']
    try:
        get_last_id = select(func.max()).select_from(results.c.id)
        last_id = check_session.execute(get_last_id).scalar_one()
    except:
        last_id = 0

    return last_id

def reset_results(Session, length_of_key):

    meta = MetaData()
    meta.reflect(bind=engine)

    reset_session = Session()

    try:
        meta.tables['results'].drop(engine)

    except:
        pass

    meta = MetaData()
    meta.reflect(bind=engine)

    results = Table(
       'results', meta,
       Column('id', Integer, primary_key = True),
       Column('algo_key', String(length_of_key)),
    )

    meta.create_all(engine)
    reset_session.close()

start = time.time()
reset_results(Session, 50)
# write_batch(dummy_batch)
# input_ = fetch_records(Session, "0201.400.110")
# output_ = fetch_key(Session, input_, 'REGO')
print(time.time()-start)

# data = meta.tables['data']
#
# s1 = select(data).limit(1000)
# s2 = select(data).where(data.c.EnterpriseNumber == '0201.400.110')

# start = time.time()
# result1 = mysession.execute(s1)
# print(time.time()-start)
# result2 = mysession.execute(s2)