import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";


function Trade() {
    const [trades, setTrades] = useState([]);
    const { userId } = useParams();


    useEffect(() => {
        const fetchTrades = () => {
            fetch(`/trade/users/${userId}`)
                .then((response) => response.json())
                .then((data) => setTrades(data))
                .catch((error) => console.error('Error fetching trades:', error));

        };
        fetchTrades(); // Call fetchTrades directly

    }, [userId]);

    return (
        <div>
            <h1>Trade Journal</h1>
            {trades && trades.length === 0 ? (
                <p>No trades found.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Entry Time</th>
                            <th>Exit Time</th>
                            <th>Symbol</th>
                            <th>Long/Short</th>
                            <th>Quantity</th>
                            <th>Entry Price</th>
                            <th>Exit Price</th>
                            <th>Profit/Loss</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {trades && trades.map((trade) => (
                            <tr key={trade.id}>
                                <td>{trade.date}</td>
                                <td>{trade.entry_time}</td>
                                <td>{trade.exit_time}</td>
                                <td>{trade.symbol}</td>
                                <td>{trade.long_short}</td>
                                <td>{trade.quantity}</td>
                                <td>{trade.entry_price}</td>
                                <td>{trade.exit_price}</td>
                                <td>{trade.pnl}</td>
                                <td>{trade.notes}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default Trade;
