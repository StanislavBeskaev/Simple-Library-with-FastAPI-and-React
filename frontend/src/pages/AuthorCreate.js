import React, {useState} from "react"
import FormInput from "../components/FormInput"
import axios from "../axios/axios-dj-api"
import {useNavigate} from "react-router-dom"
import Error from "../components/Error"
import {connect} from "react-redux"
import {loadAuthors} from "../store/actions/searchBooks"

const AuthorCreate = (props) => {
  const [name, setName] = useState('')
  const [surname, setSurname] = useState('')
  const [birthYear, setBirthYear] = useState('')
  const [error, setError] = useState(false)

  const navigate = useNavigate()

  const inputs = [
    {
      id: "name",
      label: "Имя автора",
      type: "text",
      value: name,
      onChange: e => setName(e.target.value)
    },
    {
      id: "surname",
      label: "Фамилия автора",
      type: "text",
      value: surname,
      onChange: e => setSurname(e.target.value)
    },
    {
      id: "birth_year",
      label: "Год рождения автора",
      type: "number",
      value: birthYear,
      onChange: e => setBirthYear(e.target.value)
    },
  ]

  const clearErrors = () => {
    const fields = []
    inputs.forEach(input => fields.push(input.id))
    fields.forEach(field => {
      document.getElementById(`${field}_error`).textContent = ''
    })
  }

  const renderInputs = () =>
    inputs.map((inputData, index) => <FormInput {...inputData} key={index} />)

  const onSubmit = event => {
    event.preventDefault()
    const data = {name: name.trim(), surname: surname.trim(), birth_year: birthYear}
    clearErrors()

    axios.post('/authors/', data)
      .then(() => {
        props.loadAuthors()
        navigate('/')
      })
      .catch(e => {
        console.log('author create error', e)
        if(e.response != null){
          Object.keys(e.response.data).forEach(key => {
            const keyErrorDiv = document.getElementById(`${key}_error`)
            keyErrorDiv.textContent = e.response.data[key]
          })
        } else {
          setError(true)
        }
      })
  }

  return (
    <>
      <h1>Добавление автора</h1>
      <form onSubmit={onSubmit} className="mt-4">
        {renderInputs()}
        <button type="submit" className="btn btn-primary">Добавить</button>
      </form>
      {
        error
          ? <Error />
          : null
      }
    </>
  )
}

function mapDispatchToProps(dispatch) {
  return {
    loadAuthors: () => dispatch(loadAuthors())
  }
}

export default connect(null, mapDispatchToProps)(AuthorCreate)
