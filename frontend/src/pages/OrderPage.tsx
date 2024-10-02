import exp from "constants";
import React from "react";
import Layout from "../Layout";
import { Link, Outlet } from "react-router-dom";

const order_ids = ['AFE24', 'BJF5T', 'HY4F3']

function OrderPage() {
  return (
    
    <>
    <Layout>
    <div className="flex gap-2">
    <div className="flex flex-col gap-2 text-xl">
      {order_ids.map((order_id: string) => {
        return <Link to={`/order/${order_id}`}>Order ID: {order_id}</Link>
      })}
    </div>
    <div>
      <Outlet />
    </div>
    </div>
    </Layout>
    </>
    
  );
}
export default OrderPage;