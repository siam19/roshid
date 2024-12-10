const config = {
    appName: "Roshid",
    appDescription:
      "Roshid is platform for small business to flourish on social media",
    domainName:
      process.env.NODE_ENV === "development"
        ? "http://localhost"
        : "https://roshid.com",
  };
  
  export default config;
  