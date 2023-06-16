#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import User, Trade, Watchlist, OverallPerformance, Site, WatchlistItem, Note, Tag, TradeTag

# Views go here!
class UserIdResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.to_dict()
        return {'message': 'User not found'}, 404

    def put(self, user_id):
        # Update user profile
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            user.username = data['username']
            user.password = data['password']
            user.email = data['email']
            db.session.commit()
            return {'message': 'User updated successfully'}
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}
        return {'message': 'User not found'}, 404


class UserResource (Resource):
    def post(self):
        data = request.get_json()
        user = User(username=data["username"],
                    email=data['email'], password=data["password"])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201


class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()
        user = User(username=data['username'],
                    email=data['email'], password=data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registration successfully'}, 201


class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data["password"]

        user = User.query.filter_by(
            username=username, password=password).first()

        if user:
            return {'message': 'Login successful'}, 200

        return {'message': 'Invalid username or password'}, 401


api.add_resource(UserIdResource, '/users/<int:user_id>')
api.add_resource(UserResource, '/users')
api.add_resource(UserRegistrationResource, '/register')
api.add_resource(UserLoginResource, '/login')

class TradeResource(Resource):
    pass

api.add_resource(TradeResource, '/trade')




if __name__ == '__main__':
    app.run(port=5555, debug=True)
