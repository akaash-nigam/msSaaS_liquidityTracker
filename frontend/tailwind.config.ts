import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0066FF',
        secondary: '#00C896',
        accent: '#FF6B00',
        expansion: '#00C896',
        contraction: '#FF4757',
        neutral: '#A4B0BE',
      },
    },
  },
  plugins: [],
};
export default config;
