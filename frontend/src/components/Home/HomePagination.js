import React from "react"
import {Pagination} from "antd"
import {
  searchBooks,
  setPage,
  setPageSize
} from "../../store/actions/searchBooks"
import {connect} from "react-redux"


const HomePagination = (props) => (
  <Pagination
    showQuickJumper={true}
    hideOnSinglePage={true}
    pageSizeOptions={[20, 40, 60]}
    current={props.page}
    total={props.bookCount}
    pageSize={props.pageSize}
    className="mb-4"
    onChange={(page, pageSize) => {
      if (page !== props.page) props.setPage(page)
      if (pageSize !== props.pageSize) props.setPageSize(pageSize)
      props.searchBooks()
    }}
  />
)

function mapStateToProps(state) {
  return {
    bookCount: state.searchBooks.bookCount,
    pageSize: state.searchBooks.params.pageSize,
    page: state.searchBooks.page,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    searchBooks: () => dispatch(searchBooks()),
    setPage: page => dispatch(setPage(page)),
    setPageSize: pageSize => dispatch(setPageSize(pageSize)),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(HomePagination)
