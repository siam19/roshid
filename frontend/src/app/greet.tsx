"use client";
import { getUser } from "@/queries/user";
import { useEffect, useState } from "react";


// prints the logged in user info 

export function Greet() {

  const [user, setUser] = useState(null);

  useEffect(() => {
      const fetchUser = async () => {
          const userData = await getUser();
          setUser(userData);
      };
      fetchUser();
  }, []);

  return <div>Hello {user}</div>;
}