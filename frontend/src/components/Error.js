import React from "react"


const Error = ({text}) => (
  <div className="text-danger mt-3">
    {text || "Произошла ошибка, попробуйте позже"}
  </div>
)

export default Error