import React from "react"

import {connect} from "react-redux"
import BookSearch from "../components/Home/BookSearch"
import BookResult from "../components/Home/BookResult"
import Error from "../components/Error"
import withNotifications from "../hoc/Notifications"


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

export default withNotifications(connect(mapStateToProps)(Home))

