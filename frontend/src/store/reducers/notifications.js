import {DELETE_NOTIFICATION, ADD_NOTIFICATION} from "../actionTypes"


const handlers = {
  [ADD_NOTIFICATION]: (state, action) => {
    const notifications = state.notifications
    const notification = action.payload
    notification.id = (new Date()).toString()
    notifications.push(notification)
    return {...state, notifications}
  },
  [DELETE_NOTIFICATION]: (state, action) =>
    ({...state, notifications: state.notifications.filter(notification => notification.id !== action.payload)}),
  DEFAULT: state => state
}

const initialState = {
  notifications: []
}


export const notificationReducer = (state = initialState, action) => {
  const handler = handlers[action.type] || handlers.DEFAULT
  return handler(state, action)
}