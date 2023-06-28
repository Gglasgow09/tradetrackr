from sqlalchemy.orm import validates
from enum import Enum
from config import db
# from sqlalchemy.ext.hybrid import hybrid_property
# from app import bcrypt

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

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Failed email validation")
        return address

    @validates('password')
    def validate_password(self, key, password):
        if not any(c.isupper() for c in password):
            raise ValueError("Password must have at least one capital letter")
        return password


    # def __repr__(self):
    #     return f'User {self.username}, ID {self.id}'
    
    # @hybrid_property
    # def password_hash(self):
    #     return self.password

    # @password_hash.setter
    # def password_hash(self, password):
    #     password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    #     self.password = password_hash.decode("utf-8")

    # def authenticate(self, password):
    #     return bcrypt.check_password_hash(self.password_hash, password.encode("utf-8"))

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
    author_notes = db.relationship("Note", backref="author", lazy=True)


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
            "date": self.date.isoformat(),
            "entry_time": self.entry_time.isoformat(),
            "exit_time": self.exit_time.isoformat(),
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


# WatchlistItem Model
class WatchlistItem(db.Model):
    __tablename__ = 'watchlist_items'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
        }

    # Relationships
    watchlist_id = db.Column(db.Integer, db.ForeignKey(
        "watchlists.id"), nullable=False)

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
            "date": self.date.isoformat(),
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




# Note Model
class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
        }

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# restricts the choices od the user using enum
class Sector(Enum):
    HEALTHCARE = 'healthcare'
    MATERIALS = 'materials'
    REAL_ESTATE = 'real estate'
    CONSUMER_STAPLES = 'consumer staples'
    CONSUMER_DISCRETIONARY = 'consumer discretionary'
    UTILITIES = 'utilities'
    ENERGY = 'energy'
    INDUSTRIALS = 'industrials'
    CONSUMER_SERVICES = 'consumer services'
    FINANCIALS = 'financials'
    TECHNOLOGY = 'technology'

class RiskLevel(Enum):
    LOW = 'low'
    MID = 'mid'
    HIGH = 'high'

class TradeDuration(Enum):
    SHORT = 'short'
    LONG = 'long'

class TradeOutcome(Enum):
    WIN = 'win'
    LOSS = 'loss'


# Tag Model
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    sector = db.Column(db.String(50))
    risk_level = db.Column(db.String(20))
    trade_duration = db.Column(db.String(20))
    trade_outcome = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sector": self.sector,
            "risk_level": self.risk_level,
            "trade_duration": self.trade_duration,
            "trade_outcome": self.trade_outcome
        }

    # Relationships
    trades = db.relationship("TradeTag", backref="tag", lazy=True)


# TradeTag Model (Join Table)
class TradeTag(db.Model):
    __tablename__ = 'trade_tags'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
        }

    # Relationships
    trade_id = db.Column(db.Integer, db.ForeignKey(
        "trades.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)
