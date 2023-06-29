import React, { useState } from "react";
import { Switch, Route, Redirect } from "react-router-dom";
import Home from "./components/Home";
import Register from "./components/Register";
import Login from "./components/Login";
import User from "./components/User";
import Trade from "./components/Trade";
import Watchlist from "./components/Watchlist";
import OverallPerformance from "./components/OverallPerformance";
import Site from "./components/Site";
import Note from "./components/Note";
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <div>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/register" component={Register} />
        <Route path="/login">
          {isLoggedIn ? (
            <Redirect to="/" />
          ) : (
            <Login onLogin={handleLogin} />
          )}
        </Route>
        <Route path="/users/:userId">
          {isLoggedIn ? (
            <User onLogout={handleLogout} />
          ) : (
            <Redirect to="/" />
          )}
        </Route>
        <Route path="/trade/users/:userId" component={Trade} />
        <Route path="/watchlist" component={Watchlist} />
        <Route path="/overallperformance/users/:userId" component={OverallPerformance} />
        <Route path="/site" component={Site} />
        <Route path="/note" component={Note} />
      </Switch>
    </div>
  );
}

export default App;
