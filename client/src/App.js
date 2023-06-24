import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
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
  return (
    <div>
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/register" component={Register} />
        <Route path="/login" component={Login} />
        <Route path="/users/:userId" component={User} />
        <Route path="/trade" component={Trade} />
        <Route path="/watchlist" component={Watchlist} />
        <Route path="/overallperformance" component={OverallPerformance} />
        <Route path="/site" component={Site} />
        <Route path="/note" component={Note} />
      </Switch>
    </div>
  );
}


export default App;
