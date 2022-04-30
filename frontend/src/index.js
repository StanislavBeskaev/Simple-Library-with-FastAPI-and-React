import React from 'react'
import ReactDOM from 'react-dom'
import {BrowserRouter} from "react-router-dom"
import reportWebVitals from './reportWebVitals'
import {NotificationContainer, NotificationManager} from 'react-notifications'
import reduxThunk from 'redux-thunk'

import 'antd/dist/antd.css'
import 'react-notifications/lib/notifications.css'
import "./index.scss"

import {applyMiddleware, compose, createStore} from "redux"
import App from './App'
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
        <NotificationContainer/>
      </React.StrictMode>
    </BrowserRouter>
  </Provider>
)

ReactDOM.render(app, document.getElementById('root'))

reportWebVitals()

const wsConnectString = `ws://${process.env.REACT_APP_WS_ADDRESS}/ws/notifications`
console.log(`wsConnectString = ${wsConnectString}`)
const ws = new WebSocket(wsConnectString)
const NOTIFICATION_TIME = 4000

ws.onmessage = (e) => {
  const {type, text} = JSON.parse(e.data)

  const notificationHandler = notificationTypeHandler[type]
  notificationHandler(text)
}

const notificationTypeHandler= {
  info: text => NotificationManager.info(text, null, NOTIFICATION_TIME),
  success: text => NotificationManager.success(text, null, NOTIFICATION_TIME),
  warning: text => NotificationManager.warning(text, null, NOTIFICATION_TIME),
  error: text => NotificationManager.error(text, null, NOTIFICATION_TIME),
}
