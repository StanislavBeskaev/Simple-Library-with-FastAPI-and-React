import React from "react"
import {Link} from "react-router-dom"


const BookItem = ({id, name, issue_year}) => (
  <div className="p-2 col-md-3 d-flex">
    <div className="card text-center flex-fill">
      <div className="card-body">
        <h5 className="card-title">
          <Link to={`/books/${id}`}>
            {name}
          </Link>
        </h5>
      </div>
      <div className="card-footer">
        {issue_year}г
      </div>
    </div>
  </div>
)

export default BookItem