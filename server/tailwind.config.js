/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {},
    fontSize: {
      'xxs': '.625rem',
      'xs': '.75rem',
      'sm': '.825rem',
      'base': '1rem',
      'lg': '1.125rem',
      'xl': '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
    },
  },
  // add daisyUI plugin
  plugins: [require("daisyui")],
  // daisyUI config (optional - here are the default values)
  daisyui: {
    themes: ["light", "dark", "forest", "nord", "aqua", "retro"], // false: only light + dark | true: all themes | array: specific themes like this ["light", "dark", "cupcake"]
    darkTheme: ["nord", "aqua", "retro"], // name of one of the included themes for dark mode
    base: true, // applies background color and foreground color for root element by default
    styled: true, // include daisyUI colors and design decisions for all components
    utils: true, // adds responsive and modifier utility classes
    prefix: "", // prefix for daisyUI classnames (components, modifiers and responsive class names. Not colors)
    logs: true, // Shows info about daisyUI version and used config in the console when building your CSS
    themeRoot: ":root", // The element that receives theme color CSS variables
  },
  // safelist some classes that are rendered dynamically by Jinja
  safelist: [
      'alert-success',
      'alert-error',
      'alert-warning',
      'text-success',
      'text-error',
      'text-warning',
  ]
}

