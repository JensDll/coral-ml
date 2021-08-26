module.exports = {
  purge: ['./src/**/*.html', './src/**/*.vue', './src/**/*.jsx'],
  darkMode: false,
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      ...require('tailwindcss/colors'),
      'white-90': 'rgba(255, 255, 255, 0.9)'
    },
    screens: {
      xs: '411px',
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px'
    },
    extend: {
      fontFamily: {
        body: ["'Montserrat', sans-serif"]
      },
      fill: theme => ({
        white: theme('colors.white')
      })
    }
  },
  variants: {
    extend: {
      margin: ['first']
    }
  },
  plugins: [require('@tailwindcss/forms')]
}
