#!/usr/bin/env python3

# Standard library imports
from models import db, User, UserItem, Transaction, Item
from flask_restful import Resource
from flask import Flask, make_response, jsonify, request, session, abort
from config import app, db, api


class Users(Resource):
    def get(self):
        receivers = [r.to_dict() for r in User.query.filter(User.user_type == True).all()]
        return make_response(receivers, 200)

    def post(self):
        data = request.get_json()
        try:
            new_user = User(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                city=data['city'],
                state=data['state'],
                zip_code=data['zip_code'],
                user_type=data['user_type']
            )
        except ValueError as e:
            abort(422, e.args[0])
            
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return make_response(new_user.to_dict(), 201)
    
api.add_resource(Users, '/users', "/signup")

class UserByID(Resource):
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        return make_response(user.to_dict(), 200)
    
    def patch(self, id):
        data = request.get_json()
        user = User.query.filter(User.id == id).first()
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.phone = data['phone']
        user.city = data['city']
        user.state = data['state']
        user.zip_code = data['zip_code']
        user.user_type = data['user_type']
        
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 200)
    
    def delete(self, id):
        user = User.query.filter(User.id == id).first()
        db.session.delete(user)
        db.session.commit()
        return make_response('', 204)
    
api.add_resource(UserByID, '/user/<int:id>')

class Items(Resource):
    def get(self):
        items = [i.to_dict() for i in Item.query.all()]
        return make_response(items, 200)
    
api.add_resource(Items, '/items')

class ItemById(Resource):
    def get(self, id):
        item = Item.query.filter(Item.id == id).first()
        return make_response(item.to_dict(), 200)
    
api.add_resource(ItemById, '/item/<int:id>')
    
    

class UserItemsByID(Resource):
    def get(self, id):
        useritems = [i.to_dict() for i in UserItem.query.filter(UserItem.user_id == id).all()]
        return make_response(useritems, 200)
    
    def post(self, id):
        data = request.get_json()
        useritem = UserItem(
            user_id=id,
            item_id=data['item_id'],
            title=data['title'],
            price=data['price']
        )
        db.session.add(useritem)
        db.session.commit()
        return make_response(useritem.to_dict(), 201)
    
    def delete(self, id):
        useritem = UserItem.query.filter(UserItem.id == id).first()
        db.session.delete(useritem)
        db.session.commit()
        return make_response('', 204)
    
api.add_resource(UserItemsByID, '/useritems/<int:id>')
    
class TransactionsById(Resource):    
    def get(self, id):
        transactions = [t.to_dict() for t in Transaction.query.filter(Transaction.user_id == id).all()]
        return make_response(transactions, 200)
    
    def post(self, id):
        data = request.get_json()
        transaction = Transaction(
            useritem_id=data['useritem_id'],
            amount=data['amount'],
            giver_id=id,
            receiver_id=data['receiver_id'],
            comment=data['comment']
        )
        db.session.add(transaction)
        db.session.commit()
        return make_response(transaction.to_dict(), 201)
    
api.add_resource(TransactionsById, '/transactions/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

#import requests

#payload = { 'api_key': 'afede348128295643d0b3ebd1bd5b9c3', 'query': 'sweatshirts', 'device_type': 'desktop', 'country_code': 'us', 'follow_redirect': 'false', 'autoparse': 'true', 'tld': 'com' }
#r = requests.get('https://api.scraperapi.com/structured/amazon/search', params=payload)
#print(r.text)
