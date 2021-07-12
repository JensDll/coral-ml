module.exports = {
  purge: ['./src/**/*.html', './src/**/*.vue', './src/**/*.jsx'],
  darkMode: false,
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      ...require('tailwindcss/colors')
    },
    extend: {
      fontFamily: {
        body: ["'Montserrat', sans-serif"]
      }
    }
  },
  variants: {
    extend: {}
  },
  plugins: []
}
