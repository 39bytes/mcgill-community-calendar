/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
  "./codejamapp/templates/**/*.html",
  "./codejamapp/static/src/**/*.js",
  "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
  },
  plugins: [
        require('flowbite/plugin')
    ],
}
