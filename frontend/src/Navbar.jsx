import React from 'react';
import { Sheet, SheetTrigger, SheetContent } from "@/components/ui/sheet";
import { Button } from "@/components/ui/button";

// Custom Link component to replace Next.js Link
const Link = ({ href, className, children, prefetch, ...props }) => (
  <a href={href} className={className} {...props}>
    {children}
  </a>
);

export default function Navbar() {
  return (
    <div className="flex items-center justify-between w-full top-0 py-8 px-10  bg-white dark:bg-gray-800">
      <Link href="#" className="flex items-center gap-1">
        <MountainIcon className="h-8 w-5 fill-blue-600" />
        <span className="text-xl font-medium text-slate-950">Roshid</span>
      </Link>
      <div className="hidden sm:flex flex-row w-1/3 justify-between">
        <Link href="/delivery" className="text-lg font-medium hover:underline underline-offset-4">
          Delivery
        </Link>
        <Link href="/order" className="text-lg font-medium hover:underline underline-offset-4">
          Order
        </Link>
        <Link href="/views" className="text-lg font-medium hover:underline underline-offset-4">
          Views
        </Link>

      </div>
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="outline" size="icon" className="">
            <MenuIcon className="h-6 w-6" />
            <span className="sr-only">Toggle navigation menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="right">
          <div className="w-[500px] p-4 flex flex-col-reverse">
          <Link href="/order" className="text-3xl py-10 font-medium hover:underline underline-offset-4">
              Order
            </Link>
            <Link href="/delivery" className="text-3xl py-10 font-medium hover:underline underline-offset-4">
              Delivery
            </Link>
            
            <Link href="/views" className="text-3xl py-10 font-medium hover:underline underline-offset-4">
              Views
            </Link>
            
          </div>
        </SheetContent>
      </Sheet>
    </div>
  )
}

function MenuIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="4" x2="20" y1="12" y2="12" />
      <line x1="4" x2="20" y1="6" y2="6" />
      <line x1="4" x2="20" y1="18" y2="18" />
    </svg>
  )
}

function MountainIcon(props) {
  return (
    <svg 
    {...props}
    id="Layer_1"
    data-name="Layer 1"
    xmlns="http://www.w3.org/2000/svg"
    width="12"
    height="24"
    fill="currentColor"
    viewBox="0 0 61.93 102.09"
    >

  <polygon className="cls-1 " points="53.86 86.37 0 59.34 35.94 0 51.33 9.32 25.49 51.99 61.93 70.28 53.86 86.37"/>
  <circle className="cls-1" cx="18.81" cy="90.33" r="11.76"/>
</svg>
  )
}