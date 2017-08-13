import React, { Component } from 'react';
import { ListGroup, ListGroupItem, Pagination} from 'react-bootstrap';
import {
  withRouter,
  Redirect
} from 'react-router-dom'

// const MyPagination = withRouter(({numItems, newActivePage, history})=>(
// // {(eventKey)=>{history.push("../"+String(eventKey)+"/")}}
//   )
// )

class StateArrayViewer extends Component {


  render() {
    var content
    if (this.props.states != null){
      var stateString = JSON.stringify(this.props.states[this.props.stateIndex-1], null, 4)
      content = (
        <div>
          {/* <MyPagination
            numItems={this.props.states.length}
          newActivePage={this.props.stateIndex}/> */}
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
          <pre>{stateString}</pre>
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
