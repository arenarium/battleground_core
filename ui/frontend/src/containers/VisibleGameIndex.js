import { connect } from 'react-redux'
import { selectGame ,fetchStates} from '../actions'
import GameIndex from '../components/GameIndex'
import 'whatwg-fetch'


const mapStateToProps = state => {
  return {
    // gameID:state.gameID,
    gameArray: state.gameList.gameArray
  }
}

const mapDispatchToProps = dispatch => {
  return {
    onGameSelect: id => {
      dispatch(selectGame(id))
      dispatch(fetchStates(id))
    }
  }
}

const VisibleGameIndex = connect(
  mapStateToProps,
  mapDispatchToProps
)(GameIndex)

export default VisibleGameIndex
