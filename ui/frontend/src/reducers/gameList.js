const gameList = (state = {didInvalidate: true,gameArray:[]}, action) => {
  switch (action.type) {
    case 'SELECT_GAME':
    return ({
      ...state,
        gameID:action.id
        })
    case 'REQUEST_GAMES':
    return ({
      ...state,
        isFetching: true,
        didInvalidate: false
  })
  case 'RECEIVE_GAMES':
  return ({
    ...state,
      isFetching: false,
      didInvalidate: false,
      gameArray: action.data,
  })
  default:
  return state
}
}


export default gameList
