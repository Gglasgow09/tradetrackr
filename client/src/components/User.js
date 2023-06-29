import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import './user.css';

const User = ({ onLogout }) => {
    const { userId } = useParams();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`/users/${userId}`)
            .then((response) => response.json())
            .then((data) => {
                setUser(data);
                setLoading(false);
            })
            .catch((error) => {
                console.log(error);
                setLoading(false);
            });
    }, [userId]);

    const handleLogout = () => {
        fetch("/logout", {
            method: "DELETE",
        }).then(() => onLogout());
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="container">
            <nav className="navbar">
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
                        <Link to={`/performance/users/${userId}`}>Overall Performance</Link>
                    </li>
                    <li>
                        <button onClick={handleLogout}>Logout</button>
                    </li>
                </ul>
            </nav>
            {user ? (
                <div className="content">
                    <h1>It's a beautiful day to trade {user.username}</h1>
                    <h2>Trading Rules to Keep in Mind</h2>
                    <ul className='ul'>
                        <li>Stick to Your Discipline</li>
                        <li>Lose the Crowd</li>
                        <li>Engage Your Trading Plan</li>
                        <li>Don't Cut Corners</li>
                        <li>Avoid the Obvious</li>
                        <li>Don't Break Your Rules</li>
                        <li>Avoid Market Gurus</li>
                        <li>Use Your Intuition</li>
                        <li>Don't Fall in Love</li>
                        <li>Organize Your Personal life</li>
                        <li>Don't Try to Get Even</li>
                        <li>Watch for Warnings</li>
                        <li>Tools Don't Think</li>
                        <li>Use Your Head</li>
                        <li>Forget the Holy Grail</li>
                        <li>Ditch the Paycheck Mentality</li>
                        <li>Don't Count Your Chickens</li>
                        <li>Embrace Simplicity</li>
                        <li>Make Peace With Losses</li>
                        <li>Beware of Reinforcement</li>
                    </ul>
                </div>
            ) : (
                <div>User not found.</div>
            )}
        </div>
    );
};

export default User;
