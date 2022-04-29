import React from "react"

const FormInput = ({id, label, type, value, onChange, required = true, classes= []}) => {
  classes.push("mb-3")
  return (
    <div className={classes.join(" ")}>
      <label htmlFor={id} className="form-label">{label}</label>
      <input
        id={id}
        type={type}
        className="form-control"
        value={value}
        onChange={onChange}
        required={required}
      />
      <div id={`${id}_error`} className="form-text text-danger" />
    </div>
  )
}
export default FormInput