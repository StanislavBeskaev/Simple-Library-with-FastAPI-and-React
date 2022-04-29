import React, {useEffect} from "react"
import {
  loadAuthors,
  searchBooks,
  setAuthorId,
  setName,
  setPage,
} from "../../store/actions/searchBooks"
import {connect} from "react-redux"
import AuthorSelect from "../AuthorSelect"
import {Input} from "antd"
import YearSearchGroup from "../BookSearch/YearSearchGroup"
import PageSearchGroup from "../BookSearch/PageSearchGroup"


const BookSearch = (props) => {

  useEffect(() => {
    if (props.authors.length === 0) {
      props.loadAuthors()
    }
    // eslint-disable-next-line
  }, [])

  const onSubmit = event => {
    event.preventDefault()
    props.setPage(1)
    props.searchBooks()
  }

  return (
    <>
      <h1 className="mb-4">Поиск книг</h1>
      <form onSubmit={onSubmit} className="mb-4 book-search" key="search_form">
        <AuthorSelect
          authors={props.authors}
          author={props.authorId ? props.authors.find(author => author.value === props.authorId) : ''}
          onChange={option => props.setAuthorId(option?.value)}
          required={false}
          isClearable={true}
        />
        <Input.Group compact className="mb-3">
          <Input
            allowClear
            placeholder="Название книги"
            value={props.name}
            onChange={e => props.setName(e.target.value)}
          />
        </Input.Group>
        <div className="mb-3 d-flex justify-content-between flex-wrap">
          <YearSearchGroup />
          <PageSearchGroup />
        </div>
        <button type="submit" className="btn btn-primary">Искать</button>
      </form>
    </>
  )

}

function mapStateToProps(state) {
  return {
    name: state.searchBooks.params.name,
    authorId: state.searchBooks.params.authorId,
    authors: state.searchBooks.authors,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    setName: name => dispatch(setName(name)),
    searchBooks: () => dispatch(searchBooks()),
    setAuthorId: id => dispatch(setAuthorId(id)),
    loadAuthors: () => dispatch(loadAuthors()),
    setPage: page => dispatch(setPage(page)),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(BookSearch)