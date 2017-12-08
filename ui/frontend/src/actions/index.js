// Actions are functions.
// Actions are called by passing them to the dispatcher from a container.
// dispatcher passes actions to reducers to update state.


export const selectGame = id => {
  return {
    type: 'SELECT_GAME',
    id
  }
}

export const selectTurn = turnNum => {
  return {
    type: 'SELECT_TURN',
    turnNum
  }
}

export const selectPage = path => {
  return {
    type: 'SELECT_PAGE',
    path
  }
}

export const requestGames = gameType => {
  return {
    type: 'REQUEST_GAMES',
    gameType
  }
}

export const receiveGames = (gameType,data) => {
  return {
    type: 'RECEIVE_GAMES',
    gameType,
    data
  }
}


export const requestStates = gameID => {
  return {
    type: 'REQUEST_STATES',
    gameID
  }
}

export const receiveStates = (gameID,data) => {
  return {
    type: 'RECEIVE_STATES',
    gameID,
    data
  }
}



export const changeAutoPlay = () => {
  return {
    type: 'CHANGE_AUTOPLAY',
  }
}

export const autoIncrementTurn = () => {
  return {
    type: 'AUTO_INCREMENT_TURN',
  }
}


export function fetchGames(gameType) {
  // Thunk middleware knows how to handle functions.
  // It passes the dispatch method as an argument to the function,
  // thus making it able to dispatch actions itself.

  return function (dispatch) {
    // First dispatch: the app state is updated to inform
    // that the API call is starting.

    dispatch(requestGames(gameType))

    // The function called by the thunk middleware can return a value,
    // that is passed on as the return value of the dispatch method.

    // In this case, we return a promise to wait for.
    // This is not required by thunk middleware, but it is convenient for us.

    return fetch('/api/games/')
      .then(
        response => response.json(),
        // Do not use catch, because that will also catch
        // any errors in the dispatch and resulting render,
        // causing an loop of 'Unexpected batch number' errors.
        // https://github.com/facebook/react/issues/6895
        error => console.log('An error occured.', error)
      )
      .then(json =>{
        // We can dispatch many times!
        // Here, we update the app state with the results of the API call.
        dispatch(receiveGames(gameType, json))
      }
      )
  }
}


export function fetchStates(gameID) {
  return function (dispatch) {
    dispatch(requestStates(gameID))
    return fetch('/api/states/'+String(gameID))
      .then(
        response => response.json(),
        error => console.log('An error occured.', error)
      )
      .then(json =>{
        dispatch(receiveStates(gameID, json))
      }
      )
  }
}




export function doAutoPlay(delayTime) {
  return function (dispatch) {
    setTimeout(()=>{
      dispatch(autoIncrementTurn())
      dispatch(doAutoPlay(delayTime))
    },
    delayTime);

  }
}
