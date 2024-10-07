import React from 'react'
import { X, Share2, Trash2, Edit2 } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import ShareInvoice from './InvoiceShare'

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

interface OrderInvoiceProps {
    order: Order
    onClose: () => void
}

export default function OrderInvoice({ order, onClose }: OrderInvoiceProps) {
    const handleDelete = async () => {
        try {
            const response = await fetch(`/api/order/delete/${order.roshid_id}`, {
                method: 'POST',
            });
            
            if (!response.ok) {
                throw new Error('Failed to delete the order');
            }
            onClose();
            window.location.href = '/';
        } catch (error) {
            console.error('Error deleting the order:', error);
        }
    };
    const handleShare = () => {
        const url = `${window.location.origin}/orders/${order.roshid_id}`;
        const tempInput = document.createElement('input');
        tempInput.value = url;
        document.body.appendChild(tempInput);
        tempInput.select();
        try {
            // TODO Change this later since execCommand is deprecated
            document.execCommand('copy');
        } catch (err) {
            console.error('Could not copy text: ', err);
        }
        document.body.removeChild(tempInput);
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center p-4">
            <div className="bg-white h-2/3 text-left  rounded-lg shadow-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                <div className="flex justify-between items-center mb-8">
                    <h2 className="text-2xl  ">Order Info<span className="bg-fuchsia-200 font-light text-sm mb-4 hover:cursor-pointer mx-2 rounded-full p-2">#{order.roshid_id}</span></h2>
                    <div className="flex space-x-2">
                    <ShareInvoice order_id={order.roshid_id} />
                        <Button variant="ghost" size="icon" onClick={onClose}>
                            <X className="h-6 w-6" />
                        </Button>
                    </div>
                </div>
                <div className="space-y-4 h-5/6 flex flex-col justify-between">
                    
                    <div className="flex flex-row w-full justify-between">
                        <div>
                            <p><strong>Name:</strong> {order.customer_data.name}</p>
                            <p><strong>Phone:</strong> {order.customer_data.phone}</p>
                            <p><strong>Address:</strong> {order.customer_data.address}</p>
                            <p><strong>Instructions:</strong> {order.customer_data.instructions}</p>
                        </div>
                        <div className="flex flex-col gap-2">
                            <Button variant="outline" size="icon" className='' onClick={() => {console.log("Not implemented")}}>
                                <Edit2 className="h-4 w-4" /> 
                            </Button>
                            <Button variant="destructive" size="icon" className='bg-red-400' onClick={handleDelete}>
                                <Trash2 className="h-4 w-4" />
                            </Button>
                            
                        </div>
                        
                    </div>

                    <div>
                        <h3 className="text-lg font-semibold mb-2">Order Items</h3>
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
                    </div>

                    <div className="m-8 text-right">
                    <span className='pr-1 text-md text-slate-700 font-bold'>Total:</span> <p className="text-2xl  text-slate-900 p-2  inline">{order.base_price} TK</p>
                    </div>

                    {order.delivery_method && (
                        <div>
                            <h3 className="text-lg font-semibold mb-2 ">Delivery</h3>
                            <p><strong>Vendor:</strong> {order.delivery_method}</p>
                        </div>
                    )}
                    
                </div>
            </div>
        </div>
    )
}