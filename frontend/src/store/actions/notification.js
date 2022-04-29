import {ADD_NOTIFICATION, DELETE_NOTIFICATION} from "../actionTypes"

export function addNotification(notification) {
  return {
    type: ADD_NOTIFICATION,
    payload: notification
  }
}

function deleteNotification(id) {
  return {
    type: DELETE_NOTIFICATION,
    payload: id
  }
}

export function deleteNotificationById(id) {
  return async dispatch => {
    const notification = document.getElementById(id)
    notification.classList.remove("animated")
    notification.classList.add("animated-back")
    setTimeout(() => {
      dispatch(deleteNotification(id))
    }, 500)
  }
}