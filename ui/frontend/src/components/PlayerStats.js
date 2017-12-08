import React, { Component } from 'react';
import { ListGroup, ListGroupItem} from 'react-bootstrap';




class PlayerStats extends Component {
  constructor(props){
    super(props)
  }

  componentDidMount(){

  }

  render() {
    let playerArray = this.props.playerArray
    let listItemArray=[]

    for (let key in playerArray) {
      if (playerArray.hasOwnProperty(key)) {

        let playerID = playerArray[key]["_id"]
        let playerName = playerArray[key]["name"]
        let gameType = playerArray[key]["game_type"]
        let wins = playerArray[key]["wins"]

        listItemArray.push(
          <ListGroupItem key={key}>
            {playerName}: {wins}
          </ListGroupItem>
        )
      }
    }

    return (
      <div className="PlayerStats">
        <h4>Players:</h4>
        <ListGroup>
          {listItemArray}
        </ListGroup>
      </div>
    )
  }
}

export default PlayerStats;
