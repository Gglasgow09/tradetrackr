import React from "react";
import { Link } from "react-router-dom";
import './home.css';

function Home() {
    return (
        <div>
            <img
                src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKa63CUpi_I81xLMP5Cfq3nSqbn59E3AB5EA&usqp=CAU"
                alt="Person looking at a stock chart"
                className="left-image"
            />

            <div className="content">
                <h1>TradeTrackr</h1>
                <p>Welcome to our application! Our app is designed to help you manage and track your trading activities effectively.</p>

                <p>
                    Whether you're an experienced trader or just starting out, our platform offers a range of features to assist you in organizing your trades, monitoring your performance, and staying on top of the market.
                    With our intuitive interface, you can easily record your trades, including essential details such as date, time, symbol, entry/exit prices, quantity, and more. Keep track of your profits and losses with real-time calculations, allowing you to analyze your trading strategies and make informed decisions.
                    Create personalized watchlists to monitor your favorite stocks and stay updated on market trends. Customize your watchlists by adding or removing ticker symbols, and easily access relevant information to help you make well-informed trading choices.
                    Our comprehensive performance tracking enables you to evaluate your overall trading success. Monitor your portfolio value, calculate your return on investment (ROI), analyze your win rate, and identify potential areas of improvement. Stay informed about your trade durations and maximize your trading efficiency.
                    Additionally, our platform provides a convenient note-taking feature, allowing you to jot down important insights, trade rationales, or any other information you want to remember. Seamlessly associate notes with specific trades or keep general notes for future reference.
                </p>
                <p>
                    Whether you're a day trader, swing trader, or long-term investor, our app empowers you to stay organized, analyze your performance, and make data-driven trading decisions. We're excited to have you on board and look forward to helping you on your trading journey.
                    Start exploring the app and take control of your trading experience today!
                    Sign up or log in to get started.
                </p>

                <Link to="/register">
                    <button className="btn">Sign Up</button>
                </Link>

                <Link to="/login">
                    <button className="btn">Login</button>
                </Link>
            </div>
        </div>
    );
}

export default Home;
