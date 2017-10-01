import { connect } from 'react-redux'
import {selectTurn ,changeAutoPlay} from '../actions'
import {StateNav} from '../components/StateNav'


const mapStateToProps = state => {
  return {
    // gameID:state.gameID,
    stateIndex:state.gameStates.stateIndex,
    length:state.gameStates.stateArray.length-1,
    autoPlay:state.gameStates.autoPlay,

  }
}

const mapDispatchToProps = dispatch => {
  return {
    onChangeAutoPlay: ()=> dispatch(changeAutoPlay()),
    onStateSelect: (turnNum) => {
      if (!isNaN(parseInt(turnNum,10))){
        dispatch(selectTurn(parseInt(turnNum,10)))
      }
    }
  }
}


const StateNavContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(StateNav)

export default StateNavContainer
