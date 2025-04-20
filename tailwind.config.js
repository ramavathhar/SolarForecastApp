/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {},
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html", // Include the main HTML file
    "./src/**/*.{html,js}" // Include any JS/HTML files in a src folder if you have them
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}