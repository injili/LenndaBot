/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    extend: {
      colors: {
        first: "#CDC6C3",
        second: "#E2DAD0",
        third: "#866953",
        forth: "#571F31",
      }
    },
  },
  plugins: [],
}

