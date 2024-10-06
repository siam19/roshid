import exp from "constants";
import React from "react";
import Layout from "../Layout";
import NewOrderButton from "./NewOrderButton";
import { Link, Outlet } from "react-router-dom";

import RecentOrders from "./RecentOrders";

function OrderPage() {
  return (
    
    <>
    <Layout>
    <div className="flex flex-col">
    <div className="">
      <NewOrderButton />
    <div className="">
      <RecentOrders />
    </div>
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