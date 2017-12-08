import React from 'react';
// import {  Row, Col,Grid,Pager, Form,FormGroup,ControlLabel,FormControl,Checkbox} from 'react-bootstrap';
import StateNavContainer from '../containers/StateNavContainer'
// const MyPagination = withRouter(({numItems, newActivePage, history})=>(
// // {(eventKey)=>{history.push("../"+String(eventKey)+"/")}}
//   )
// )
//,stateIndex,length,autoPlay,onChangeAutoPlay ,onStateSelect
const GameStateViewer = ({gameState})=>{

    var content
    if (gameState != null){
      var currentGameState = gameState["game_state"]
      var lastMove = gameState["last_move"]
      var gameStateString = JSON.stringify(currentGameState, null, 4)
      var lastMoveString = JSON.stringify(lastMove, null, 4)
      content = (
        <div>
          <StateNavContainer/>
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
// class StateArrayViewer extends Component {
//   constructor(props){
//     super(props)
//     this.doAutoPlay = this.doAutoPlay.bind(this)
//     this.onChangeAutoPlay = this.onChangeAutoPlay.bind(this)
//     // this.autoPlay = true
//     this.playing=false
//     this.state={autoPlay:true}
//
//   }
//
//   onChangeAutoPlay(event){
//     if(this.state.autoPlay){
//       this.playing=false
//     }
//     this.setState({autoPlay:!this.state.autoPlay})
//   }
//
//   doAutoPlay() {
//     if (this.state.autoPlay){
//       if (this.props.states != null){
//         if(this.props.stateIndex<this.props.states.length){
//           this.playing=true
//           this.props.onNextSelect()
//           setTimeout(this.doAutoPlay, 2000)
//         }}
//       }
//     }
//
//     componentDidMount(){
//       if (!this.playing){
//         this.doAutoPlay()
//       }
//     }
//
//     componentDidUpdate(){
//       if (!this.playing){
//         this.doAutoPlay()
//       }
//     }
//
//
//     render() {
//     }

    export default GameStateViewer;
