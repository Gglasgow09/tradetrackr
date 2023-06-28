import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

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
                        <Link to={`/performance/users/${userId}`}>Overall Performance</Link>
                    </li>
                    <li>
                        <button onClick={handleLogout}>Logout</button>
                    </li>
                </ul>
            </nav>
            {user ? (
                <div>
                    <h2>Welcome {user.username}</h2>
                    <p>Username: {user.username}</p>
                    <p>Email: {user.email}</p>
                    <p>Hello, {user.username}!</p>
                </div>
            ) : (
                <div>User not found.</div>
            )}
        </div>
    );
};

export default User;
