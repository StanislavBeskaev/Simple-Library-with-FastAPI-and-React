import React from "react"

import {connect} from "react-redux"
import BookSearch from "../components/Home/BookSearch"
import BookResult from "../components/Home/BookResult"
import Error from "../components/Error"


const Home = (props) => (
    <>
      <BookSearch />
      {
        props.error
          ? <Error text="Ошибка при поиске книг, попробуйте позже" />
          : <BookResult />
      }
    </>
  )

function mapStateToProps(state) {
  return {
    error: state.searchBooks.error
  }
}

export default connect(mapStateToProps)(Home)

