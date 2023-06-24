import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';

function Trade() {
    const [trades, setTrades] = useState([]);
    const userId = 1; // Replace with the logged-in user's ID

    useEffect(() => {
        fetchTrades();
    }, []);

    const fetchTrades = () => {
        fetch('/api/trade')
            .then(response => response.json())
            .then(data => setTrades(data.trades))
            .catch(error => console.error('Error fetching trades:', error));
    };

    return (
        <div>
            <h1>Trade Journal</h1>
            {trades.length === 0 ? (
                <p>No trades found.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Symbol</th>
                            <th>Quantity</th>
                            <th>Entry Price</th>
                            <th>Exit Price</th>
                            <th>Profit/Loss</th>
                        </tr>
                    </thead>
                    <tbody>
                        {trades.map((trade) => (
                            <tr key={trade.id}>
                                <td>{trade.date}</td>
                                <td>{trade.symbol}</td>
                                <td>{trade.quantity}</td>
                                <td>{trade.entry_price}</td>
                                <td>{trade.exit_price}</td>
                                <td>{trade.pnl}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
// check to see if i can render all of the trades by user id instead if individual trade id 
// find a way to add new trades to  the user using full CRUD 
// each user should be able to pull up all trades and that should also allow them to add new trades
// add a nav bar fer the others
//figure out they python yahoofinance library for watchlist 

export default Trade;
