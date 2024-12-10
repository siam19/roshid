import Image from "next/image";
import { useEffect } from "react";
import { redirect } from "next/navigation";
import { Greet } from "@/app/greet";


export default function Home() {
  

  return (
    <Greet />

  );
}
