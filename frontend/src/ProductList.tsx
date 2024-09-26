import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

// define product type
interface Product {
  id: number;
  name: string;
  description: string;
  image: string;
  base_price: number;
  weight_category: string;
  variants: Variant[];
}

interface Variant {
    name: string;
    description: string;
    possible_values: string[];
}


const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://localhost/api/products');
        if (!response.ok) {
          throw new Error('Failed to fetch products');
        }
        const data = await response.json();
        setProducts(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {products.map((product: Product, index) => (
        <Card key={index} className="w-full">
          <CardHeader>
            <CardTitle>{product.name}</CardTitle>
            <CardDescription>{product.description}</CardDescription>
          </CardHeader>
          <CardContent>
            <img src={product.image} alt={product.name} className="w-full h-48 object-cover mb-4" />
            <p className="font-bold">Base Price: ${product.base_price}</p>
            <p>Weight Category: {product.weight_category}</p>
            <div className="mt-4">
              <h4 className="font-semibold">Variants:</h4>
              {product.variants.map((variant, vIndex) => (
                <div key={vIndex} className="mt-2">
                  <h5 className="font-medium">{variant.name}</h5>
                  <p>{variant.description}</p>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {variant.possible_values.map((value, pIndex) => (
                      <Badge key={pIndex} variant="secondary">{value}</Badge>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default ProductList;