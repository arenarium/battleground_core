import React, { Component } from 'react';
import { ListGroup, ListGroupItem} from 'react-bootstrap';
import {LinkContainer} from 'react-router-bootstrap'


class GameIndex extends Component {

  render() {
    let listItemArray=[]
    for (let key in this.props.gameArray) {
      if (this.props.gameArray.hasOwnProperty(key)) {
        let gameID = this.props.gameArray[key]["_id"]
        let gameType = this.props.gameArray[key]["game_type"]
        listItemArray.push(
          <LinkContainer key={key} to={"/games/"+String(gameID)+"/1/"}
            onClick={()=>{this.props.onGameSelect(key)}}>
            <ListGroupItem >
              {gameType+": "+gameID.substring(0,8)}
            </ListGroupItem>
          </LinkContainer>
      )
    }
  }
  return (
    <div className="GameIndex">
      <h4>Games:</h4>
      <ListGroup>
        {listItemArray}
      </ListGroup>
    </div>

  );
}
}

export default GameIndex;
