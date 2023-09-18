import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      animation: {
        'spin-slow': 'spin 3s linear infinite',
        // 'bounce': 'bounce 3s linear infinite',
      },
      keyframes: {
      bounce: {
          '0%, 100%': {
            'transform': 'translateY(-50%)',
            'animation-timing-function': 'cubic-bezier(0.8, 0, 1, 1)'
          },
          '50%': {
            'transform': 'translateY(0)',
            'animation-timing-function': 'cubic-bezier(0, 0, 0.2, 1)'
          }
        }
      }
    },
  },
  daisyui: {
    themes: ['light', 'dark', 'cupcake', 'dracula'],
  },
  plugins: [require('daisyui')],
};
export default config;
