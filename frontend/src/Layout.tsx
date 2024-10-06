import React from 'react'
import Navbar from './Navbar'


const Layout = ({children}) => {
  return (
    <>
    <div className="app h-screen flex-row">
      <div className="navbar w-full top-0 ">
        <Navbar />
      </div>
      <div className="content w-full justify-center">
        {children}
      </div>
    </div>
    </>
  )
}

export default Layout