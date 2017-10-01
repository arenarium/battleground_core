
function getTargetTurn(oldTurn,newTurn,maxTurn){
  // if (isNaN(newTurn)) return(oldTurn)
  return (Math.min(Math.max(0,newTurn),maxTurn))
}

function autoIncrement(state){
  if (state.autoPlay){
    return getTargetTurn(state.stateIndex,state.stateIndex+1,state.stateArray.length-1);
  }else {
    return state.stateIndex
  }
}

const gameStates = (state = {didInvalidate: true, stateArray:[], stateIndex:0,autoPlay:true}, action) => {
  switch (action.type) {
    case 'SELECT_TURN':
    return ({
      ...state,
        stateIndex: getTargetTurn(state.stateIndex,action.turnNum,state.stateArray.length-1)
        })
        case 'AUTO_INCREMENT_TURN':
        return ({
          ...state,
            stateIndex: autoIncrement(state)
            })
    case 'REQUEST_STATES':
    return ({
      ...state,
        isFetching: true,
        didInvalidate: false
  })
  case 'RECEIVE_STATES':
  return ({
    ...state,
      isFetching: false,
      didInvalidate: false,
      stateArray: action.data,
  })
  case 'CHANGE_AUTOPLAY':
  return ({
    ...state,
      autoPlay:!state.autoPlay
  })
  default:
  return state
}
}


export default gameStates
