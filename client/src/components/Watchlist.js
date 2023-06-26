import React, { useState, useEffect } from 'react';

const Watchlist = () => {
    const [watchlists, setWatchlists] = useState([]);
    const [watchlistName, setWatchlistName] = useState('');
    const [watchlistItems, setWatchlistItems] = useState('');

    useEffect(() => {
        fetchWatchlists();
    }, []);

    const fetchWatchlists = async () => {
        try {
            const response = await fetch('/watchlist');
            const data = await response.json();
            setWatchlists(data);
        } catch (error) {
            console.error('Error:', error.message);
        }
    };

    const handleFormSubmit = async (event) => {
        event.preventDefault();

        const payload = {
            name: watchlistName,
            items: watchlistItems.split('\n').filter((item) => item.trim() !== ''),
        };

        try {
            const response = await fetch('/watchlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error('Failed to create watchlist');
            }

            const data = await response.json();
            console.log(data);

            // Reset form fields
            setWatchlistName('');
            setWatchlistItems('');

            // Fetch updated watchlists
            fetchWatchlists();
        } catch (error) {
            console.error('Error:', error.message);
        }
    };

    const handleDeleteClick = async (watchlistId) => {
        try {
            const response = await fetch(`/watchlist/${watchlistId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete watchlist');
            }

            const data = await response.json();
            console.log(data);

            // Fetch updated watchlists
            fetchWatchlists();
        } catch (error) {
            console.error('Error:', error.message);
        }
    };

    return (
        <div>
            <h1>Watchlist</h1>
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
                <button type="submit">Create Watchlist</button>
            </form>
            <h2>Current Watchlists:</h2>
            {watchlists.map((watchlist) => (
                <div key={watchlist.id}>
                    <h3>{watchlist.name}</h3>
                    <ul>
                        {watchlist.items.map((item) => (
                            <li key={item}>{item}</li>
                        ))}
                    </ul>
                    <button onClick={() => handleDeleteClick(watchlist.id)}>Delete</button>
                </div>
            ))}
        </div>
    );
};

export default Watchlist;
