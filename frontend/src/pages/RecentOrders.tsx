import React, { useEffect, useState } from 'react'
import OrderSummary from './OrderSummary'

interface Order {
  roshid_id: string
  customer_data: {
    name: string
    phone: string
    address: string
    instructions: string
  }
  cart_items: Array<{
    name: string
    base_price: number
    quantity: number
  }>
  base_price: number
  delivery_method: {
    vendor_name: string
  } | null
}

export default function RecentOrders() {
  const [orders, setOrders] = useState<Order[]>([])

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await fetch('/api/orders')
        const data = await response.json()
        setOrders(data)
      } catch (error) {
        console.error('Error fetching orders:', error)
      }
    }

    fetchOrders()
  }, [])

  return (
    <div className="space-y-4 w-4/5 rounded-xl ">
      <h2 className="text-2xl font-medium mb-4">Recent Orders</h2>
      <div className="flex flex-row justify-center">
      <div className="text-gray-400 w-11/12  text-sm flex items-center justify-around">
          <div className="flex-1 mr-4">
            <span className="font-medium">Roshid ID</span>
          </div>
          <div className="flex-1 mr-4">
            <span className="font-medium">Customer Name</span>
          </div>
          <div className="flex-1 mr-4">
            <span className="font-medium">Phone</span>
          </div>
          <div className="flex-1 mr-4">
            <span className="font-medium">Amount</span>
          </div>
          <div className="flex-none">
            <span className="font-medium">Status</span>
          </div>
        </div>
      </div>
      <div className="flex flex-col-reverse gap-5">
      {orders.map(order => (
        <OrderSummary key={order.roshid_id} order={order} />
      ))}
      </div>
    </div>
  )
}