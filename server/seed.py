#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, UserItem, Transaction, Item

def create_users():
    users = []
    for _ in range(40):
        user = User(
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number(),
            city=fake.city(),
            state=fake.state(),
            zip_code=fake.zipcode(),
            user_type=rc([True, False])
        )
        users.append(user)
    return users

def create_items():
    items = []
    for _ in range(100):
        item = Item(
            title=fake.word(),
            price=randint(1, 100)
        )
        items.append(item)
    return items

def create_useritems(users, items):
    useritems = []
    for user in users:
        for _ in range(3):
            item = rc(items)
            useritem = UserItem(
                user_id=user.id,
                item_id=item.id,
                title=item.title,
                price=item.price
            )
            useritems.append(useritem)
    return useritems

def create_transactions(users, useritems):
    transactions = []
    for user in users:
        for useritem in user.useritems:
            for _ in range(3):
                transaction = Transaction(
                    useritem_id=useritem.id,
                    amount=randint(1, 100),
                    giver_id=user.id,
                    receiver_id=rc(users).id,
                    comment=fake.sentence()
                )
                transactions.append(transaction)
    return transactions

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Clearing db...")
        User.query.delete()
        UserItem.query.delete()
        Item.query.delete()
        #Transaction.query.delete()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding items...")
        items = create_items()
        db.session.add_all(items)
        db.session.commit()
        
        print("Seeding useritems...")
        useritems = create_useritems(users, items)
        db.session.add_all(useritems)
        db.session.commit()
        
        print("Seeding transactions...")
        transactions = create_transactions(users, useritems)
        db.session.add_all(transactions)
        db.session.commit()

        print("Done seeding!")
