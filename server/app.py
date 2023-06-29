#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, session
from flask_restful import Resource
from datetime import datetime
from flask import jsonify
# from flask_bcrypt import Bcrypt


# Local imports
from config import app, db, api
from models import User, Trade, Watchlist, OverallPerformance, Site, WatchlistItem, Note, Tag, TradeTag

# bcrypt = Brypt(app)

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
    
    def get(self):
        users = User.query.all()
        return [user.to_dict() for user in users]


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
            session['user_id'] = user.id
            return user.to_dict(), 200

        return {'message': 'Invalid username or password'}, 401

class Logout(Resource):

    def delete(self): # just add this line!
        session['user_id'] = None
        return {'message': '204: No Content'}, 204

api.add_resource(Logout, '/logout')
api.add_resource(UserIdResource, '/users/<int:user_id>')
api.add_resource(UserResource, '/users')
api.add_resource(UserRegistrationResource, '/register')
api.add_resource(UserLoginResource, '/login')


class TradeResource(Resource):
    def get(self, trade_id=None, user_id=None):  
        if trade_id is None and user_id is None:
            return self.get_all_trades()
        elif trade_id is not None:
            return self.get_trade(trade_id)
        elif user_id is not None:
            return self.get_user_trades(user_id)

        
    def get_trade(self, trade_id):
        trade = Trade.query.get(trade_id)
        if trade:
            return trade.to_dict()
        return {'message': 'Trade not found'}, 404
    
    def get_user_trades(self, user_id):
        trades = Trade.query.filter_by(user_id=user_id).all()
        return [trade.to_dict() for trade in trades]

    def patch(self, trade_id):
        trade = Trade.query.get(trade_id)
        if trade:
            data = request.get_json()
            if 'date' in data:
                trade.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if 'entry_time' in data:
                trade.entry_time = datetime.strptime(data['entry_time'], '%H:%M:%S').time()
            if 'exit_time' in data:
                trade.exit_time = datetime.strptime(data['exit_time'], '%H:%M:%S').time()
            if 'symbol' in data:
                trade.symbol = data['symbol']
            if 'long_short' in data:
                trade.long_short = data['long_short']
            if 'quantity' in data:
                trade.quantity = data['quantity']
            if 'entry_price' in data:
                trade.entry_price = data['entry_price']
            if 'exit_price' in data:
                trade.exit_price = data['exit_price']
            if 'pnl' in data:
                trade.pnl = data['pnl']
            if 'notes' in data:
                trade.notes = data['notes']
            db.session.commit()
            return {'message': 'Trade updated successfully'}
        return {'message': 'Trade not found'}, 404
    
    @staticmethod
    def post(user_id):
        # Ensure the user is authenticated
        if not user_id:  # Replace this condition with your authentication logic
            return {'message': 'Unauthorized user'}, 401

        data = request.get_json()
        trade_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        entry_time = datetime.strptime(data['entry_time'], '%H:%M:%S').time()
        exit_time = datetime.strptime(data['exit_time'], '%H:%M:%S').time()

        new_trade = Trade(
            user_id=user_id,
            date=trade_date,
            entry_time=entry_time,
            exit_time=exit_time,
            symbol=data['symbol'],
            long_short=data['long_short'],
            quantity=data['quantity'],
            entry_price=data['entry_price'],
            exit_price=data['exit_price'],
            pnl=data['pnl'],
            notes=data['notes'],
        )
        db.session.add(new_trade)
        db.session.commit()
        return {'message': 'Trade created successfully'}, 201

    def delete(self, trade_id):
        trade = Trade.query.get(trade_id)
        if trade:
            db.session.delete(trade)
            db.session.commit()
            return {'message': 'Trade deleted successfully'}
        return {'message': 'Trade not found'}, 404

    def get_all_trades(self):
        trades = Trade.query.all()
        return [trade.to_dict() for trade in trades]
    
api.add_resource(TradeResource, '/trade', '/trade/<int:trade_id>', '/trade/users/<int:user_id>', endpoint='trade')

class OverallPerformanceResource(Resource):
    def get(self, user_id):
        performances = OverallPerformance.query.filter_by(user_id=user_id).all()
        if performances:
            performance_data = [performance.to_dict() for performance in performances]
            return jsonify(performance_data)
        return jsonify({'message': 'No overall performances found for the specified user ID'}), 404
    
    def put(self, user_id):
        performances = OverallPerformance.query.get(user_id=user_id).all()
        if performances:
            return [performance.to.dict() for performance in performances]
        return {"message": 'Overall performance not found for the user'}, 404
    
    def delete(self, performance_id):
        performance = OverallPerformance.query.get(performance_id)
        if performance:
            db.session.delete(performance)
            db.session.commit()
            return {'message': 'Overall performance deleted successfully'}
        return {'message': 'Overall performance not found'}, 404

api.add_resource(OverallPerformanceResource, '/overallperformance/users/<int:user_id>')


class WatchlistId(Resource):
    def get(self, watchlist_id):
        watchlist = Watchlist.query.get(watchlist_id)
        if watchlist:
            return watchlist.to_dict()
        return {'message': 'Watchlist not found'}, 404
    
    def put(self, watchlist_id):
        watchlist = Watchlist.query.get(watchlist_id)
        if watchlist:
            data = request.get_json()
            watchlist.name = data['name']
            db.session.commit()
            return {'message': 'Watchlist updated successfully'}
        return {'message': 'Watchlist not found'}, 404
    
    def delete(self, watchlist_id):
        watchlist = Watchlist.query.get(watchlist_id)
        if watchlist:
            db.session.delete(watchlist)
            db.session.commit()
            return {'message': 'Watchlist deleted successfully'}
        return {'message': 'Watchlist not found'}, 404


class Watchlist(Resource):
    def get(self):
        watchlists = Watchlist.query.all()
        return [watchlist.to_dict() for watchlist in watchlists]
    
    def post(self):
        data = request.get_json()
        watchlist = Watchlist(name=data["name"])
        db.session.add(watchlist)
        db.session.commit()
        return {'message': 'Watchlist created successfully'}, 201

    def get_user_watchlist(self, user_id):
        watchlists = Watchlist.query.filter_by(user_id=user_id).all()
        return [watchlist.to_dict() for watchlist in watchlists]


api.add_resource(WatchlistId, '/watchlist/<int:watchlist_id>')
api.add_resource(Watchlist, '/watchlist')
api.add_resource(Watchlist, '/user/<int:user_id>/watchlist', endpoint='user_watchlist')

class UserWatchlists(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            watchlists = user.watchlists.all()
            return [watchlist.to_dict() for watchlist in watchlists]
        return {'message': 'User not found'}, 404

api.add_resource(UserWatchlists, '/user/<int:user_id>/watchlists')

class WatchlistResource(Resource):
    def get(self, watchlist_id=None):
        if watchlist_id is None:
            return self.get_all_watchlists()
        else:
            return self.get_watchlist(watchlist_id)

    def get_watchlist(self, watchlist_id):
        watchlist = Watchlist.query.get(watchlist_id)
        if watchlist:
            return watchlist.to_dict()
        return {'message': 'Watchlist not found'}, 404

    def get_all_watchlists(self):
        watchlists = Watchlist.query.all()
        return [watchlist.to_dict() for watchlist in watchlists]

    def post(self):
        data = request.get_json()
        watchlist = Watchlist(name=data["name"])
        db.session.add(watchlist)
        db.session.commit()
        return {'message': 'Watchlist created successfully'}, 201

    def put(self, watchlist_id):
        watchlist = Watchlist.query.get(watchlist_id)
        if watchlist:
            data = request.get_json()
            watchlist.name = data['name']
            db.session.commit()
            return {'message': 'Watchlist updated successfully'}
        return {'message': 'Watchlist not found'}, 404

    def delete(self, watchlist_id):
        watchlist = Watchlist.query.get(watchlist_id)
        if watchlist:
            db.session.delete(watchlist)
            db.session.commit()
            return {'message': 'Watchlist deleted successfully'}
        return {'message': 'Watchlist not found'}, 404

api.add_resource(WatchlistResource, '/watchlist', '/watchlist/<int:watchlist_id>')


class SiteResource(Resource):
    def get(self, site_id):
        site = Site.query.get(site_id)
        if site:
            return site.to_dict()
        return {'message': 'Site not found'}, 404
    
    def put(self, site_id):
        site = Site.query.get(site_id)
        if site:
            data = request.get_json()
            site.name = data['name']
            site.url = data['url']
            db.session.commit()
            return {'message': 'Site updated successfully'}
        return {'message': 'Site not found'}, 404
    
    def delete(self, site_id):
        site = Site.query.get(site_id)
        if site:
            db.session.delete(site)
            db.session.commit()
            return {'message': 'Site deleted successfully'}
        return {'message': 'Site not found'}, 404
    
api.add_resource(SiteResource, '/site/<int:site_id>') 

class NoteResource(Resource):
    def get(self, note_id):
        note = Note.query.get(note_id)
        if note:
            return note.to_dict()
        return {'message': 'Note not found'}, 404
    
    def put(self, note_id):
        note = Note.query.get(note_id)
        if note:
            data = request.get_json()
            note.title = data['title']
            note.content = data['content']
            db.session.commit()
            return {'message': 'Note updated successfully'}
        return {'message': 'Note not found'}, 404
    
    def delete(self, note_id):
        note = Note.query.get(note_id)
        if note:
            db.session.delete(note)
            db.session.commit()
            return {'message': 'Note deleted successfully'}
        return {'message': 'Note not found'}, 404

api.add_resource(NoteResource, '/note/<int:note_id>')

class TagResource(Resource):
    def get(self, tag_id):
        tag = Tag.query.get(tag_id)
        if tag:
            return tag.to_dict()
        return {'message': 'Tag not found'}, 404
    
    def put(self, tag_id):
        tag = Tag.query.get(tag_id)
        if tag:
            data = request.get_json()
            tag.name = data['name']
            db.session.commit()
            return {'message': 'Tag updated successfully'}
        return {'message': 'Tag not found'}, 404
    
    def delete(self, tag_id):
        tag = Tag.query.get(tag_id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
            return {'message': 'Tag deleted successfully'}
        return {'message': 'Tag not found'}, 404
    
api.add_resource(TagResource, '/tag/<int:tag_id>')

class TradeTagResource(Resource):
    def get(self, trade_tag_id):
        trade_tag = TradeTag.query.get(trade_tag_id)
        if trade_tag:
            return trade_tag.to_dict()
        return {'message': 'Trade tag not found'}, 404
    
    def put(self, trade_tag_id):
        trade_tag = TradeTag.query.get(trade_tag_id)
        if trade_tag:
            data = request.get_json()
            trade_tag.trade_id = data['trade_id']
            trade_tag.tag_id = data['tag_id']
            db.session.commit()
            return {'message': 'Trade tag updated successfully'}
        return {'message': 'Trade tag not found'}, 404
    
    def delete(self, trade_tag_id):
        trade_tag = TradeTag.query.get(trade_tag_id)
        if trade_tag:
            db.session.delete(trade_tag)
            db.session.commit()
            return {'message': 'Trade tag deleted successfully'}
        return {'message': 'Trade tag not found'}, 404

api.add_resource(TradeTagResource, '/tradetag/<int:trade_tag_id>')





if __name__ == '__main__':
    app.run(port=5555, debug=True)
