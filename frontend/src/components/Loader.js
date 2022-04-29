import React from "react"

export const Loader = ({text}) => (
    <div className="d-block mt-5">
      <span className="me-2">{text || "Загрузка данных"}</span>
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
)
