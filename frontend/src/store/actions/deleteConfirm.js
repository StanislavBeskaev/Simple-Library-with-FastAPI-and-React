import {
  HIDE_DELETE_CONFIRM_MODAL,
  SET_DELETE_CONFIRM_TEXT,
  SHOW_DELETE_CONFIRM_MODAL
} from "../actionTypes"


export function setDeleteConfirmModalText(text) {
  return {
    type: SET_DELETE_CONFIRM_TEXT,
    payload: text
  }
}

export function showDeleteConfirmModal() {
  return {
    type: SHOW_DELETE_CONFIRM_MODAL
  }
}

export function hideDeleteConfirmModal() {
  return {
    type: HIDE_DELETE_CONFIRM_MODAL
  }
}
