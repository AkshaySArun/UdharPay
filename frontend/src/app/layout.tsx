import type { Metadata } from "next";
import "./globals.css";
export const metadata:Metadata={title:"UdharPay AI — Digital Khata",description:"Your kirana's money, collected without the awkwardness."};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
