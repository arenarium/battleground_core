import React, { Component } from 'react';
import './App.css';
import Header from "./components/Header"
import Welcome from "./components/Welcome"
import About from "./components/About"
import GameList from "./components/GameList"
import {
  BrowserRouter as Router,
  Route,
} from 'react-router-dom'


class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <div>
            <Header/>
            <Route exact path="/" component={Welcome}/>
            <Route  path="/about" component={About}/>
            <Route  exact path="/games" component={GameList}/>
            <Route  path="/games/:gameID/:stateIndex" component={GameList}>
              {/* <GameList/> */}
            </Route>
          </div>
      </Router>
    </div>

  );
}
}

export default App;
