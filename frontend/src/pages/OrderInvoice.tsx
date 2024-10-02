import React from "react";
import { useParams } from "react-router-dom";
import Layout from "../Layout";
function OrderInvoice() {
    const params = useParams<{ order_id: string }>();

  return (
    
    <div className="flex flex-col gap-2 text-xl">
      <h1>Order ID: {params.order_id}</h1>
      
    </div>
  );
}
export default OrderInvoice;