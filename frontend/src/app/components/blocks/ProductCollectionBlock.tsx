'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { getUserProducts } from '@/lib/api'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"

type Product = {
  productId: string
  userId: string
  name: string
  price: number
  description: string
  images: string[]
}

type ProductCollectionBlockContent = {
  products: string[]
  style: {
    columns: string
    type: string
  }
}

export function ProductCollectionBlock({ content, userId }: { content: ProductCollectionBlockContent; userId: string }) {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchProducts() {
      try {
        const allProducts = await getUserProducts(userId)
        const filteredProducts = allProducts.filter((product: Product) => 
          content.products.includes(product.productId)
        )
        setProducts(filteredProducts)
      } catch (err) {
        setError('Failed to load products.')
      } finally {
        setLoading(false)
      }
    }

    fetchProducts()
  }, [userId, content.products])

  if (loading) {
    return <ProductSkeleton columns={content.style.columns} />
  }

  if (error) {
    return <div className="text-red-500">{error}</div>
  }

  return (
    <div className={`grid gap-4 ${content.style.columns === 'double' ? 'md:grid-cols-2' : 'md:grid-cols-1'}`}>
      {products.map((product) => (
        <Card key={product.productId} className="overflow-hidden">
          <CardHeader className="p-0">
            <div className="relative h-48">
              <Image
                src={product.images[0]}
                alt={product.name}
                fill
                className="object-cover"
              />
            </div>
          </CardHeader>
          <CardContent className="p-4">
            <CardTitle className="text-lg font-semibold mb-2">{product.name}</CardTitle>
            <p className="text-sm text-gray-600 mb-2">{product.description}</p>
            <p className="text-lg font-bold">৳{product.price}</p>
          </CardContent>
          <CardFooter className="p-4">
            <Button className="w-full">Add to Cart</Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}

function ProductSkeleton({ columns }: { columns: string }) {
  return (
    <div className={`grid gap-4 ${columns === 'double' ? 'md:grid-cols-2' : 'md:grid-cols-1'}`}>
      {[1, 2].map((i) => (
        <Card key={i} className="overflow-hidden">
          <CardHeader className="p-0">
            <Skeleton className="h-48 w-full" />
          </CardHeader>
          <CardContent className="p-4">
            <Skeleton className="h-6 w-3/4 mb-2" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-6 w-1/4" />
          </CardContent>
          <CardFooter className="p-4">
            <Skeleton className="h-10 w-full" />
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}