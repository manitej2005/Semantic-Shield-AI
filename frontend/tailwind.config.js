/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "hsl(224, 71%, 4%)",
        foreground: "hsl(213, 31%, 91%)",
        soc: {
          dark: "#090d16",
          card: "#0f172a",
          border: "#1e293b",
          accent: "#0284c7",
          glow: "rgba(14, 165, 233, 0.15)",
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
}
