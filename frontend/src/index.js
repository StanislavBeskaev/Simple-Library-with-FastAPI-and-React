import React from 'react'
import ReactDOM from 'react-dom'
import {BrowserRouter} from "react-router-dom"
import reportWebVitals from './reportWebVitals'
import {applyMiddleware, compose, createStore} from "redux"
import reduxThunk from 'redux-thunk'

import App from './App'
import 'antd/dist/antd.css'
import "./index.scss"
import {Provider} from "react-redux"
import rootReducer from "./store/reducers/rootReducer"


const composeEnhancers =
  typeof window === 'object' &&
  window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ ?
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({
      // Specify extension’s options like name, actionsBlacklist, actionsCreators, serialize...
    }) : compose;

const enhancer = composeEnhancers(applyMiddleware(
  reduxThunk
))

export const store = createStore(rootReducer, enhancer)

const app = (
  <Provider store={store} >
    <BrowserRouter>
      <React.StrictMode>
        <App />
      </React.StrictMode>
    </BrowserRouter>
  </Provider>
)

ReactDOM.render(app, document.getElementById('root'))

reportWebVitals()
