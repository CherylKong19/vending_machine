from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Mask(Base):
    """ mask """

    __tablename__ = "mask"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(250), nullable=False)
    color = Column(String(250), nullable=False)
    size = Column(String(250), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, transaction_id, color, size, quantity, price, trace_id):
        """ Initializes a mask transaction  reading """
        self.transaction_id = transaction_id
        self.color = color
        self.size = size
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.quantity = quantity
        self.price = price
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a mask transaction """
        dict = {}
        dict['id'] = self.id
        dict['transaction_id'] = self.transaction_id
        dict['color'] = self.color
        dict['quantity'] = self.quantity
        dict['price'] = self.price
        dict['size'] = self.size
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict
