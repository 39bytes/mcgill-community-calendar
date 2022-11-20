/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./community_calendar/templates/**/*.html",
    "./community_calendar/static/src/**/*.js",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("flowbite/plugin")],
};
