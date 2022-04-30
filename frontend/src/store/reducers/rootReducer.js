import {combineReducers} from "redux"
import {searchBooksReducer} from "./searchBooks"
import {deleteConfirmReducer} from "./deleteConfirm"


export default combineReducers({
  searchBooks: searchBooksReducer,
  deleteConfirm: deleteConfirmReducer
})