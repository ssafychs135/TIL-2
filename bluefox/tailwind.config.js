/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    // 1. Screens (Spacing System.md)
    screens: {
      'tablet': '768px',
      'desktop': '1440px',
    },
    extend: {
      // 2. Color System (Color Variables.md + Component Specs.md)
      colors: {
        blue: {
          400: '#3B82F6',
          500: '#2563EB',
          600: '#1D4ED8',
          700: '#1E40AF',
        },
        success: {
          DEFAULT: '#00C853',
          light: '#00E676',
        },
        warning: '#FFB020',
        danger: '#EF4444',
        info: '#00AFF4',
        bg: {
          primary: '#0F1014',
          secondary: '#1A1C23',
          tertiary: '#24262E',
          elevated: '#2D3039',
          tooltip: '#000000',
          backdrop: 'rgba(0, 0, 0, 0.75)',
        },
        state: {
          'input': 'rgba(255, 255, 255, 0.03)',
          'table-header': 'rgba(255, 255, 255, 0.02)',
          'table-hover': 'rgba(37, 99, 235, 0.06)',
          'table-selected': 'rgba(37, 99, 235, 0.12)',
          'ghost-hover': 'rgba(37, 99, 235, 0.08)',
          'ghost-active': 'rgba(37, 99, 235, 0.12)',
          'tab-hover': 'rgba(255, 255, 255, 0.04)',
        },
        text: {
          primary: '#FAFAFA',
          secondary: '#A0A4B8',
          tertiary: '#6B7280',
          accent: '#2563EB',
        },
        border: {
          subtle: 'rgba(255, 255, 255, 0.04)',
          DEFAULT: 'rgba(255, 255, 255, 0.08)',
          strong: 'rgba(255, 255, 255, 0.12)',
        },
        'focus-ring': 'rgba(37, 99, 235, 0.4)',
        code: {
          bg: '#161B22',
          text: '#C9D1D9',
          border: 'rgba(255, 255, 255, 0.06)',
          inline: 'rgba(255, 255, 255, 0.08)',
        }
      },

      // 3. Typography (Typography.md)
      fontFamily: {
        sans: ['Geist', 'Inter', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"Fira Code"', '"SF Mono"', 'Consolas', 'monospace'],
      },
      fontSize: {
        'display': ['40px', { lineHeight: '48px', fontWeight: '700', letterSpacing: '-0.5px' }],
        'h1': ['32px', { lineHeight: '40px', fontWeight: '700' }],
        'h2': ['24px', { lineHeight: '32px', fontWeight: '700' }],
        'h3': ['20px', { lineHeight: '28px', fontWeight: '600' }],
        'h4': ['18px', { lineHeight: '24px', fontWeight: '600' }],
        'body-lg': ['16px', { lineHeight: '24px', fontWeight: '400' }],
        'body': ['14px', { lineHeight: '20px', fontWeight: '400' }],
        'body-sm': ['13px', { lineHeight: '18px', fontWeight: '400' }],
        'caption': ['12px', { lineHeight: '16px', fontWeight: '500', letterSpacing: '0.2px' }],
        'code': ['14px', { lineHeight: '20px', fontWeight: '400' }],
      },
      letterSpacing: {
        'caps': '0.5px',
        'caps-wider': '1px',
      },

      // 4. Spacing (Spacing System.md + Alignment & Layout)
      spacing: {
        '1': '4px',
        '2': '8px',
        '2.5': '10px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '5.5': '22px', // [추가] Alignment & Layout - Main to Subtext Gap
        '6': '24px',
        '8': '32px',
        '9': '36px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
        '18': '72px',
        '20': '80px',
        '24': '96px',
      },
      
      // 5. Dimensions (Component Specs + Alignment & Layout)
      height: {
        'badge': '26px',
        'tab': '44px',
      },
      width: {
        'switch': '44px',
        'repo-icon': '36px',
        'field-sm': '276px', // [추가] Alignment & Layout - Field 1/2 Width
        'field-lg': '576px', // [추가] Alignment & Layout - Total Field Width
        'row-checkbox': '584px', // [추가] Alignment & Layout - Checkbox Row Width
      },
      
      // 6. Layout & Constraints
      container: {
        center: true,
        padding: {
          DEFAULT: '20px',
          tablet: '40px',
          desktop: '80px',
        },
        screens: {
          desktop: '1280px',
        },
      },
      maxWidth: {
        'reading': '720px',
        'narrow': '560px',
        'modal-md': '640px',
        'modal-lg': '800px',
        'toast-min': '320px',
        'toast-max': '480px',
        'tooltip': '240px',
      },
      maxHeight: {
        'modal': '60vh',
        'dropdown': '320px',
      },
      minWidth: {
        'toast': '320px',
      },

      // 7. Component Specs (Borders, Shadows, Blurs)
      borderRadius: {
        'sm': '4px',
        DEFAULT: '6px',
        'md': '8px',
        'lg': '12px',
        'pill': '9999px',
      },
      boxShadow: {
        'modal': '0 8px 32px rgba(0, 0, 0, 0.6)',
        'dropdown': '0 4px 16px rgba(0, 0, 0, 0.5)',
        'tooltip': '0 2px 8px rgba(0, 0, 0, 0.4)',
        'focus': '0 0 0 3px rgba(37, 99, 235, 0.2)',
        'error': '0 0 0 3px rgba(239, 68, 68, 0.2)',
      },
      backdropBlur: {
        'sm': '4px',
      },
      opacity: {
        'disabled': '0.5',
      },
      transitionDuration: {
        DEFAULT: '200ms',
        '300': '300ms',
      },
      transitionTimingFunction: {
        DEFAULT: 'ease',
      },
    },
  },
  plugins: [],
}
