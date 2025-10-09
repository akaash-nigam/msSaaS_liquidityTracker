import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Global Liquidity Tracker",
  description: "Track the $176+ trillion global liquidity cycle in real-time",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
