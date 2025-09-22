import React, { useState, useEffect } from 'react';
import { useParams, Link } from "react-router-dom";
import './site.css';

function SiteForm() {
    const { userId } = useParams(); // Access the userId from the URL parameter
    const [url, setUrl] = useState('');
    const [favoriteWebsites, setFavoriteWebsites] = useState([]);

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log('Submitted URL:', url);
        setFavoriteWebsites([...favoriteWebsites, url]);
        setUrl(''); // Clear the input field after submission
    };

    const handleChange = (event) => {
        setUrl(event.target.value);
    };

    useEffect(() => {
        const script = document.createElement('script');
        script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
        script.async = true;
        script.innerHTML = JSON.stringify({
            allow_symbol_change: true,
            calendar: false,
            details: false,
            hide_side_toolbar: true,
            hide_top_toolbar: false,
            hide_legend: false,
            hide_volume: false,
            hotlist: false,
            interval: "D",
            locale: "en",
            save_image: true,
            style: "1",
            symbol: "NASDAQ:AAPL",
            theme: "dark",
            timezone: "Etc/UTC",
            backgroundColor: "#0F0F0F",
            gridColor: "rgba(242, 242, 242, 0.06)",
            watchlist: [],
            withdateranges: false,
            compareSymbols: [],
            studies: [],
            autosize: true,
        });
        document.querySelector('.tradingview-widget-container__widget').appendChild(script);
    }, []);

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
            <div>
                <div className="tradingview-widget-container" style={{ height: "100%", width: "100%" }}>
                    <div className="tradingview-widget-container__widget" style={{ height: "calc(100% - 32px)", width: "100%" }}></div>
                    <div className="tradingview-widget-copyright">
                        <a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener nofollow" target="_blank">
                            <span className="blue-text">AAPL stock chart</span>
                        </a>
                        <span className="trademark"> by TradingView</span>
                    </div>
                </div>
            </div>
            <form className="Site" onSubmit={handleSubmit}>
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