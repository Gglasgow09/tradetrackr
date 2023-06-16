#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Trade, OverallPerformance

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
                entry_time = fake.time()
                exit_time = fake.time()
                symbol = fake.random_element(
                    elements=('AAPL', 'GOOGL', 'TSLA', 'MSFT'))
                long_short = fake.random_element(elements=('Long', 'Short'))
                quantity = fake.random_int(min=1, max=100)
                entry_price = fake.pyfloat(min_value=50, max_value=200)
                exit_price = fake.pyfloat(min_value=50, max_value=200)
                pnl = fake.random_number(decimals=2, min=-200, max=200)
                notes = fake.sentence()

                # Create a Trade instance with the generated data and assign it to the user
                trade = Trade(date=date, entry_time=entry_time, exit_time=exit_time, symbol=symbol,
                              long_short=long_short, quantity=quantity, entry_price=entry_price,
                              exit_price=exit_price, pnl=pnl, notes=notes, user=user)

                # Add the trade to the database session
                db.session.add(trade)

            # Create a Performance instance for each user
            portfolio_value = fake.random_int(decimals=2, min=10000, max=1000000)
            pnl = fake.random_number(decimals=2, min=-2000, max=2000)
            roi = fake.random_number(decimals=2, min=-10, max=10)
            win_rate = fake.random_number(decimals=2, min=0, max=100)
            max_drawdown = fake.random_number(decimals=2, min=0, max=100)
            trade_duration = fake.random_int(decimals=2, min=1, max=100)

            # Create a Performance instance with the generated data and assign it to the user
            overallperformance = OverallPerformance(date=fake.date(), portfolio_value=portfolio_value,
                                                    pnl=pnl, roi=roi, win_rate=win_rate,
                                                    max_drawdown=max_drawdown, trade_duration=trade_duration,
                                                    user=user)

            # Add the performance to the database session
            db.session.add(overallperformance)

        # Commit the changes to the database
        db.session.commit()

        print("Seed completed!")
