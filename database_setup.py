from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    category = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)


class Items(Base):
    __tablename__ = 'items'

    item = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)

    # this serialize function makes us able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):

        return {
            'item': self.item,
            'description': self.description,
            'id': self.id,

        }


engine = create_engine('sqlite:///project3rd.db')


Base.metadata.create_all(engine)

print "database was set up"
