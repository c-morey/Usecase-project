from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData, Table, Column, Integer, String


meta = MetaData()
Base = declarative_base()

def create_Key_schema(key_length):

    class Key(Base):
        __tablename__ = 'results'
        id = Column(Integer, primary_key=True)
        enterprise_number = Column(Integer)
        key = Column(String(key_length))

        def __repr__(self):
            return "<Key(id='%s', enterprise_number='%s', key='%s')>" % (self.id, self.enterprise_number, self.key)

    return Key