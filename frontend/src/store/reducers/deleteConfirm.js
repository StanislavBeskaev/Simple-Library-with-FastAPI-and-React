import {HIDE_DELETE_CONFIRM_MODAL, SET_DELETE_CONFIRM_TEXT, SHOW_DELETE_CONFIRM_MODAL} from "../actionTypes"


const handlers = {
  [SHOW_DELETE_CONFIRM_MODAL]: state=> ({...state, visible: true}),
  [HIDE_DELETE_CONFIRM_MODAL]: state => ({...state, visible: false}),
  [SET_DELETE_CONFIRM_TEXT]: (state, action) => ({...state, text: action.payload}),
  DEFAULT: state => state
}

const initialState = {
  visible: false,
  text: '',
}


export const deleteConfirmReducer = (state = initialState, action) => {
  const handler = handlers[action.type] || handlers.DEFAULT
  return handler(state, action)
}