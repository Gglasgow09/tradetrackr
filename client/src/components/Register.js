import React, { useState } from "react";
import axios from "axios";
import './register.css'; // Import the CSS file

function Register() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();

        // Create a new user object
        const newUser = {
            username: username,
            email: email,
            password: password,
        };

        // Send a POST request to the registration endpoint
        axios
            .post("/register", newUser)
            .then((response) => {
                // Registration successful
                setMessage(response.data.message);
                setUsername("");
                setEmail("");
                setPassword("");

            })
            .catch((error) => {
                // Registration failed
                setMessage(error.response.data.message);
            });
    };

    return (
        <div className="register-container">
            <form className="register-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button className="btn" type="submit">Register</button>
            </form>
            {message && <p>{message}</p>}
        </div>

    );
}

export default Register;
