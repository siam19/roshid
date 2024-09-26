import React, { useState } from 'react'

import './App.css'


import ProductList from './ProductList'
import Navbar from './Navbar'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div className="app h-screen">
      <div className="navbar w-full top-0 ">
        <Navbar />
      </div>
      <div className="content w-full">
        <ProductList />
      </div>


    </div>
    </>
  )
}

export default App
