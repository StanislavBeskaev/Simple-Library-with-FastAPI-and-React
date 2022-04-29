import React, {useState, useEffect} from "react"
import {useNavigate} from "react-router-dom"

import axios from "../axios/axios-dj-api"
import {Loader} from "../components/Loader"
import FormInput from "../components/FormInput"
import AuthorSelect from "../components/AuthorSelect"
import Error from "../components/Error"
import {searchBooks} from "../store/actions/searchBooks"
import {connect} from "react-redux"
import withNotifications from "../hoc/Notifications"
import {addNotification} from "../store/actions/notification"


const BookCreate = (props) => {
  const [name, setName] = useState('')
  const [authorId, setAuthorID] = useState('')
  const [isbn, setIsbn] = useState('')
  const [issueYear, setIssueYear] = useState('')
  const [pageCount, setPageCount] = useState('')
  const [authors, setAuthors] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)

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
    setLoading(true)

    axios.get('/authors/')
      .then(response => {
        const apiAuthors = []
        response.data.forEach(author => {
          apiAuthors.push({value: author.id, label: `${author.name} ${author.surname}`})
        })

        setAuthors(apiAuthors)
        setLoading(false)
      })
      .catch(e => {
        console.log('load authors error', e)
        setError(true)
        setLoading(false)
      })
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

    axios.post('/books/', data)
      .then(() => {
        props.addNotification({type: "success", text: `Добавлена книга ${name}`})
        props.searchBooks()
        navigate('/')
      })
      .catch(e => {
        console.log('book create error', e)
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

  if (loading) {
    return (
      <>
        <h1>Добавление книги</h1>
        <Loader text="Загрузка авторов"/>
      </>
    )
  }

  if (error) {
    return (
      <>
        <h1>Добавление книги</h1>
        <Error />
      </>
    )
  }

  return (
    <>
      <h1>Добавление книги</h1>
      <form onSubmit={onSubmit} className="mt-4">
        <AuthorSelect
          authors={authors}
          author={authorId}
          onChange={option => setAuthorID(option.value)}
        />
        {renderInputs()}
        <button type="submit" className="btn btn-primary">Добавить</button>
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

export default withNotifications(connect(null, mapDispatchToProps)(BookCreate))
