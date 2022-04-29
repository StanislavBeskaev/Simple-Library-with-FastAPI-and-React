import {
  FINISH_BOOKS_LOADING,
  SET_BOOK_SEARCH_AUTHOR_ID,
  SET_BOOK_SEARCH_AUTHORS,
  SET_BOOK_SEARCH_BOOK_COUNT,
  SET_BOOK_SEARCH_ERROR,
  SET_BOOK_SEARCH_ISSUE_YEAR_GT,
  SET_BOOK_SEARCH_ISSUE_YEAR_LT,
  SET_BOOK_SEARCH_NAME, SET_BOOK_SEARCH_PAGE,
  SET_BOOK_SEARCH_PAGE_COUNT_GT,
  SET_BOOK_SEARCH_PAGE_COUNT_LT,
  SET_BOOK_SEARCH_PAGE_SIZE,
  SET_BOOK_SEARCH_SEARCHED,
  SET_BOOKS,
  START_BOOKS_LOADING
} from "../actionTypes"
import axios from "../../axios/axios-dj-api"
import {store} from "../../index"


export function setBookCount(number) {
  return {
    type: SET_BOOK_SEARCH_BOOK_COUNT,
    payload: number
  }
}

export function startBooksLoading() {
  return {
    type: START_BOOKS_LOADING
  }
}

export function finishBooksLoading() {
  return {
    type: FINISH_BOOKS_LOADING
  }
}

export function setBooksSearched() {
  return {
    type: SET_BOOK_SEARCH_SEARCHED
  }
}

export function setName(name) {
  return {
    type: SET_BOOK_SEARCH_NAME,
    payload: name
  }
}

export function setIssueYearGT(number) {
  return {
    type: SET_BOOK_SEARCH_ISSUE_YEAR_GT,
    payload: number
  }
}

export function setIssueYearLT(number) {
  return {
    type: SET_BOOK_SEARCH_ISSUE_YEAR_LT,
    payload: number
  }
}

export function setPageCountGT(number) {
  return {
    type: SET_BOOK_SEARCH_PAGE_COUNT_GT,
    payload: number
  }
}

export function setPageCountLT(number) {
  return {
    type: SET_BOOK_SEARCH_PAGE_COUNT_LT,
    payload: number
  }
}

function setBooks(books) {
  return {
    type: SET_BOOKS,
    payload: books
  }
}

function setAuthors(authors) {
  return {
    type: SET_BOOK_SEARCH_AUTHORS,
    payload: authors
  }
}

export function setPageSize(number) {
  return {
    type: SET_BOOK_SEARCH_PAGE_SIZE,
    payload: number
  }
}

export function setBooksSearchError(value) {
  return {
    type: SET_BOOK_SEARCH_ERROR,
    payload: value
  }
}

export function setAuthorId(id) {
  return {
    type: SET_BOOK_SEARCH_AUTHOR_ID,
    payload: id
  }
}

export function setPage(number) {
  return {
    type: SET_BOOK_SEARCH_PAGE,
    payload: number
  }
}

function makeSearchString() {
  const state = store.getState()
  const {name, issueYearGT, issueYearLT, pageSize, pageCountGT, pageCountLT, authorId} = state.searchBooks.params
  const {page} = state.searchBooks
  let searchParams = []
  if (name) searchParams.push(`name=${name}`)
  if (issueYearGT) searchParams.push(`issue_year__gte=${issueYearGT}`)
  if (issueYearLT) searchParams.push(`issue_year__lte=${issueYearLT}`)
  if (pageCountGT) searchParams.push(`page_count__gte=${pageCountGT}`)
  if (pageCountLT) searchParams.push(`page_count__lte=${pageCountLT}`)
  if (authorId) searchParams.push(`author=${authorId}`)
  searchParams.push(`page=${page}`)
  searchParams.push(`page_size=${pageSize}`)
  return searchParams.join('&')
}

export function searchBooks() {
  return async dispatch => {
    const state = store.getState()
    const {searched, error} = state.searchBooks
    dispatch(startBooksLoading())
    try {
      const response = await axios.get(`books/?${makeSearchString()}`)
      console.log('book search response', response)
      dispatch(setBooks(response.data.results))
      dispatch(setBookCount(response.data.count))
      if (!searched) dispatch(setBooksSearched(true))
      if (error) dispatch(setBooksSearchError(false))
    } catch (e) {
      console.log("book search error:", e)
      dispatch(setBooksSearchError(true))
    }
    dispatch(finishBooksLoading())
  }
}

export function loadAuthors() {
  return async dispatch => {
    const state = store.getState()
    const {error} = state.searchBooks
    try {
      dispatch(startBooksLoading())
      const response = await axios.get('/authors/')
      let apiAuthors = []
      response.data.forEach(author => {
        apiAuthors.push({value: author.id, label: `${author.name} ${author.surname}`})
      })
      dispatch(setAuthors(apiAuthors))
      if (error) dispatch(setBooksSearchError(false))
    } catch (e) {
      console.log('load authors error:', e)
      dispatch(setBooksSearchError(true))
    }
    dispatch(finishBooksLoading())
  }
}