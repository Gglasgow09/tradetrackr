from sqlalchemy_serializer import SerializerMixin

from config import db

# Models go here!

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
        }

    # Relationships
    trades = db.relationship("Trade", backref="user", lazy=True)
    watchlists = db.relationship("Watchlist", backref="user", lazy=True)
    performances = db.relationship(
        "OverallPerformance", backref="user", lazy=True)
    sites = db.relationship("Site", backref="user", lazy=True)
    notes = db.relationship("Note", backref="user", lazy=True)


# Trade Model
class Trade(db.Model):
    __tablename__ = "trades"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    entry_time = db.Column(db.Time, nullable=False)
    exit_time = db.Column(db.Time, nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    long_short = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float, nullable=False)
    pnl = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "entry_time": self.entry_time,
            "exit_time": self.exit_time,
            "symbol": self.symbol,
            "long_short": self.long_short,
            "quantity": self.quantity,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "pnl": self.pnl,
            "notes": self.notes
        }

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tags = db.relationship("TradeTag", backref="trade", lazy=True)


# Watchlist Model
class Watchlist(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
        }

    # Relationship
    symbols = db.relationship("WatchlistItem", backref="watchlist", lazy=True)


# Performance Model
class OverallPerformance(db.Model):
    __tablename__ = "overall_performances"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    portfolio_value = db.Column(db.Integer, nullable=False)
    pnl = db.Column(db.Float, nullable=False)
    roi = db.Column(db.Float, nullable=False)
    win_rate = db.Column(db.Float, nullable=False)
    max_drawdown = db.Column(db.Float, nullable=False)
    trade_duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "portfolio_value": self.portfolio_value,
            "pnl": self.pnl,
            "roi": self.roi,
            "win_rate": self.win_rate,
            "max_drawdown": self.max_drawdown,
            "trade_duration": self.trade_duration,
        }

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# Site Model
class Site(db.Model):
    __tablename__ = "sites"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
        }

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# WatchlistItem Model
class WatchlistItem(db.Model):
    __tablename__ = 'watchlist_items'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    # Relationships
    watchlist_id = db.Column(db.Integer, db.ForeignKey(
        "watchlists.id"), nullable=False)


# Note Model
class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# Tag Model
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    # Relationships
    trades = db.relationship("TradeTag", backref="tag", lazy=True)


# TradeTag Model (Join Table)
class TradeTag(db.Model):
    __tablename__ = 'trade_tags'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    # Relationships
    trade_id = db.Column(db.Integer, db.ForeignKey(
        "trades.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)
