import React, { useState } from 'react'
import OrderInvoice from './modals/OrderInvoiceModal'

interface Order {
  roshid_id: string
  customer_data: {
    name: string
    phone: string
  }
  cart_items: Array<{
    name: string
    quantity: number
  }>
}

interface OrderSummaryProps {
  order: Order
}

export default function OrderSummary({ order }: OrderSummaryProps) {
  const [showInvoice, setShowInvoice] = useState(false)

  return (
    <>
      <div 
        className="p-4 border-b last:border-b-0 hover:bg-gray-100 rounded-xl bg-gray-50 cursor-pointer transition-colors flex items-center justify-between"
        onClick={() => setShowInvoice(true)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            setShowInvoice(true)
          }
        }}
        tabIndex={0}
        role="button"
        aria-label={`View details for order ${order.roshid_id}`}
      >
        <div className="flex-1 mr-4">
          <span className="font-medium">{order.roshid_id}</span>
        </div>
        <div className="flex-1 mr-4">
          <span>{order.customer_data.name}</span>
        </div>
        <div className="flex-1 mr-4">
          <span>{order.customer_data.phone}</span>
        </div>
        <div className="flex-1 mr-4">
          <span className="text-sm">{order.base_price} <span className='text-teal-400'>৳</span></span>
        </div>
        <div className="flex-none">
          <span className="text-sm font-medium text-yellow-600">Pending</span>
        </div>
      </div>
      {showInvoice && (
        <OrderInvoice order={order} onClose={() => setShowInvoice(false)} />
      )}
    </>
  )
}