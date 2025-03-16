"use client"
import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function Home() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        // Use /api route instead of direct backend URL
        const response = await fetch('/api/products/all');
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Roshid Products</h1>
      <a href="/app" className="text-blue-500 hover:underline mb-4 inline-block">Go to App</a>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {products.map((product) => (
          <div key={product._id} className="border p-4 rounded shadow-sm hover:shadow-md">
            <h2 className="font-bold text-lg">{product.content?.name || 'Unnamed Product'}</h2>
            <p className="text-gray-600">{product.content?.description || 'No description'}</p>
            <p className="font-semibold mt-2">Price: ৳{product.price.toFixed(2)}</p>
            <p>Store: {product.store_id}</p>
            <p>Delivery: {product.delivery_method}</p>
            <Link href={`/products/${product._id}`} className="mt-2 inline-block text-blue-500 hover:underline">
              View Details
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}