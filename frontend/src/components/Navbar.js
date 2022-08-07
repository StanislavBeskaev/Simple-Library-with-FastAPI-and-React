import React from "react"
import {NavLink} from "react-router-dom"

const Navbar = () => {

  return (
    <nav className="navbar navbar-dark bg-primary navbar-expand-lg p-3 sticky-top">
        <div className="navbar-brand">
          <strong>Библиотека</strong>
        </div>
        <div className="container-fluid justify-content-between">
          <ul className="navbar-nav">
            <li className="nav-item">
              <NavLink to="/" className="nav-link">Поиск книг</NavLink>
            </li>
            <li className="nav-item">
              <NavLink to="/create-book" className="nav-link">Добавление книги</NavLink>
            </li>
            <li className="nav-item">
              <NavLink to="/create-author" className="nav-link">Добавление автора</NavLink>
            </li>
          </ul>
        </div>
    </nav>
  )
}

export default Navbar