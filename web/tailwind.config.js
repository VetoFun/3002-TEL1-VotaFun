/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js}'],
  theme: {
    extend: {
      animation: {
        'spin-slow': 'spin 3s linear infinite',
      }
    },
  },
  daisyui: {
    themes: ["light", "dark", "cupcake", "dracula"]
  },
  plugins: [require("daisyui")],
}

