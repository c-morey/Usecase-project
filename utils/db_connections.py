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
        raise Exception("This EnterpriseNumber could not be found in the Database")

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
        raise Exception("The key for this record has not been generated yet")

def fetch_batch(Session, batch_number=1, offset=0):

    floor = offset + ((batch_number-1) * 50000)

    fetch_session = Session()

    meta = MetaData()
    meta.reflect(bind=engine)
    data = meta.tables['data']

    stmnt = select(data).where(floor < data.c.id).limit(50000)

    batch = fetch_session.execute(stmnt).all()

    fetch_session.close()

    return batch

def check_results(Session):

    check_session = Session()
    meta = MetaData()
    meta.reflect(bind=engine)
    results = meta.tables['results']
    try:
        get_last_id = select(func.max()).select_from(results.c.id)
        last_id = check_session.execute(get_last_id).scalar_one()
    except:
        last_id = 0
    check_session.close()
    return last_id

def reset_results(Session, length_of_key=66):

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