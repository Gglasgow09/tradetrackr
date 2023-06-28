import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";

function Trade() {
    const [trades, setTrades] = useState([]);
    const { userId } = useParams();

    const [newTrade, setNewTrade] = useState({
        date: "",
        entry_time: "",
        exit_time: "",
        symbol: "",
        long_short: "",
        quantity: 0,
        entry_price: "",
        exit_price: "",
        pnl: 0,
        notes: "",
    });

    useEffect(() => {
        const fetchTrades = () => {
            fetch(`/trade/users/${userId}`)
                .then((response) => response.json())
                .then((data) => setTrades(data))
                .catch((error) => console.error("Error fetching trades:", error));
        };
        fetchTrades();
    }, [userId]);


    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewTrade((prevTrade) => ({
            ...prevTrade,
            [name]: value,
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // Calculate profit/loss
        const entryPrice = parseFloat(newTrade.entry_price);
        const exitPrice = parseFloat(newTrade.exit_price);
        const quantity = parseFloat(newTrade.quantity);
        let pnl = 0;

        if (newTrade.long_short === "Long") {
            pnl = (exitPrice - entryPrice) * quantity;
        } else if (newTrade.long_short === "Short") {
            pnl = (entryPrice - exitPrice) * quantity;
        }

        // Create a new trade object with the calculated pnl
        const tradeWithPnl = {
            ...newTrade,
            pnl: pnl.toFixed(2), // Round pnl to 2 decimal places
            user_id: userId,
        };

        // Send a POST request to save the new trade
        fetch(`/trade/users/${userId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(tradeWithPnl),
        })
            .then((response) => response.json())
            .then((data) => {
                // Update the trades list with the new trade
                setTrades((prevTrades) => [...prevTrades, data]);
                // Clear the form fields
                setNewTrade({
                    date: "",
                    entry_time: "",
                    exit_time: "",
                    symbol: "",
                    long_short: "",
                    quantity: "",
                    entry_price: "",
                    exit_price: "",
                    pnl: 0,
                    notes: "",
                });
            })
            .catch((error) => console.error("Error adding trade:", error));
    };

    return (
        <div>
            <nav>
                <ul>
                    <li>
                        <Link to="/watchlist">Watchlist</Link>
                    </li>
                    <li>
                        <Link to={`/trade/users/${userId}`}>Trade Journal</Link>
                    </li>
                    <li>
                        <Link to="/site">Site</Link>
                    </li>
                    <li>
                        <Link to="/performance">Overall Performance</Link>
                    </li>
                </ul>
            </nav>
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
                        {trades &&
                            trades.map((trade) => (
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
            <h2>Add New Trade</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="date"
                    value={newTrade.date}
                    onChange={handleChange}
                    placeholder="Date"
                />
                <input
                    type="text"
                    name="entry_time"
                    value={newTrade.entry_time}
                    onChange={handleChange}
                    placeholder="Entry Time"
                />
                <input
                    type="text"
                    name="exit_time"
                    value={newTrade.exit_time}
                    onChange={handleChange}
                    placeholder="Exit Time"
                />
                <input
                    type="text"
                    name="symbol"
                    value={newTrade.symbol}
                    onChange={handleChange}
                    placeholder="Symbol"
                />
                <select
                    name="long_short"
                    value={newTrade.long_short}
                    onChange={handleChange}
                >
                    <option value="">Long/Short --</option>
                    <option value="Long">Long</option>
                    <option value="Short">Short</option>
                </select>
                <input
                    type="number"
                    name="quantity"
                    value={newTrade.quantity}
                    onChange={handleChange}
                    placeholder="Quantity"
                />
                <input
                    type="number"
                    name="entry_price"
                    value={newTrade.entry_price}
                    onChange={handleChange}
                    placeholder="Entry Price"
                />
                <input
                    type="number"
                    name="exit_price"
                    value={newTrade.exit_price}
                    onChange={handleChange}
                    placeholder="Exit Price"
                />
                <input
                    type="number"
                    name="pnl"
                    value={newTrade.pnl}
                    onChange={handleChange}
                    placeholder="Profit/Loss"
                />
                <input
                    type="text"
                    name="notes"
                    value={newTrade.notes}
                    onChange={handleChange}
                    placeholder="Notes"
                />
                <button type="submit">Add Trade</button>
            </form>
        </div>
    );
}

export default Trade;
