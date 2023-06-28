import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

const User = () => {
    // Retrieve the user ID from the route parameter
    const { userId } = useParams();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        console.log(userId);
        fetch(`/users/${userId}`) // Use the retrieved user ID in the API request
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
        // Implement the logout functionality here
        // You can clear any user-related data or perform any necessary cleanup

        // For example, you can redirect the user to the login page after logout
        // window.location.href = "/login";
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
                    <p>Hello, {user.username}!</p> {/* Print "Hello, user" with the user's username */}
                </div>
            ) : (
                <div>User not found.</div>
            )}
        </div>
    );
};

export default User;
