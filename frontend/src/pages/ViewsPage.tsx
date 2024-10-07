import React from "react";
import Layout from "../Layout";
import BarChartThick from "./charts/BarChartThick";
import PieChartCounter from "./charts/PieChartCounter";
import LineChartSmooth from "./charts/LineChartSmooth";
import BarChartInteractive from "./charts/BarChartInteractive";

function ViewsPage() {
  return (
    <Layout>
      <div className="flex flex-col">
        <div className="flex md:flex-row md:justify-center gap-8 flex-col ">
          <div className="flex flex-col">
            <div className="w-full">
                <PieChartCounter />
            </div>
            <div className="w-full">
              <BarChartThick />
            </div>
          </div>
        <div className="md:w-1/2 w-full">
          <LineChartSmooth />
        </div>
        
        </div>
      </div>
        <div className="w-full flex flex-row justify-center">
        <div className="w-3/4">
          <BarChartInteractive />
        </div>
        </div>
    </Layout>
  );
}
export default ViewsPage;