import {
  FINISH_BOOKS_LOADING,
  SET_BOOK_SEARCH_AUTHOR_ID,
  SET_BOOK_SEARCH_AUTHORS,
  SET_BOOK_SEARCH_BOOK_COUNT,
  SET_BOOK_SEARCH_ERROR,
  SET_BOOK_SEARCH_ISSUE_YEAR_GT,
  SET_BOOK_SEARCH_ISSUE_YEAR_LT,
  SET_BOOK_SEARCH_NAME,
  SET_BOOK_SEARCH_PAGE_COUNT_GT,
  SET_BOOK_SEARCH_PAGE_COUNT_LT,
  SET_BOOK_SEARCH_PAGE,
  SET_BOOK_SEARCH_PAGE_SIZE,
  SET_BOOK_SEARCH_SEARCHED,
  SET_BOOKS,
  START_BOOKS_LOADING,
} from "../actionTypes"


const handlers = {
  [SET_BOOK_SEARCH_BOOK_COUNT]: (state, action) => ({...state, bookCount: action.payload}),
  [START_BOOKS_LOADING]: state => ({...state, loading: true}),
  [FINISH_BOOKS_LOADING]: state => ({...state, loading: false}),
  [SET_BOOK_SEARCH_ERROR]: (state, action) => ({...state, error: action.payload}),
  [SET_BOOK_SEARCH_SEARCHED]: state => ({...state, searched: true}),
  [SET_BOOK_SEARCH_NAME]: (state, action) => ({...state, params: {...state.params, name: action.payload}}),
  [SET_BOOK_SEARCH_ISSUE_YEAR_GT]: (state, action) => ({...state, params: {...state.params, issueYearGT: action.payload}}),
  [SET_BOOK_SEARCH_ISSUE_YEAR_LT]: (state, action) => ({...state, params: {...state.params, issueYearLT: action.payload}}),
  [SET_BOOKS]: (state, action) => ({...state, books: action.payload}),
  [SET_BOOK_SEARCH_AUTHORS]: (state, action) => ({...state, authors: action.payload}),
  [SET_BOOK_SEARCH_PAGE_SIZE]: (state, action) => ({...state, params: {...state.params, pageSize: action.payload}}),
  [SET_BOOK_SEARCH_PAGE_COUNT_GT]: (state, action) => ({...state, params: {...state.params, pageCountGT: action.payload}}),
  [SET_BOOK_SEARCH_PAGE_COUNT_LT]: (state, action) => ({...state, params: {...state.params, pageCountLT: action.payload}}),
  [SET_BOOK_SEARCH_AUTHOR_ID]: (state, action) => ({...state, params: {...state.params, authorId: action.payload}}),
  [SET_BOOK_SEARCH_PAGE]: (state, action) => ({...state, page: action.payload}),
  DEFAULT: state => state
}

const initialState = {
  loading: false,
  error: false,
  page: 1,
  books: [],
  authors: [],
  searched: false,
  bookCount: null,
  params: {
    name: '',
    issueYearGT: '',
    issueYearLT: '',
    pageSize: 20,
    pageCountGT: '',
    pageCountLT: '',
    authorId: '',
  },
}


export const searchBooksReducer = (state = initialState, action) => {
  const handler = handlers[action.type] || handlers.DEFAULT
  return handler(state, action)
}