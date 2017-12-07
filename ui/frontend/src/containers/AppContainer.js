// Containers are wrappers around components that implement mapping from
// state variables to props
// dispatch functions to props

import { connect } from 'react-redux'
import { fetchGames ,doAutoPlay} from '../actions'
import App from '../components/App'
import 'whatwg-fetch'


const mapStateToProps = state => {

  return {
    gameID:state.gameID,
    gameArray: state.gameArray
  }
}

const mapDispatchToProps = dispatch => {
  return {
    populateGameList: gameType => {
      dispatch(fetchGames(gameType))
    },
    doAutoPlay: (delay) => {
      dispatch(doAutoPlay(delay))
    }
  }
}

const AppContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(App)

export default AppContainer
