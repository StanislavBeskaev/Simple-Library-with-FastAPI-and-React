import React, {useEffect, useState} from "react"
import {useParams, useNavigate} from "react-router-dom"
import axios from "../axios/axios-dj-api"
import FormInput from "../components/FormInput"
import {Loader} from "../components/Loader"
import Error from "../components/Error"
import AuthorSelect from "../components/AuthorSelect"
import {searchBooks} from "../store/actions/searchBooks"
import {connect} from "react-redux"
import {addNotification} from "../store/actions/notification"
import withNotifications from "../hoc/Notifications"


const BookChange = (props) => {
  const [name, setName] = useState('')
  const [authorId, setAuthorID] = useState('')
  const [isbn, setIsbn] = useState('')
  const [issueYear, setIssueYear] = useState('')
  const [pageCount, setPageCount] = useState('')
  const [loading, setLoading] = useState(false)
  const [authors, setAuthors] = useState([])
  const [error, setError] = useState(false)
  const bookId = useParams().id

  const navigate = useNavigate()

  const inputs = [
    {
      id: "name",
      label: "Название книги",
      type: "text",
      value: name,
      onChange: e => setName(e.target.value)
    },
    {
      id: "isbn",
      label: "ISBN",
      type: "text",
      value: isbn,
      onChange: e => setIsbn(e.target.value)
    },
    {
      id: "issue_year",
      label: "Год выпуска",
      type: "number",
      value: issueYear,
      onChange: e => setIssueYear(e.target.value)
    },
    {
      id: "page_count",
      label: "Количество страниц",
      type: "number",
      value: pageCount,
      onChange: e => setPageCount(e.target.value)
    },
  ]

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      try {
        const authorsResponse = await axios.get('/authors/')
        const apiAuthors = []
        authorsResponse.data.forEach(author => {
          apiAuthors.push({value: author.id, label: `${author.name} ${author.surname}`})
        })
        setAuthors(apiAuthors)

        const bookResponse = await axios.get(`/books/${bookId}`)
        setName(bookResponse.data.name)
        setAuthorID(bookResponse.data.author)
        setIsbn(bookResponse.data.isbn)
        setIssueYear(bookResponse.data.issue_year)
        setPageCount(bookResponse.data.page_count)
        if (error) setError(false)
      } catch (e) {
        console.log('book change fetch data error', e)
        setError(true)
      }
      setLoading(false)
    }

    fetchData()
    // eslint-disable-next-line
  }, [])

  const clearErrors = () => {
    const fields = ['author']
    inputs.forEach(input => fields.push(input.id))
    fields.forEach(field => {
      document.getElementById(`${field}_error`).textContent = ''
    })
  }

  const onSubmit = event => {
    event.preventDefault()
    const data = {name: name.trim(), isbn: isbn.trim(), issue_year: issueYear, author: authorId, page_count: pageCount}
    clearErrors()

    axios.put(`/books/${bookId}`, data)
      .then(() => {
        props.searchBooks()
        props.addNotification({text: `Изменена книга: ${name}`, type: "orange"})
        navigate(`/books/${bookId}`)
      })
      .catch(e => {
        console.log('book change error', e)
        if(e?.response) {
          Object.keys(e.response.data).forEach(key => {
            const keyErrorDiv = document.getElementById(`${key}_error`)
            keyErrorDiv.textContent = e.response.data[key][0]
          })
        } else {
          setError(true)
        }
      })
  }

  const renderInputs = () =>
    inputs.map((inputData, index) => <FormInput {...inputData} key={index} />)

  const onBack = () => {
    navigate(`/books/${bookId}`)
  }

  if (loading) {
    return (
      <>
        <button className="btn btn-link" onClick={onBack}>Назад</button>
        <h1>Изменение книги</h1>
        <Loader/>
      </>
    )
  }

  if (error) {
    return (
      <>
        <button className="btn btn-link" onClick={onBack}>Назад</button>
        <h1>Изменение книги</h1>
        <Error />
      </>
    )
  }
  return (
    <>
      <button className="btn btn-link" onClick={onBack}>Назад</button>
      <h1>Изменение книги</h1>
      <form onSubmit={onSubmit} className="mt-4">
        <AuthorSelect
          authors={authors}
          author={authors.find(author => author.value === authorId)}
          onChange={option => setAuthorID(option.value)}
        />
        {renderInputs()}
        <button type="submit" className="btn btn-primary">Изменить</button>
      </form>
    </>
  )
}

function mapDispatchToProps(dispatch) {
  return {
    searchBooks: () => dispatch(searchBooks()),
    addNotification: notification => dispatch(addNotification(notification)),
  }
}

export default withNotifications(connect(null, mapDispatchToProps)(BookChange))