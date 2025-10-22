import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import './watchlist.css';
import './TradingViewWidget.js';


const Watchlist = () => {
    const { userId } = useParams(); // Access the userId from the URL parameter
    const [watchlists, setWatchlists] = useState([]);
    const [watchlistName, setWatchlistName] = useState('');
    const [watchlistItems, setWatchlistItems] = useState('');
    const [editingWatchlistId, setEditingWatchlistId] = useState(null);

    const handleFormSubmit = (event) => {
        event.preventDefault();

        if (editingWatchlistId) {
            // Update existing watchlist
            const updatedWatchlists = watchlists.map((watchlist) => {
                if (watchlist.id === editingWatchlistId) {
                    return {
                        ...watchlist,
                        name: watchlistName,
                        items: watchlistItems.split('\n').filter((item) => item.trim() !== ''),
                    };
                }
                return watchlist;
            });

            setWatchlists(updatedWatchlists);
            setEditingWatchlistId(null);
        } else {
            // Create new watchlist
            const newWatchlist = {
                id: Date.now(),
                name: watchlistName,
                items: watchlistItems.split('\n').filter((item) => item.trim() !== ''),
            };

            setWatchlists([...watchlists, newWatchlist]);
        }

        // Reset form fields
        setWatchlistName('');
        setWatchlistItems('');
    };

    const handleEditClick = (watchlistId) => {
        const watchlistToEdit = watchlists.find((watchlist) => watchlist.id === watchlistId);
        setWatchlistName(watchlistToEdit.name);
        setWatchlistItems(watchlistToEdit.items.join('\n'));
        setEditingWatchlistId(watchlistId);
    };

    const handleDeleteClick = (watchlistId) => {
        const updatedWatchlists = watchlists.filter((watchlist) => watchlist.id !== watchlistId);
        setWatchlists(updatedWatchlists);
        setEditingWatchlistId(null);
    };

    return (
        <div>
            <nav className="navbar">
                <ul className="nav-list">
                    <li className="nav-item">
                        <Link to="/">Home</Link>
                    </li>
                    <li className="nav-item">
                        <Link to="/watchlist">WatchList</Link>
                    </li>
                    <li className="nav-item">
                        <Link to={`/trade/users/${userId}`}>Trade Journal</Link>
                    </li>
                    <li className="nav-item">
                        <Link to="/site">Resources</Link>
                    </li>
                    <li className="nav-item">
                        <Link to="/performance">Overall Performance</Link>
                    </li>
                </ul>
            </nav>
            <h1 className="heading">Watchlist</h1>
            <form onSubmit={handleFormSubmit}>
                <label htmlFor="watchlistName">Watchlist Name:</label>
                <input
                    type="text"
                    id="watchlistName"
                    value={watchlistName}
                    onChange={(e) => setWatchlistName(e.target.value)}
                />
                <br />
                <label htmlFor="watchlistItems">Watchlist Items:</label>
                <textarea
                    id="watchlistItems"
                    value={watchlistItems}
                    onChange={(e) => setWatchlistItems(e.target.value)}
                />
                <br />
                <button type="submit">{editingWatchlistId ? 'Update Watchlist' : 'Create Watchlist'}</button>
            </form>
            <h2 className="subheading">Current Watchlists:</h2>
            {watchlists.map((watchlist) => (
                <div key={watchlist.id}>
                    <h3 className='h3'>{watchlist.name}</h3>
                    <ul>
                        {watchlist.items.map((item) => (
                            <li className='li' key={item}>{item}</li>
                        ))}
                    </ul>
                    <div>
                        <button onClick={() => handleEditClick(watchlist.id)}>Edit</button>
                        <button onClick={() => handleDeleteClick(watchlist.id)}>Delete</button>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Watchlist;
