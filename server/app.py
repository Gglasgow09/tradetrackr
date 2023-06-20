#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import User, Trade, Watchlist, OverallPerformance, Site, WatchlistItem, Note, Tag, TradeTag

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
    def get(self, trade_id):
        trade = Trade.query.get(trade_id)
        if trade_id:
            return trade.to_dict()
        return {'message': 'Trade not found'}, 404
    
    def put(self, trade_id):
        print ('PUT request received for trade ID', trade_id)
        trade= Trade.query.get(trade_id)
        if trade:
            print ("Trade found:", trade.to_dict())
            data = request.get_json()
            print('Received data:', data)
            db.session.commit()
            print('Trade updated successfully')
            return{'message':'Trade updated successfully'}
        print('Trade not found')
        return {"message":"Trade not found"}, 404
    
    def delete(self, trade_id):
        print('DELETE request received for trade ID', trade_id)
        trade = Trade.query.get(trade_id)
        if trade:
            print("Trade found:", trade.to_dict())
            db.session.delete(trade)
            db.session.commit()
            print('Trade deleted successfully')
            return {'message': 'Trade deleted successfully' }
        print("Trade not found")
        return {'message': 'Trade not found'}, 404

api.add_resource(TradeResource, '/trade/<int:trade_id>')

class WatchlistId(Resource):
    def get (self, watchlist_id):
        watchlist = Watchlist.query.get(watchlist_id)
        if watchlist:
            return watchlist.to_dict()
        return {'message': 'Watchlist not found'}, 404
    
    def put (self, watchlist_id,):
        print('PUT request received for watchlist id', watchlist_id)
        watchlist = Watchlist.query.get(watchlist_id)
        if watchlist:
            print('Watchlist found:', watchlist.to_dict())
            data= request.get_json()
            print ("Received watchlist data", data)
            watchlist.name = data["name"]
            db.session.commit()
            print ("Watchlist updated successfully")
            return {"message": "Watchlist updated successfully "}
        print("Watchlist not found")
        return {'message': 'Watchlist not found'}, 404
    
    def delete(self, watchlist_id):
        print ("DELETE request received for watchlist ID", watchlist_id)
        watchlist = Watchlist.query.get(watchlist_id)
        if watchlist:
            print('Watchlist found', watchlist.to_dict())
            db.session.delete(watchlist)
            db.session.commit()
            print("Watchlist deleted successfully")
            return{'message': 'Watchlist deleted successfully'}
        print('Watchlist not found')
        return{'message':"Watchlist not found"}, 404

api.add_resource(Watchlist, '/watchlist/<int:watchlist_id>')

class Watchlist(Resource):
    def get(self):
        watchlist = Watchlist.query.all()
        return [list.to_dict() for list in watchlist]
    
    def post (self):
        print ("POST request received")
        data = request.get_json()
        print ("Received data:", data)
        watchlist = Watchlist (name=data["name"])
        db.session.add(watchlist)
        db.session.commit()

        print ('Watchlist created successfully')
        return {'message': 'Watchlist created successfully'}

api.add_resource(Watchlist, '/watchlist')

class OverallPerformance(Resource):
    def get (self):
        pass

api.add_resource(OverallPerformance, '/overallperformance')





if __name__ == '__main__':
    app.run(port=5555, debug=True)
