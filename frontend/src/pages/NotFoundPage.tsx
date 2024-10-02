import React from "react";
import Layout from "../Layout";
import { Link } from "react-router-dom";

function NotFoundPage() {
  return (
    <Layout>
      <h1>Page Not Found</h1>
      <Link to="/">Go Back</Link>
    </Layout>
  );
}

export default NotFoundPage;