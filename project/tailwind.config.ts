import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: ['class'],
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        chart: {
          '1': 'hsl(var(--chart-1))',
          '2': 'hsl(var(--chart-2))',
          '3': 'hsl(var(--chart-3))',
          '4': 'hsl(var(--chart-4))',
          '5': 'hsl(var(--chart-5))',
        },
        purple: {
          100: '#f5f3ff',
          200: '#e0d7ff',
          300: '#d0b1ff',
          400: '#a66dff',
          500: '#7a3eff',
          600: '#5e1ce6',
          700: '#3b0db5',
          800: '#280b84',
          900: '#190c5a',
        },
        blue: {
          100: '#ccf2ff',
          200: '#99e0ff',
          300: '#66c2ff',
          400: '#33a3ff',
          500: '#009eff',
          600: '#007fdd',
          700: '#0061b2',
          800: '#004785',
          900: '#003366',
        },
        red: {
          100: '#ffe6e6',
          200: '#ffcccc',
          300: '#ff9999',
          400: '#ff6666',
          500: '#ff3333',
          600: '#e60000',
          700: '#b20000',
          800: '#800000',
          900: '#4d0000',
        },
        green: {
          100: '#e6ffe6',
          200: '#ccffcc',
          300: '#99ff99',
          400: '#66ff66',
          500: '#33ff33',
          600: '#00e600',
          700: '#00b200',
          800: '#008000',
          900: '#004d00',
        },
        yellow: {
          100: '#fff9e6',
          200: '#ffec99',
          300: '#ffdf66',
          400: '#ffd033',
          500: '#ffcc00',
          600: '#e6b800',
          700: '#b38f00',
          800: '#806600',
          900: '#4d3d00',
        },
      },
      keyframes: {
        'accordion-down': {
          from: {
            height: '0',
          },
          to: {
            height: 'var(--radix-accordion-content-height)',
          },
        },
        'accordion-up': {
          from: {
            height: 'var(--radix-accordion-content-height)',
          },
          to: {
            height: '0',
          },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};

export default config;
