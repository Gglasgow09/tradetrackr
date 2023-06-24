#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, session
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
    def get(self, trade_id):
        trade = Trade.query.get(trade_id)
        if trade_id:
            return trade.to_dict()
        return {'message': 'Trade not found'}, 404
    
    def put(self, trade_id):
        print ('PUT request received for trade ID', trade_id)
        trade= Trade.query.get(trade_id)
        if trade:
            data = request.get_json()
            trade.date = data['date']
            trade.entry_time = data['entry_time']
            trade.exit_time = data['exit_time']
            trade.symbol = data['symbol']
            trade.long_short = data['long_short']
            trade.quantity = data['quantity']
            trade.entry_price = data['entry_price']
            trade.exit_price = data['exit_price']
            trade.pnl = data['pnl']
            trade.notes = data['notes']
            db.session.commit()
            return {'message': 'Trade updated successfully'}
        return {'message': 'Trade not found'}, 404
    
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

api.add_resource(TradeResource, '/trade/<int:trade_id>')
api.add_resource(TradeResource, '/trade', endpoint='all_trades')

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

api.add_resource(WatchlistId, '/watchlist/<int:watchlist_id>')

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

api.add_resource(Watchlist, '/watchlist')

class OverallPerformance(Resource):
    def get(self, performance_id):
        performance = OverallPerformance.query.get(performance_id)
        if performance:
            return performance.to_dict()
        return {'message': 'Overall performance not found'}, 404
    
    def put(self, performance_id):
        performance = OverallPerformance.query.get(performance_id)
        if performance:
            data = request.get_json()
            performance.metric1 = data['metric1']
            performance.metric2 = data['metric2']
            performance.metric3 = data['metric3']
            db.session.commit()
            return {'message': 'Overall performance updated successfully'}
        return {'message': 'Overall performance not found'}, 404
    
    def delete(self, performance_id):
        performance = OverallPerformance.query.get(performance_id)
        if performance:
            db.session.delete(performance)
            db.session.commit()
            return {'message': 'Overall performance deleted successfully'}
        return {'message': 'Overall performance not found'}, 404

api.add_resource(OverallPerformance, '/overallperformance')

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

class WatchlistItemResource(Resource):
    def get(self, item_id):
        item = WatchlistItem.query.get(item_id)
        if item:
            return item.to_dict()
        return {'message': 'Watchlist item not found'}, 404
    
    def put(self, item_id):
        item = WatchlistItem.query.get(item_id)
        if item:
            data = request.get_json()
            item.watchlist_id = data['watchlist_id']
            item.symbol = data['symbol']
            item.notes = data['notes']
            db.session.commit()
            return {'message': 'Watchlist item updated successfully'}
        return {'message': 'Watchlist item not found'}, 404
    
    def delete(self, item_id):
        item = WatchlistItem.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return {'message': 'Watchlist item deleted successfully'}
        return {'message': 'Watchlist item not found'}, 404

api.add_resource(WatchlistItemResource, '/watchlistitem/<int:item_id>')

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
