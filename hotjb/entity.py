from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HotJBDictionary(Base):
    '''
    '''

    __tablename__ = 'hjb_dictionary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, nullable=False, unique=True)
    create_at = Column(DateTime, nullable=False)


class HotJBEntity:
    '''
    '''

    __engines__ = {}

    def __init__(self, url):
        '''
        '''

        self.url = url
        self.engine = self.get_engine(url)
        self.smaker = sessionmaker(bind=self.engine)

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def make_session(self):
        return self.smaker()

    @classmethod
    def get_engine(cls, url):
        '''
        '''

        if url not in cls.__engines__:
            engine = create_engine(url)
            cls.__engines__[url] = engine
        return cls.__engines__[url]

            
