import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './App.tsx'
import './index.css'

import OrderPage from './pages/OrderPage.tsx'
import StorePage from './pages/StorePage.tsx'
import ViewsPage from './pages/ViewsPage.tsx'
import NotFoundPage from './pages/NotFoundPage.tsx'
import OrderInvoice from './pages/OrderInvoice.tsx'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <NotFoundPage />,
  },
  {
    path: '/store',
    element: <StorePage />,

  },
  {
    path: '/views',
    element: <ViewsPage />,
  },
  {
    path: '/order',
    element: <OrderPage />,
    children: [
      {
      path: '/order/:order_id',
      element: <OrderInvoice />,
    }
  ]
  },
  

])
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router}>
      <App />
    </RouterProvider>
  </StrictMode>,
)
