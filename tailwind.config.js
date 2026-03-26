/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,svelte}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["Plus Jakarta Sans", "sans-serif"]
      },
      colors: {
        ink: "#0f172a",
        mist: "#eff6ff",
        coral: "#ff6b57",
        teal: "#0f766e",
        sand: "#f7f2ea",
        night: "#07111f",
        dusk: "#0f172a",
        aurora: "#22d3ee",
        violet: "#8b5cf6"
      },
      boxShadow: {
        panel: "0 24px 80px rgba(15, 23, 42, 0.12)",
        "panel-dark": "0 24px 80px rgba(2, 6, 23, 0.45)"
      }
    }
  },
  plugins: []
};
