import React, { Component } from 'react';
import {  Pagination} from 'react-bootstrap';

// const MyPagination = withRouter(({numItems, newActivePage, history})=>(
// // {(eventKey)=>{history.push("../"+String(eventKey)+"/")}}
//   )
// )

class StateArrayViewer extends Component {


  render() {
    var content
    if (this.props.states != null){
      let currentState = this.props.states[this.props.stateIndex-1]
      let currentGameState = currentState["game_state"]
      let currentLastMove = currentState["last_move"]
      var gameStateString = JSON.stringify(currentGameState, null, 4)
      var lastMoveString = JSON.stringify(currentLastMove, null, 4)
      content = (
        <div>
          <Pagination
            prev
            next
            first
            last
            ellipsis
            boundaryLinks
            items={this.props.states.length}
            maxButtons={5}
            activePage={this.props.stateIndex}
            onSelect= {this.props.onStateSelect} />
          <p>Last Move:</p>
          <pre>{lastMoveString}</pre>
          <p>Game State</p>
          <pre>{gameStateString}</pre>
        </div>)
        }else {
          content = (<p>Select a game to view.</p>)
        }
        return (
          <div className="StateArrayViewer">
            {content}
          </div>
        );
      }
    }

    export default StateArrayViewer;
