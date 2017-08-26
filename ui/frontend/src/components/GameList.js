import React, {Component} from 'react'
import { Grid, Row,Col,Panel, Button, PageHeader } from 'react-bootstrap';
import GameIndex from './GameIndex'
import StateArrayViewer from './StateArrayViewer'
import 'whatwg-fetch'
var request = require('request');


class GameList extends Component {
  constructor(props){
    super(props)
    this.state = {
      gameStates:null,
      gameArray:null,
      stateIndex: props.match.params.stateIndex !=null?props.match.params.stateIndex:0,
      // gameID:props.match.params.gameID
    }
    this.getGamesList = this.getGamesList.bind(this)
    this.updateMoves = this.updateMoves.bind(this)
    this.onStateSelect = this.onStateSelect.bind(this)
    this.getGamesList()
    if (props.match.params.gameID !=null){
      this.updateMoves(props.match.params.gameID)
    }
  }


  getGamesList() {
    fetch('/api/games/')
    .then((response) =>{
      return response.json()})
      .then((value)=>{
        this.setState({gameArray:value})
      })
      .catch(function(ex) {
        console.log('parsing failed', ex)
      })
    }


  updateMoves(gameID){
    fetch('/api/states/'+gameID)
    .then((response) =>{
      return response.json()})
      .then((value)=>{
        this.setState({gameStates:value})
      })
      .catch(function(ex) {
        console.log('parsing failed', ex)
      })
    }

  onStateSelect(eventKey){
    this.props.history.push("../"+String(eventKey)+"/")
    this.setState({stateIndex:eventKey})
  }

  onGameSelect(eventKey){
    this.updateMoves(eventKey)
  }

  render() {
    return(
      <div className="container">
        <Grid>
          <Row>
            <PageHeader>Watch Games
              <br/><small>Watch and Learn from ongoing games or replays</small></PageHeader>
          </Row>
          <Row>
            <Col md={3}>
              <Panel>
                <GameIndex onGameSelect={this.onGameSelect} gameArray={this.state.gameArray}/>
              </Panel>
            </Col>
            <Col md={8}>
              <Panel>
                <StateArrayViewer
                  states={this.state.gameStates}
                  stateIndex={this.state.stateIndex}
                  onStateSelect={this.onStateSelect}/>
              </Panel>
            </Col>
          </Row>
        </Grid>
      </div>
        )
      }
  }

export default GameList
