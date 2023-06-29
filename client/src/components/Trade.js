import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import './trade.css';

function Trade() {
    const [trades, setTrades] = useState([]);
    // tracks trade for update
    const [selectedTrade, setSelectedTrade] = useState(null);
    // allows for access to 'userId' from url
    const { userId } = useParams();
    const [newTrade, setNewTrade] = useState({
        id: "", // Add trade ID property
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
    const [sortOrder, setSortOrder] = useState("asc"); // Default sorting order is ascending

    // fetches trades from server when either the userId or trade state changes
    useEffect(() => {
        const fetchTrades = () => {
            fetch(`/trade/users/${userId}`)
                .then((response) => response.json())
                .then((data) => {
                    const sortedTrades = data.sort((a, b) => {
                        if (sortOrder === "asc") {
                            return new Date(a.date) - new Date(b.date);
                        } else {
                            return new Date(b.date) - new Date(a.date);
                        }
                    });
                    setTrades(sortedTrades);
                })
                .catch((error) => console.error("Error fetching trades:", error));
        };
        fetchTrades();
    }, [userId, trades, sortOrder]);

    const handleChangeSortOrder = (e) => {
        setSortOrder(e.target.value);
    };

    // event handler for change in form
    const handleChange = (e) => {
        const { name, value } = e.target;
        setNewTrade((prevTrade) => ({
            ...prevTrade,
            [name]: value,
        }));
    };
    //event handler for form submission
    const handleSubmit = (e) => {
        e.preventDefault();
        // Check if a trade ID is present to determine if it's an update or addition
        if (newTrade.id) {
            // Handle trade update
            const tradeToUpdate = {
                ...newTrade,
                user_id: userId,
            };

            fetch(`/trade/${newTrade.id}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(tradeToUpdate),
            })
                .then((response) => response.json())
                .then((updatedTrade) => {
                    // Update the trade in the trades list
                    // its currently not updating the front end unless a refresh happens 
                    setTrades((prevTrades) =>
                        prevTrades.map((trade) =>
                            trade.id === updatedTrade.id ? updatedTrade : trade
                        )
                    );

                    // Reset the form fields
                    setNewTrade({
                        id: "",
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

                    // Clear the selected trade
                    setSelectedTrade(null);
                })
                .catch((error) => console.error("Error updating trade:", error));
        } else {

            // Calculate profit/loss and create a new trade object
            const entryPrice = parseFloat(newTrade.entry_price);
            const exitPrice = parseFloat(newTrade.exit_price);
            const quantity = parseFloat(newTrade.quantity);
            let pnl = 0;

            if (newTrade.long_short === "Long") {
                pnl = (exitPrice - entryPrice) * quantity;
            } else if (newTrade.long_short === "Short") {
                pnl = (entryPrice - exitPrice) * quantity;
            }

            const tradeWithPnl = {
                ...newTrade,
                pnl: pnl.toFixed(2),
                user_id: userId,
            };

            fetch(`/trade/users/${userId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(tradeWithPnl),
            })
                .then((response) => response.json())
                .then((data) => {
                    setTrades((prevTrades) => [...prevTrades, data]);
                    setNewTrade({
                        id: "",
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
                })
                .catch((error) => console.error("Error adding trade:", error));
        }
    };
    // called when update button is clicked 
    const handleUpdate = (tradeId) => {
        const tradeToUpdate = trades.find((trade) => trade.id === tradeId);
        setSelectedTrade(tradeToUpdate);
        setNewTrade(tradeToUpdate);
    };
    // takes care of deleting a trade
    const handleDelete = (tradeId) => {
        fetch(`/trade/${tradeId}`, {
            method: "DELETE",
        })
            .then(() => {
                setTrades((prevTrades) =>
                    prevTrades.filter((trade) => trade.id !== tradeId)
                );
            })
            .catch((error) => console.error("Error deleting trade:", error));
    };

    return (
        // navbar for the different links 
        <div>
            <nav>
                <ul>
                    {/* <li>
                        <Link to="/watchlist">Watchlist</Link>
                    </li> */}
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
            {/* trade journal entries */}
            <h1>Trade Journal</h1>
            <div>
                Sort:
                <select value={sortOrder} onChange={handleChangeSortOrder}>
                    <option value="asc">Oldest to Current</option>
                    <option value="desc">Current to Oldest</option>
                </select>
            </div>
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
                            <th>Actions</th>
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
                                    <td>
                                        <button onClick={() => handleUpdate(trade.id)}>
                                            Update
                                        </button>
                                        <button onClick={() => handleDelete(trade.id)}>
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            ))}
                    </tbody>
                </table>
            )}
            {/* if you hit update the form changes to update if not it will be add new */}
            <h2>{selectedTrade ? "Update Trade" : "Add New Trade"}</h2>
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
                    <option value="">Long/Short</option>
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
                <button type="submit">{selectedTrade ? "Update" : "Add Trade"}</button>
            </form>
        </div>
    );
}

export default Trade;
