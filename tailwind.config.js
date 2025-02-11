module.exports = {
    content: [

        './node_modules/flowbite/**/*.js',
        './templates/**/*.html',  // Indique où chercher les fichiers HTML
    './admin_panel/templates/**/*.html',
    './static/src/**/*.js',  // Pour tout fichier JS de Tailwind
    ],
    theme: {
      extend: {},
    },
    plugins: [
        require('flowbite/plugin')
    ]
  }
