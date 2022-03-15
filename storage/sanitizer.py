from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Sanitizer(Base):
    """ sanitizer """

    __tablename__ = "sanitizer"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(250), nullable=False)
    scent = Column(String(250), nullable=False)
    volume = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, transaction_id, scent, volume, quantity, price, trace_id):
        """ Initializes a sanitizer transaction reading """
        self.transaction_id = transaction_id
        self.scent = scent
        self.volume = volume
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.quantity = quantity
        self.price = price
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a sanitizer transaction """
        dict = {}
        dict['id'] = self.id
        dict['transaction_id'] = self.transaction_id
        dict['scent'] = self.scent
        dict['quantity'] = self.quantity
        dict['price'] = self.price
        dict['volume'] = self.volume
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict
