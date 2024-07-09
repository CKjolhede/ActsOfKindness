from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates

from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    #password = db.Column(db.String)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.String, nullable=False)
    user_type = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    #useritems = db.relationship('UserItem', back_populates='user', cascade="delete, delete-orphan")
    
    def __repr__(self):
        return f'<ID: {self.id} | Name {self.first_name} {self.last_name} | Email {self.email}>'
    
class UserItem(db.Model, SerializerMixin):
    __tablename__ = 'useritems'    

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    title = db.Column(db.String)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    #user = db.relationship('User', back_populates='useritems')
    
    @validates('price')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError('Price cannot be negative')
        return price
    
    def __repr__(self):
        return f'<ID: {self.id} | Product Name: {self.title} | User {self.user_id} | Price {self.price}>'
    

class Item(db.Model, SerializerMixin): 
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    @validates('price')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError('Price cannot be negative')
        return price
    
    def __repr__(self):
        return f'<ID: {self.id} | Product Name: {self.name} | Price {self.price}>'
    

    
class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    useritem_id = db.Column(db.Integer, db.ForeignKey('useritems.id'))
    amount = db.Column(db.Float)
    giver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    comment = db.Column(db.String)
    
    giver = db.relationship('User', foreign_keys=[giver_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    #useritem = db.relationship('UserItem', back_populates='transactions')
    
    @validates('amount')
    def validate_amount(self, key, amount):
        if amount < 0:
            raise ValueError('Amount cannot be negative')
        return amount
    
    def __repr__(self):
        return f'<ID: {self.id} | Item {self.useritem_id} | Amount {self.amount} | Receiver {self.receiver_id} | Giver {self.giver_id} | Comment {self.comment}>'

    
