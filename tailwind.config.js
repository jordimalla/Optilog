module.exports = {
  purge: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './templates/**/*.js',
    './static/src/**/*.js',
  ],
  darkMode: 'media', // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}