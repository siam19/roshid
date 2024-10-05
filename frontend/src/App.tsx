import React, { useState } from 'react'
import { useLocation } from 'react-router-dom'

import './App.css'
import Layout from './Layout'

import OrderPage from './pages/OrderPage'
import StorePage from './pages/StorePage'
import ViewsPage from './pages/ViewsPage'

function App() {
  const [count, setCount] = useState(0)
  const location = useLocation()

  return (
    <>

        {location.pathname === '/' && <OrderPage />}
        

    </>
  )
}

export default App