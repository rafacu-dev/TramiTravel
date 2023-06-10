/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

let a = '#d791ff',
    b = '#c15dfc',
    c = '#b941ff',
    d = '#af2cfc',
    e = '#a002fc',
    f = '#d091b4',
    g = '#bc7da0',
    h = '#a8698c',
    i = '#945f78',
    j = '#804b64';
    
/**
let a = '#5d719a',
b = '#5d719a',
c = '#5d719a',
d = '#536790',
e = '#495d86',
f = '#3f537c',
g = '#354972',
h = '#2b3f68',
i = '#21355e',
j = '#172b54';
    */

module.exports = {
    /**
     * Stylesheet generation mode.
     *
     * Set mode to "jit" if you want to generate your styles on-demand as you author your templates;
     * Set mode to "aot" if you want to generate the stylesheet in advance and purge later (aka legacy mode).
     */
    mode: "jit",

    purge: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /* 
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',
        
        /* 
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            shadow: {
            'itravel': {
                50: a,
                100: b,
                200: c,
                300: d,
                400: e,
                500: f,
                600: g,
                700: h,
                800: i,
                900: j,
              },
            },
            colors: {
            'itravel': {
                50: a,
                100: b,
                200: c,
                300: d,
                400: e,
                500: f,
                600: g,
                700: h,
                800: i,
                900: j,
              },
            },
            border: {
            'itravel': {
                50: a,
                100: b,
                200: c,
                300: d,
                400: e,
                500: f,
                600: g,
                700: h,
                800: i,
                900: j,
              },
            },
            ring: {
            'itravel': {
                50: a,
                100: b,
                200: c,
                300: d,
                400: e,
                500: f,
                600: g,
                700: h,
                800: i,
                900: j,
              },
            },
            text: {
            'itravel': {
                50: a,
                100: b,
                200: c,
                300: d,
                400: e,
                500: f,
                600: g,
                700: h,
                800: i,
                900: j,
              },
            },
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
