import {combineReducers} from "redux"
import {searchBooksReducer} from "./searchBooks"
import {deleteConfirmReducer} from "./deleteConfirm"
import {notificationReducer} from "./notifications"


export default combineReducers({
  searchBooks: searchBooksReducer,
  deleteConfirm: deleteConfirmReducer,
  notifications: notificationReducer,
})