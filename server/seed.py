from random import randint, uniform, choice as rc
from datetime import datetime

# Remote library imports
from faker import Faker
from sqlalchemy import func

# Local imports
from app import app
from models import db, User, Trade, Watchlist, OverallPerformance, Site, WatchlistItem, Note, Tag, TradeTag, Sector, RiskLevel, TradeDuration, TradeOutcome

# Available choices for sectors, risk levels, trade durations, and trade outcomes
SECTORS = ['healthcare', 'materials', 'real estate', 'consumer staples', 'consumer discretionary',
           'utilities', 'energy', 'industrials', 'consumer services', 'financials', 'technology']
RISK_LEVELS = ['low', 'mid', 'high']
TRADE_DURATIONS = ['short', 'long']
TRADE_OUTCOMES = ['win', 'loss']

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        # Create 5 users
        for _ in range(5):
            username = fake.user_name()
            password = fake.password(length=10)
            email = fake.email()

            # Create a User instance with the generated data
            user = User(username=username, password=password, email=email)

            # Add the user to the database session
            db.session.add(user)

            # Create trades for each user
            for _ in range(5):  # Create 5 trades per user
                date = fake.date_between(start_date='-1y', end_date='today')
                entry_time = fake.time_object()
                exit_time = fake.time_object()

                symbol = fake.random_element(
                    elements=('AAPL', 'GOOGL', 'TSLA', 'MSFT'))
                long_short = fake.random_element(
                    elements=('Long', 'Short'))
                quantity = fake.random_int(min=1, max=100)
                entry_price = uniform(50, 200)
                exit_price = uniform(50, 200)
                pnl = uniform(-200, 200)
                notes = fake.sentence()

            # Create watchlists
            for _ in range(5):
                name = fake.word()
                user = User.query.order_by(func.random()).first()
            # Create a Watchlist instance with the generated data
                watchlist = Watchlist(name=name, user=user)
            # Add the watchlist to the database session
                db.session.add(watchlist)
            # Generate ticker symbols for the watchlist items
                ticker_symbols = [fake.random_element(elements=('AAPL', 'GOOGL', 'TSLA', 'MSFT')) for _ in range(5)]
            # Create watchlist items for the watchlist
            for ticker_symbol in ticker_symbols:
                watchlist_item = WatchlistItem(symbol=ticker_symbol, watchlist=watchlist)
                db.session.add(watchlist_item)

                # Create a Trade instance with the generated data and assign it to the user
                trade = Trade(date=date, entry_time=entry_time, exit_time=exit_time, symbol=symbol,
                              long_short=long_short, quantity=quantity, entry_price=entry_price,
                              exit_price=exit_price, pnl=pnl, notes=notes, user=user)

                # Add the trade to the database session
                db.session.add(trade)

                # Create a TradeTag instance with random tags for the trade
                tags = []
                for _ in range(randint(1, 3)):
                    tag = Tag(name=fake.word(),
                              sector=rc(SECTORS),
                              risk_level=rc(RISK_LEVELS),
                              trade_duration=rc(TRADE_DURATIONS),
                              trade_outcome=rc(TRADE_OUTCOMES))
                    db.session.add(tag)
                    tags.append(tag)

                # Create TradeTag instances to associate the trade with tags
                for tag in tags:
                    trade_tag = TradeTag(trade=trade, tag=tag)
                    db.session.add(trade_tag)
                
        # Retrieve all trades and users from the database
        trades = Trade.query.all()
        users = User.query.all()

        # Create notes for each trade and assign a random user
        for trade in trades:
            for _ in range(randint(1, 3)):
                content = fake.sentence()
                user = rc(users)  # Choose a random user
                note = Note(content=content, user=user, trade=trade)
                db.session.add(note)
                
            # Create a Performance instance for each user
            portfolio_value = randint(10000, 1000000)
            pnl = uniform(-2000, 2000)
            roi = uniform(-10, 10)
            win_rate = uniform(0, 100)
            max_drawdown = uniform(0, 100)
            trade_duration = randint(1, 100)

            # Convert the fake.date() value to Python date object
            date = datetime.strptime(fake.date(), "%Y-%m-%d").date()

            # Create a Performance instance with the generated data and assign it to the user
            overallperformance = OverallPerformance(date=date, portfolio_value=portfolio_value,
                                                    pnl=pnl, roi=roi, win_rate=win_rate,
                                                    max_drawdown=max_drawdown, trade_duration=trade_duration,
                                                    user=user)

            # Add the performance to the database session
            db.session.add(overallperformance)

        # Commit the changes to the database
        db.session.commit()

        print("Seed completed!")
