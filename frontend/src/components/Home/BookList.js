import React from "react"

import {connect} from "react-redux"
import {Loader} from "../Loader"
import BookItem from "./BookItem"


const BookList = (props) => {

  const renderBooks = () => {
    return props.books.map((book, index) => {
      return <BookItem {...book} key={index}/>
    })
  }

  return (
      <div className="row mb-5">
        {
          props.loading
            ? <Loader />
            : renderBooks()
        }
      </div>
  )
}

function mapStateToProps(state) {
  return {
    loading: state.searchBooks.loading,
    books: state.searchBooks.books,
  }
}

export default connect(mapStateToProps)(BookList)
