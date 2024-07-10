from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from config import bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.String, nullable=False)
    user_type = db.Column(db.Boolean)
    
    useritems = db.relationship('UserItem', back_populates='user')
    transactions = db.relationship('Transaction', back_populates='user')
    
    serialize_rules = ('-useritems.user', '-transactions.user', '-useritems.transaction', '-transactions.useritem', '-useritems.item')
    
    
    @validates('password_hash')
    def validate_password(self, key, password_hash):
        if not password_hash:
            raise ValueError('Password cannot be left blank')
        return password_hash
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf8"))
        self._password_hash = password_hash.decode("utf8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf8"))
    
    def __repr__(self):
        return f'<ID: {self.id} | Name {self.first_name} {self.last_name} | Email {self.email}>'
    
class UserItem(db.Model, SerializerMixin):
    __tablename__ = 'useritems'    

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='useritems')
    
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship('Item', back_populates='useritems')
    
    transaction = db.relationship('Transaction', back_populates='useritem')
    
    serialize_rules = ('-item', '-user.useritems', '-transaction.useritem', '-user.transactions', '-transaction.user')
    
    def __repr__(self):
        return f'<ID: {self.id} | Product Name: {self.title} | User {self.user_id} | Price {self.price}>'
    

class Item(db.Model, SerializerMixin): 
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    category = db.Column(db.String)
    price = db.Column(db.Float)
    
    useritems = db.relationship('UserItem', back_populates='item')
    
    serialize_rules = ('-useritems.item', '-useritems', '-transactions', '-users')
    
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
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    comment = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='transactions')
    
    useritem_id = db.Column(db.Integer, db.ForeignKey('useritems.id'))
    useritem = db.relationship('UserItem', back_populates='transaction')
    
    serialize_rules = ('-useritem.transaction', '-useritems.item', '-user.transactions', '-user.useritems', '-useritems.user')
    
    def __repr__(self):
        return f'<ID: {self.id} | Item {self.useritem.title} | Comment {self.comment}>'

    
