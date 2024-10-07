import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import {RoshidIcon } from "../Navbar"
interface CartItem {
  name: string
  base_price: number
  quantity: number
}

interface Order {
  roshid_id: string
  customer_data: {
    name: string
    phone: string
    address: string
    instructions: string
  }
  cart_items: CartItem[]
  base_price: number
  delivery_method?: {
    vendor_name: string
  }
}

export default function OrderInvoicePage() {
  const { roshid_id } = useParams<{ roshid_id: string }>()
  const [order, setOrder] = useState<Order | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const response = await fetch(`/api/orders/${roshid_id}`)
        if (response.ok) {
          const data = await response.json()
          setOrder(data)
        } else {
          console.error('Failed to fetch order')
        }
      } catch (error) {
        console.error('Error fetching order:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchOrder()
  }, [roshid_id])

  if (loading) {
    return <div>Loading...</div>
  }

  if (!order) {
    return <div>Order not found</div>
  }

  return (
    <div className="container mx-auto p-4 pt-8 text-left">
        
      <h1 className="text-2xl font-medium mb-6"><RoshidIcon  className="fill-blue-600 inline scale-150" /> Order Invoice</h1>
      
      <div className="space-y-6">
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-normal mb-4">Customer Details</h2>
          <p className='mb-4'><span className='font-medium mr-1 text-gray-400'>Order ID:</span> <span className='bg-blue-300 text-md p-3 py-2 rounded-full'>#{order.roshid_id}</span></p> 
          <p><span className='font-medium mr-1 text-gray-400'>Name:</span> {order.customer_data.name}</p>
          <p><span className='font-medium mr-1 text-gray-400'>Phone:</span> {order.customer_data.phone}</p>
          <p><span className='font-medium mr-1 text-gray-400'>Address:</span> {order.customer_data.address}</p>
          <p><span className='font-medium mr-1 text-gray-400'>Instructions:</span> {order.customer_data.instructions}</p></div>
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-medium mb-4">Delivery Status</h2>
          <Badge variant="secondary" className="text-md bg-teal-500 text-slate-50 animate-pulse">Pending</Badge>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-medium mb-4">Order Items</h2>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Item</TableHead>
                <TableHead>Quantity</TableHead>
                <TableHead>Price</TableHead>
                <TableHead>Total</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {order.cart_items.map((item, index) => (
                <TableRow key={index}>
                  <TableCell>{item.name}</TableCell>
                  <TableCell>{item.quantity}</TableCell>
                  <TableCell>{item.base_price} TK</TableCell>
                  <TableCell>{item.base_price * item.quantity} TK</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="text-right mt-4">
            <p className="text-lg font-medium">Total: <span className='text-2xl'>{order.base_price}</span> TK</p>
          </div>
        </div>

        {order.delivery_method && (
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-medium mb-4">Delivery</h2>
            <p>Vendor: {order.delivery_method}</p>
          </div>
        )}

        
      </div>
    </div>
  )
}