import { combineReducers } from 'redux'
import gameList from './gameList'
import gameStates from './gameStates'

const battlegroundApp = combineReducers({
    gameList,
    gameStates
})

export default battlegroundApp
