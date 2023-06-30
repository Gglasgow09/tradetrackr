import React, { useState } from 'react';
import { useParams, Link } from "react-router-dom";
import './site.css';

function SiteForm() {
    const { userId } = useParams(); // Access the userId from the URL parameter
    const [url, setUrl] = useState('');
    const [favoriteWebsites, setFavoriteWebsites] = useState([]);

    const handleSubmit = (event) => {
        event.preventDefault();
        // Add your logic here to handle the form submission
        // For example, you can make an API call to store the website in the backend
        console.log('Submitted URL:', url);
        setFavoriteWebsites([...favoriteWebsites, url]);
        setUrl(''); // Clear the input field after submission
    };

    const handleChange = (event) => {
        setUrl(event.target.value);
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
            <form className='Site' onSubmit={handleSubmit}>
                <label>
                    Website URL:
                    <input type="text" value={url} onChange={handleChange} />
                </label>
                <button type="submit">Add Website</button>
            </form>
            <div className="favorite-websites">
                <h2>Favorite Websites:</h2>
                {favoriteWebsites.length > 0 ? (
                    <ul>
                        {favoriteWebsites.map((website, index) => (
                            <li key={index}>
                                <a href={website} target="_blank" rel="noopener noreferrer">
                                    {website}
                                </a>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No favorite websites added yet.</p>
                )}
            </div>
        </div>
    );
}

export default SiteForm;
