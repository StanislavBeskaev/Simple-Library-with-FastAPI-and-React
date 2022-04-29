import React from "react"
import Select from "react-select"


const AuthorSelect = ({authors, author, onChange, required = true, isClearable = false }) => (
  <div className="mb-3" style={{position: "relative"}}>
    <label htmlFor="author" className="form-label">Автор</label>
    <Select
      options={authors}
      defaultValue={author}
      onChange={onChange}
      placeholder="Выберите автора"
      isClearable={isClearable}
    >
    </Select>
    <input
      tabIndex={-1}
      autoComplete="off"
      style={{ opacity: 0, height: 0, position: "absolute", top: "65px", left: "50%" }}
      value={author}
      onChange={() => null}
      required={required}
    />
    <div id="author_error" className="form-text text-danger" />
  </div>
)

export default AuthorSelect