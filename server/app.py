#!/usr/bin/env python3

# Standard library imports
from models import db, User, UserItem, Transaction, Item
from werkzeug.exceptions import NotFound, Unauthorized
from flask_restful import Resource
from flask import make_response, jsonify, request, session, abort
from config import app, db, api, bcrypt
import ipdb


class Users(Resource):
    def get(self):
        receivers = [r.to_dict() for r in User.query.filter(User.user_type == True)]
        return make_response(receivers, 200)

    def post(self):
        data = request.get_json()
        try:
            new_user = User(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password_hash=data['password'],
                phone=data['phone'],
                street=data['street'],
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


@app.route("/login", methods=["POST"])
def login():
    user = User.query.filter(User.email == request.get_json()["email"]).first()
    if user and user.authenticate(request.get_json()["password"]):
        session["user_id"] = user.id 
        return make_response(user.to_dict(), 200)
    else:
        raise Unauthorized
    
@app.route("/authorized")
def authorized():
    if user := User.query.filter(User.id == session.get("user_id")).first():
        return make_response(user.to_dict(), 200)
    else:
        raise Unauthorized

@app.route("/logout", methods=["DELETE"])
def logout():
    session.clear()
    return make_response({}, 204)
    

class UserByID(Resource):
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        return make_response(user.to_dict(), 200)
    
    #def patch(self, id):
    #    data = request.get_json()
    #    user = User.query.filter(User.id == id).first()
    #    user.first_name = data['first_name']
    #    user.last_name = data['last_name']
    #    user.phone = data['phone']
    #    user.email = data['email']
    #    user.street = data['street']
    #    user.city = data['city']
    #    user.state = data['state']
    #    user.zip_code = data['zip_code']
    #    user.user_type = data['user_type']
    
    def patch(self,id):
        user=db.session.get(User, id)
        if not user:
            return make_response({'error': 'User not found'}, 404)
        form_json = request.get_json()
        for key, value in form_json.items():
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return make_response(user.to_dict(), 202)    
    
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
    
class UserItems(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_useritem = UserItem(
            user_id=data['user_id'],
            item_id=data['item_id'],
            status=data['status']
        )
        except ValueError as e:
            abort(422, e.args[0])
            
        db.session.add(new_useritem)
        db.session.commit()
        return make_response(new_useritem.to_dict(), 201)
    
api.add_resource(UserItems, '/useritems')

class UserItemsByID(Resource):
    def get(self, id):
        useritems = [i.to_dict() for i in UserItem.query.filter(UserItem.id == id).all()]
        return make_response(useritems, 200)
    
    def delete(self, id):
        useritem = UserItem.query.filter(UserItem.id == id).first()
        db.session.delete(useritem)
        db.session.commit()
        return make_response('', 204)
    
api.add_resource(UserItemsByID, '/useritems/<int:id>')
    
class TransactionsByUserId(Resource):    
    def get(self, id):
        transactions = [t.to_dict() for t in Transaction.query.filter(Transaction.user_id == id).all()]
        return make_response(transactions, 200)
    
    def post(self, id):
        data = request.get_json()
        transaction = Transaction(
            useritem_id=data['useritem_id'],
            user_id=id,
            comment=data['comment']
        )
        db.session.add(transaction)
        db.session.commit()
        return make_response(transaction.to_dict(), 201)
    
api.add_resource(TransactionsByUserId, '/transactions/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)


