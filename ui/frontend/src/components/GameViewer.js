import React from 'react'
import { Grid, Row,Col,Panel, PageHeader } from 'react-bootstrap';
import VisibleGameIndex from '../containers/VisibleGameIndex'
import VisibleGameState from '../containers/VisibleGameState'
import 'whatwg-fetch'


 const GameViewer =() => (
  <div className="container">
    <Grid>
      <Row>
        <PageHeader><small>Watch and Learn from ongoing games or replays</small></PageHeader>
      </Row>
      <Row>
        <Col md={3}>
          <Panel>
            <VisibleGameIndex/>
          </Panel>
        </Col>
        <Col md={8}>
          <Panel>
            <VisibleGameState/>
          </Panel>
        </Col>
      </Row>
    </Grid>
  </div>
)

export default GameViewer
//
// onGameSelect={this.onGameSelect}
//   gameArray={this.state.gameArray}
//


  // states={this.state.gameStates}
  // stateIndex={this.state.stateIndex}
  // onNextSelect={this.onNextSelect}
  // onPreviousSelect={this.onPreviousSelect}
  // onStateSelect={this.onStateSelect}
//
// class GameViewer extends Component {
//   constructor(props){
//     super(props)
//     this.state = {
//       gameStates:null,
//       gameArray:null,
//       stateIndex: props.match.params.stateIndex !=null?props.match.params.stateIndex:1,
//       // gameID:props.match.params.gameID
//     }
//
//     this.onGameSelect = this.onGameSelect.bind(this)
//     this.getGamesList = this.getGamesList.bind(this)
//     this.updateMoves = this.updateMoves.bind(this)
//     this.onStateSelect = this.onStateSelect.bind(this)
//     this.onPreviousSelect = this.onPreviousSelect.bind(this)
//     this.onNextSelect = this.onNextSelect.bind(this)
//     this.changeState = this.changeState.bind(this)
//
//     this.getGamesList()
//     if (props.match.params.gameID !=null){
//       this.updateMoves(props.match.params.gameID)
//     }
//   }
//
//
//   getGamesList() {
//     fetch('/api/games/')
//     .then((response) =>{
//       return response.json()})
//       .then((value)=>{
//         this.setState({gameArray:value})
//       })
//       .catch(function(ex) {
//         console.log('parsing failed', ex)
//       })
//   }
//
//
//   updateMoves(gameID){
//     fetch('/api/states/'+gameID)
//     .then((response) =>{
//       return response.json()})
//       .then((value)=>{
//         this.setState({gameStates:value,stateIndex:1})
//         this.props.history.push("/games/"+String(gameID)+"/1/")
//       })
//       .catch(function(ex) {
//         console.log('parsing failed', ex)
//       })
//   }
//
//   onStateSelect(event){
//     console.log(event);
//     let  newStateIndex = parseInt(event.target.value)
//     this.changeState(newStateIndex)
//   }
//
//   changeState(newStateIndex){
//     this.props.history.push("../"+String(newStateIndex)+"/")
//     this.setState({stateIndex:newStateIndex})
//   }
//
//   onNextSelect(){
//     if (this.state.stateIndex<this.state.gameStates.length){
//       let  newStateIndex = parseInt(this.state.stateIndex)+1
//       this.changeState(newStateIndex)
//     }
//   }
//
//   onPreviousSelect(){
//     if (this.state.stateIndex>0){
//       let  newStateIndex = parseInt(this.state.stateIndex)-1
//       this.changeState(newStateIndex)
//     }
//   }
//
//   onGameSelect(eventKey){
//     this.updateMoves(eventKey)
//   }
//
//   render() {
//     return(
//       <div className="container">
//         <Grid>
//           <Row>
//             <PageHeader><small>Watch and Learn from ongoing games or replays</small></PageHeader>
//           </Row>
//           <Row>
//             <Col md={3}>
//               <Panel>
//                 <GameIndex onGameSelect={this.onGameSelect}
//                   gameArray={this.state.gameArray}/>
//                   </Panel>
//                 </Col>
//                 <Col md={8}>
//                   <Panel>
//                     <StateArrayViewer
//                       states={this.state.gameStates}
//                       stateIndex={this.state.stateIndex}
//                       onNextSelect={this.onNextSelect}
//                       onPreviousSelect={this.onPreviousSelect}
//                       onStateSelect={this.onStateSelect}/>
//                     </Panel>
//                   </Col>
//                 </Row>
//               </Grid>
//             </div>
//           )
//     }
// }
//
// export default GameViewer
