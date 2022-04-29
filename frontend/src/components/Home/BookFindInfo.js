import React from "react"
import {connect} from "react-redux"


const BookFindInfo = (props) => {

  return (
    <>
      {
        props.searched
          ? <div className="mb-3" id={0}>Найдено книг: {props.bookCount}</div>
          : null
      }
    </>
  )
}

function mapStateToProps(state) {
  return {
    searched: state.searchBooks.searched,
    bookCount: state.searchBooks.bookCount,
  }
}

export default connect(mapStateToProps)(BookFindInfo)