import React, { Component } from 'react';
import './styles/App.css';
import Header from "./Header"
import Welcome from "./Welcome"
import About from "./About"
import GameViewer from "./GameViewer"
import PlayerStats from "./PlayerStats"
import CodeUpload from "./CodeUpload"
import {
  BrowserRouter as Router,
  Route,
} from 'react-router-dom'


class App extends Component {
  constructor(props){
    super(props)
    this.playing=false
  }

componentDidMount(){
  this.props.populateGameList("default")
  if (!this.playing){
    this.playing=true
    this.props.doAutoPlay(1500)
  }
}

  render() {
    return (
      <div className="App">
        <Router>
          <div>
            <Header/>
            <Route exact path="/" component={Welcome}/>
            <Route  path="/about" component={About}/>
            <Route  exact path="/games" component={GameViewer}/>
            <Route  exact path="/stats" component={PlayerStats}/>
            <Route  exact path="/upload" component={CodeUpload}/>
            <Route  path="/games/:gameID/:stateIndex" component={GameViewer}>
              <GameViewer/>
              </Route>
          </div>
        </Router>
    </div>

  );
}
}

export default App;
