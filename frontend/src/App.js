import React from "react"
import {Navigate, Route, Routes} from "react-router-dom"
import Home from "./pages/Home"
import BookCreate from "./pages/BookCreate"
import AuthorCreate from "./pages/AuthorCreate"
import Layout from "./components/Layout"
import BookDetail from "./pages/BookDetail"
import BookChange from "./pages/BookChange"


const App = () => (
  <>
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="create-book" element={<BookCreate />} />
        <Route path="create-author" element={<AuthorCreate />} />
        <Route path="/books/:id" element={<BookDetail />}/>
        <Route path="change-book/:id" element={<BookChange />}/>
        <Route path="*" element={<Navigate replace to="/" />} />
      </Route>
    </Routes>
  </>
)

export default App
