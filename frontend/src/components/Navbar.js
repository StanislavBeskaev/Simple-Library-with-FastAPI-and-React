import React from "react"
import {Link} from "react-router-dom"

const Navbar = () => {

  return (
    <nav className="navbar navbar-dark bg-primary navbar-expand-lg p-3 sticky-top">
        <div className="navbar-brand">
          <strong>Библиотека</strong>
        </div>
        <div className="container-fluid justify-content-between">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link to="/" className="nav-link">Поиск книг</Link>
            </li>
            <li className="nav-item">
              <Link to="/create-book" className="nav-link">Добавление книги</Link>
            </li>
            <li className="nav-item">
              <Link to="/create-author" className="nav-link">Добавление автора</Link>
            </li>
          </ul>
        </div>
    </nav>
  )
}

export default Navbar