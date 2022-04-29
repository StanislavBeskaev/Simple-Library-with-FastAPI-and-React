import React, {useEffect, useState} from "react"
import {useNavigate, useParams} from "react-router-dom"
import axios from "../axios/axios-dj-api"
import {Loader} from "../components/Loader"
import Error from "../components/Error"
import {searchBooks} from "../store/actions/searchBooks"
import {connect} from "react-redux"
import {setDeleteConfirmModalText, showDeleteConfirmModal} from "../store/actions/deleteConfirm"
import DeleteConfirmModal from "../components/modals/DeleteConfirmModal"
import withNotifications from "../hoc/Notifications"
import {addNotification} from "../store/actions/notification"


const BookDetail = (props) => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const [deleteError, setDeleteError] = useState(false)
  const [book, setBook] = useState({})
  const bookId = useParams().id

  const navigate = useNavigate()

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      try {
        const bookResponse = await axios.get(`/books/${bookId}`)
        const authorResponse = await axios.get(`/authors/${bookResponse.data.author}`)
        setBook({...bookResponse.data, author: authorResponse.data})
        if (error) setError(false)
      } catch (e) {
        console.log(`Book detail ${bookId} error: ${e}`)
        setError(true)
      }
      setLoading(false)
    }
    fetchData()
  }, [])

  const onDelete = () => {
    axios.delete(`/books/${bookId}`)
      .then(res => {
        props.addNotification({type: "danger", text: `Удалена книга: ${book.name}`})
        props.searchBooks()
        navigate('/')
      })
      .catch(e => {
        console.log(`delete book ${bookId} error: ${e}`)
        setDeleteError(true)
      })
  }

  const onChange = () => {
    navigate(`/change-book/${bookId}`)
  }

  const callDeleteConfirm = () => {
    props.setDeleteConfirmModalText(`Вы действительно хотите удалить книгу "${book.name}"?`)
    props.showDeleteConfirmModal()
  }

  if (loading) {
    return <Loader />
  }

  if (error) {
    return <Error />
  }

  return (
    <>
      <button className="btn btn-link" onClick={() => navigate('/')}>К поиску</button>
      <div className="card mt-2">
        <h5 className="card-header bg-info">{book.name}</h5>
        <div className="card-body">
          <p className="card-text" key={2}>
            Автор: {`${book.author.name} ${book.author.surname}, ${book.author.birth_year} г.р.`}
          </p>
          <p className="card-text" key={3}>ISBN: {book.isbn}</p>
          <p className="card-text" key={4}>Год выпуска: {book.issue_year}</p>
          <p className="card-text" key={5}>Количество страниц: {book.page_count}</p>
          <div className="mt-3">
            <button className="btn btn-primary" onClick={onChange}>Изменить книгу</button>
            <button className="btn btn-danger ms-3" onClick={callDeleteConfirm}>Удалить книгу</button>
          </div>
        </div>
      </div>
      <DeleteConfirmModal onDelete={onDelete} />
      {
        deleteError
          ? <Error text="Не удалось удалить книгу, попробуйте позже"/>
          : null
      }
    </>

  )
}

function mapDispatchToProps(dispatch) {
  return {
    searchBooks: () => dispatch(searchBooks()),
    showDeleteConfirmModal: () => dispatch(showDeleteConfirmModal()),
    setDeleteConfirmModalText: text => dispatch(setDeleteConfirmModalText(text)),
    addNotification: notification => dispatch(addNotification(notification)),
  }
}

export default withNotifications(connect(null, mapDispatchToProps)(BookDetail))
