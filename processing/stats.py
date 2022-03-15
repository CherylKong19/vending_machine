from sqlalchemy import Column, Integer, String, DateTime 
from base import Base 
class Stats(Base): 
    """ Processing Statistics """ 
 
    __tablename__ = "stats" 
 
    id = Column(Integer, primary_key=True) 
    sanitizer_quantity = Column(Integer, nullable=False) 
    sanitizer_price = Column(Integer, nullable=False) 
    mask_quantity = Column(Integer, nullable=True) 
    mask_price = Column(Integer, nullable=True)  
    last_updated = Column(String(250), nullable=False) 
 
    def __init__(self, sanitizer_quantity, sanitizer_price, 
mask_quantity, mask_price, last_updated): 
        """ Initializes a processing statistics objet """ 
        self.sanitizer_quantity = sanitizer_quantity 
        self.sanitizer_price = sanitizer_price 
        self.mask_quantity = mask_quantity 
        self.mask_price = mask_price 
        self.last_updated = last_updated 
 
    def to_dict(self): 
        """ Dictionary Representation of a statistics """ 
        dict = {} 
        dict['sanitizer_quantity'] = self.sanitizer_quantity 
        dict['sanitizer_price'] = self.sanitizer_price 
        dict['mask_quantity'] = self.mask_quantity 
        dict['mask_price'] = self.mask_price 
        dict['last_updated'] = self.last_updated 
 
        return dict