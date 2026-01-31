#!/usr/bin/python3
from app.db import db
from app.models.user import User


class UserRepository:
    def add(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def get(self, user_id):
        return User.query.get(user_id)

    def get_all(self):
        return User.query.all()

    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def update(self, user):
        db.session.commit()
        return user

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
