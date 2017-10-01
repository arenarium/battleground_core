import { connect } from 'react-redux'
import GameStateViewer from '../components/GameStateViewer'

const mapStateToProps = state => {
  // do work here
  return {
    gameState:state.gameStates.stateArray[state.gameStates.stateIndex],
  }
}

const mapDispatchToProps = dispatch => {
  return {}
}

const VisibleGameState = connect(
  mapStateToProps,
  mapDispatchToProps
)(GameStateViewer)

export default VisibleGameState
