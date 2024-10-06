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
    <div className="space-y-4 w-2/3 rounded-xl">
      <h2 className="text-2xl font-bold mb-4">Recent Orders</h2>
      {orders.map(order => (
        <OrderSummary key={order.roshid_id} order={order} />
      ))}
    </div>
  )
}