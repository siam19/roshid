import React, { useState, useEffect, useRef } from 'react'
import { X, Upload, Minus, Plus, Loader2 } from 'lucide-react'
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
    const [isProcessing, setIsProcessing] = useState(false);
    const [uploadedImage, setUploadedImage] = useState<string | null>(null);
    const [createdOrder, setCreatedOrder] = useState<Order | null>(null)
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [formErrors, setFormErrors] = useState({
        name: '',
        phone: '',
        address: '',
      })


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
    // Clear the error when the user starts typing
    setFormErrors(prev => ({ ...prev, [name]: '' }))
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

  useEffect(() => {
    const handlePaste = async (e: ClipboardEvent) => {
      const items = e.clipboardData?.items;
      if (!items) return;

      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          const blob = items[i].getAsFile();
          if (blob) {
            await processFile(blob);
          }
          break;
        }
      }
    };

    window.addEventListener('paste', handlePaste);
    return () => {
      window.removeEventListener('paste', handlePaste);
    };
}, []);

const handleButtonClick = () => {
    fileInputRef.current?.click();
  };


  const processFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    setUploadedImage(URL.createObjectURL(file));
    setIsProcessing(true);
    try {
      const response = await fetch('/api/llm/extract/customer_data', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload file');
      }

      const data = await response.json();
      setFormData({
        name: data.name || '',
        phone: data.phone || '',
        address: data.address || '',
        additionalInstructions: data.instructions || '',
      });
    } catch (error) {
      console.error('Error processing file:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const validateForm = () => {
    let errors = {
        name: '',
        phone: '',
        address: '',
    }
    let isValid = true

    if (!formData.name.trim()) {
        errors.name = 'Name is required'
        isValid = false
    }

    if (!formData.address.trim()) {
        errors.address = 'Address is required'
        isValid = false
    }

    if (!formData.phone.trim()) {
        errors.phone = 'Phone number is required'
        isValid = false

    } else if (!/^\d{11,14}$/.test(formData.phone)) {
        errors.phone = 'Phone number should be at least 11 digits'
        isValid = false
    }

    setFormErrors(errors)
    return isValid
}
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    await processFile(file);
  };
  
  
  const handleDraft = async () => {
    if (!validateForm()) {
        console.log('Form validation failed')
        return
    }

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
    if (!validateForm()) {
        console.log('Form validation failed')
        return
    }
    console.log('Form data:', { customer_data: formData, products: selectedProducts, deliveryMethod })
  }
  
  const handleCloseInvoice = () => {
    setCreatedOrder(null)
    window.location.href = '/';
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
          <h2 className="text-2xl font-medium">New Order</h2>
          
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-6 w-6" />
          </Button>
        </div>

        <div className="mb-6 flex flex-col justify-center items-center">
        <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        accept="image/*"
        className="hidden"
        id="fileUpload"
      />
      <Button 
        variant="outline" 
        onClick={handleButtonClick} 
        disabled={isProcessing}
        hidden={isProcessing}
        className='transition-all ease-in-out hover:py-10 hover:px-6 '
      >
        <Upload className="mr-2 h-4 w-4" /> Upload Screenshot
      </Button>

      {/* <Button disabled hidden={isProcessing}>
        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      Extracting
    </Button> */}
      <p className="text-sm mt-2 text-gray-500">
        You can also paste an image using Ctrl+V (or Cmd+V on Mac)
      </p>
      {uploadedImage && (
        <img src={uploadedImage} alt="Uploaded" className="max-w-xs mt-4" />
      )}
          </div>

          <div className={`space-y-4 mb-6 ${isProcessing ? 'cursor-not-allowed' : ''}`}>
                    <h3 className="text-lg font-medium">Customer Information</h3>
                    <div>
                        <Input
                            name="name"
                            placeholder="Name"
                            value={formData.name}
                            onChange={handleInputChange}
                            disabled={isProcessing}
                        />
                        {formErrors.name && <p className="text-red-500 text-sm mt-1">{formErrors.name}</p>}
                    </div>
                    <div>
                        <Input
                            name="phone"
                            placeholder="Phone"
                            value={formData.phone}
                            onChange={handleInputChange}
                            disabled={isProcessing}
                        />
                        {formErrors.phone && <p className="text-red-500 text-sm mt-1">{formErrors.phone}</p>}
                    </div>
                    <div>
                        <Input
                            name="address"
                            placeholder="Address"
                            value={formData.address}
                            onChange={handleInputChange}
                            disabled={isProcessing}
                        />
                        {formErrors.address && <p className="text-red-500 text-sm mt-1">{formErrors.address}</p>}
                    </div>
                    <Textarea
                        name="additionalInstructions"
                        placeholder="Additional Instructions"
                        value={formData.additionalInstructions}
                        onChange={handleInputChange}
                        disabled={isProcessing}
                    />
                </div>

        <div className="mb-6">
          <h3 className="text-lg font-medium mb-2">Product Selection</h3>
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
                    <h4 className="font-medium">{product.name}</h4>
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
          <p className='font-medium text-right my-3'>
            Amount to Collect: <span className='text-2xl  '>{selectedProducts.reduce((total, product) => total + product.base_price * product.quantity, 0)}</span> TK
          </p>
        </div>

        <div className="mb-6">
          <h3 className="text-lg font-medium mb-2">Delivery Method</h3>
          <div className="flex space-x-4">
            <Button
              variant={deliveryMethod === 'Steadfast' ? 'default' : 'outline'}
              onClick={() => setDeliveryMethod('Steadfast')}
              className='focus:bg-green-600 focus:text-white hover:bg-green-600 hover:text-white py-5'
            >
              Steadfast
            </Button>
            <Button
              variant={deliveryMethod === 'None' ? 'default' : 'outline'}
              onClick={() => setDeliveryMethod('None')}
              className='focus:bg-red-600 focus:text-white hover:bg-red-600 hover:text-white py-5'
            >
              Pathao Courier
            </Button>
            <Button
              variant={deliveryMethod === 'None' ? 'default' : 'outline'}
              onClick={() => setDeliveryMethod('None')}
              className='focus:bg-gray-500 focus:text-white hover:bg-gray-500 hover:text-white py-5'
            >
              None
            </Button>
          </div>
        </div>

        <div className="flex justify-end space-x-4">
          <Button variant="outline" className='hover:bg-blue-800 hover:text-white' onClick={handleDraft}>
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