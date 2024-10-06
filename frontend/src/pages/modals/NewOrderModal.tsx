import React, { useState, useEffect } from 'react'
import { X, Upload, Minus, Plus, Share2 } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import OrderInvoice from './OrderInvoiceModal'

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

interface CartItem {
    name: string
    base_price: number
    quantity: number
}

interface Product {
  name: string
  base_price: number
  weight_category: string
  image: string | null
  description: string | null
  variants: any[]
}

interface SelectedProduct {
  name: string
  base_price: number
  quantity: number
}
export default function NewOrderModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
    const [products, setProducts] = useState<Product[]>([])
    const [selectedProducts, setSelectedProducts] = useState<SelectedProduct[]>([])
    const [deliveryMethod, setDeliveryMethod] = useState<'Steadfast' | 'None'>('None')
    const [formData, setFormData] = useState({
      name: '',
      phone: '',
      address: '',
      additionalInstructions: '',
    })
    const [createdOrder, setCreatedOrder] = useState<Order | null>(null)


  useEffect(() => {
    fetch('/api/products')
      .then(response => response.json())
      .then(data => {
        console.log('Fetched data:', data)
        setProducts(data)
      })
      .catch(error => console.error('Error fetching products:', error))
  }, [])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleProductSelect = (product: Product) => {
    setSelectedProducts(prev => {
      const existingProduct = prev.find(p => p.name === product.name)
      if (existingProduct) {
        return prev.filter(p => p.name !== product.name)
      } else {
        return [...prev, { name: product.name, base_price: product.base_price, quantity: 1 }]
      }
    })
  }

  const handleQuantityChange = (productName: string, change: number) => {
    setSelectedProducts(prev => 
      prev.map(p => 
        p.name === productName 
          ? { ...p, quantity: Math.max(1, p.quantity + change) } 
          : p
      )
    )
  }

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log('File uploaded:', e.target.files)
  }

  const handleDraft = async () => {
    const customerData = {
      name: formData.name,
      phone: formData.phone,
      address: formData.address,
      instructions: formData.additionalInstructions,
    }

    const orderData = {
      customer_data: customerData,
      cart_items: selectedProducts,
      delivery_method: deliveryMethod,
    }

    try {
      console.log(JSON.stringify(orderData))
      const response = await fetch('/api/orders/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
      })
      if (response.ok) {
        const createdOrder = await response.json()
        console.log('Order drafted successfully')
        setCreatedOrder(createdOrder)
      } else {
        console.error('Failed to draft order')
      }
    } catch (error) {
      console.error('Error drafting order:', error)
    }
  }

  const handleConfirmPickup = () => {
    console.log('Form data:', { customer_data: formData, products: selectedProducts, deliveryMethod })
  }
  
  const handleCloseInvoice = () => {
    setCreatedOrder(null)
    onClose()
  }
  if (!isOpen) return null

  if (createdOrder) {
    return <OrderInvoice order={createdOrder} onClose={handleCloseInvoice} />
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">New Order</h2>
          
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-6 w-6" />
          </Button>
        </div>

        <div className="mb-6 flex justify-center">
          <Button variant="outline" onClick={() => document.getElementById('fileUpload')?.click()}>
            <Upload className="mr-2 h-4 w-4" /> Upload Screenshot
          </Button>
          <input
            id="fileUpload"
            type="file"
            className="hidden"
            onChange={handleFileUpload}
            accept="image/*"
          />
        </div>

        <div className="space-y-4 mb-6">
          <h3 className="text-lg font-semibold">Customer Information</h3>
          <Input
            name="name"
            placeholder="Name"
            value={formData.name}
            onChange={handleInputChange}
          />
          <Input
            name="phone"
            placeholder="Phone"
            value={formData.phone}
            onChange={handleInputChange}
          />
          <Input
            name="address"
            placeholder="Address"
            value={formData.address}
            onChange={handleInputChange}
          />
          <Textarea
            name="additionalInstructions"
            placeholder="Additional Instructions"
            value={formData.additionalInstructions}
            onChange={handleInputChange}
          />
        </div>

        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Product Selection</h3>
          <div className="grid grid-cols-2 gap-4">
            {products.map((product) => {
              const selectedProduct = selectedProducts.find(p => p.name === product.name)
              return (
                <Card 
                  key={product.name}
                  className={`cursor-pointer ${selectedProduct ? 'border-primary' : ''}`}
                  onClick={() => handleProductSelect(product)}
                >
                  <CardContent className="p-4">
                    <h4 className="font-semibold">{product.name}</h4>
                    <p className="text-sm text-gray-600">{product.base_price} TK</p>
                    {selectedProduct && (
                      <div className="flex items-center justify-between mt-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={(e) => {
                            e.stopPropagation()
                            handleQuantityChange(product.name, -1)
                          }}
                        >
                          <Minus className="h-4 w-4" />
                        </Button>
                        <span>{selectedProduct.quantity}</span>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={(e) => {
                            e.stopPropagation()
                            handleQuantityChange(product.name, 1)
                          }}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )
            })}
            
          </div>
          {/* Display the sum of base_price*quantity for each product */}
          <p className='font-semibold'>
            Amount to Collect: {selectedProducts.reduce((total, product) => total + product.base_price * product.quantity, 0)} TK
          </p>
        </div>

        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-2">Delivery Method</h3>
          <div className="flex space-x-4">
            <Button
              variant={deliveryMethod === 'Steadfast' ? 'default' : 'outline'}
              onClick={() => setDeliveryMethod('Steadfast')}
            >
              Steadfast
            </Button>
            <Button
              variant={deliveryMethod === 'None' ? 'default' : 'outline'}
              onClick={() => setDeliveryMethod('None')}
            >
              None
            </Button>
          </div>
        </div>

        <div className="flex justify-end space-x-4">
          <Button variant="outline" onClick={handleDraft}>
            Draft
          </Button>
          <Button onClick={handleConfirmPickup}>
            Confirm Pickup
          </Button>
        </div>
      </div>
    </div>
  )
}