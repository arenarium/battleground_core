import React from 'react';
import ReactDOM from 'react-dom';

import { Provider } from 'react-redux'
import thunkMiddleware from 'redux-thunk'
// import { createLogger } from 'redux-logger'
import { createStore, applyMiddleware } from 'redux'

import './index.css';
import AppContainer from './containers/AppContainer'
import battlegroundApp from './reducers'
import registerServiceWorker from './registerServiceWorker';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';

// const loggerMiddleware = createLogger()

const store = createStore(
  battlegroundApp,
  applyMiddleware(
    thunkMiddleware, // lets us dispatch() functions
    // loggerMiddleware // neat middleware that logs actions
  )
)


ReactDOM.render(
 <Provider store={store}>
   <AppContainer/>
 </Provider>,
   document.getElementById('root'));

registerServiceWorker();
