import { extendTheme } from '@chakra-ui/react';

const colors = {
  brand: {
    50: '#e6f2ff',
    100: '#b3d9ff',
    200: '#80bfff',
    300: '#4da6ff',
    400: '#1a8cff',
    500: '#0073e6',
    600: '#0066cc', // Primary Blue
    700: '#0052a3',
    800: '#003d7a',
    900: '#002952',
  },
  secondary: {
    50: '#f2f9ff',
    100: '#d9edff',
    200: '#c0e0ff',
    300: '#a6d4ff',
    400: '#8dc7ff',
    500: '#73bbff',
    600: '#5a9ecc',
    700: '#407299',
    800: '#264566',
    900: '#0d1933',
  },
  accent: {
    50: '#fff8e6',
    100: '#ffeab3',
    200: '#ffdc80',
    300: '#ffce4d',
    400: '#ffc01a',
    500: '#ffb200', // Vibrant Orange Accent
    600: '#cc8f00',
    700: '#996b00',
    800: '#664700',
    900: '#332300',
  },
  text: {
    50: '#ffffff', // Pure White
    100: '#f8f8f8',
    200: '#f0f0f0',
    300: '#e0e0e0',
    400: '#cccccc',
    500: '#b8b8b8',
    600: '#a0a0a0',
    700: '#787878',
    800: '#505050',
    900: '#1a1a1a', // Darker black for better contrast
  },
  success: {
    50: '#e6f9f0',
    100: '#b3ecd6',
    200: '#80dfbc',
    300: '#4dd2a2',
    400: '#1ac588',
    500: '#00b86f',
    600: '#008f56',
    700: '#00663d',
    800: '#003c24',
    900: '#00130b',
  },
  error: {
    50: '#fce8e8',
    100: '#f5b8b8',
    200: '#ee8888',
    300: '#e75858',
    400: '#e02828',
    500: '#c71212',
    600: '#9b0e0e',
    700: '#6f0a0a',
    800: '#430606',
    900: '#170202',
  },
  warning: {
    50: '#fdf8e6',
    100: '#f9e9b3',
    200: '#f5db80',
    300: '#f1cc4d',
    400: '#edbe1a',
    500: '#d4a500',
    600: '#a58000',
    700: '#755c00',
    800: '#463700',
    900: '#171200',
  },
  gradient: {
    blue: '#0066cc',
    purple: '#4B0082',
    red: '#B22222',
    orange: '#FF8C00',
    yellow: '#FFD700',
  },
};

const fonts = {
  heading: "'Poppins', sans-serif",
  body: "'Inter', sans-serif",
};

const components = {
  Button: {
    baseStyle: {
      fontWeight: 'semibold',
      borderRadius: 'md',
    },
    variants: {
      solid: (props) => ({
        bg: props.colorScheme === 'accent' 
          ? 'accent.500' 
          : `${props.colorScheme}.600`,
        color: props.colorScheme === 'accent' 
          ? 'text.900' 
          : 'text.50',
        _hover: {
          bg: props.colorScheme === 'accent' 
            ? 'accent.400' 
            : `${props.colorScheme}.700`,
          _disabled: {
            bg: props.colorScheme === 'accent' 
              ? 'accent.500' 
              : `${props.colorScheme}.600`,
          },
        },
        _active: {
          bg: props.colorScheme === 'accent' 
            ? 'accent.600' 
            : `${props.colorScheme}.800`,
        },
      }),
      outline: (props) => ({
        border: '2px solid',
        borderColor: props.colorScheme === 'accent' 
          ? 'accent.500' 
          : `${props.colorScheme}.600`,
        color: props.colorScheme === 'accent' 
          ? 'accent.500' 
          : `${props.colorScheme}.600`,
        _hover: {
          bg: 'rgba(255, 255, 255, 0.08)',
        },
        _active: {
          bg: 'rgba(255, 255, 255, 0.12)',
        },
      }),
      ghost: (props) => ({
        color: props.colorScheme === 'accent' 
          ? 'accent.500' 
          : `${props.colorScheme}.600`,
        _hover: {
          bg: 'rgba(255, 255, 255, 0.08)',
        },
        _active: {
          bg: 'rgba(255, 255, 255, 0.12)',
        },
      }),
    },
    defaultProps: {
      colorScheme: 'brand',
    },
  },
  Input: {
    baseStyle: {
      field: {
        color: 'text.900',
        borderColor: 'secondary.200',
        _focus: {
          borderColor: 'accent.500',
          boxShadow: '0 0 0 1px var(--chakra-colors-accent-500)',
        },
        _hover: {
          borderColor: 'accent.500',
        },
        _placeholder: {
          color: 'text.500',
        },
      },
    },
    defaultProps: {
      variant: 'outline',
      focusBorderColor: 'accent.500',
    },
  },
  Select: {
    baseStyle: {
      field: {
        color: 'text.900',
        borderColor: 'secondary.200',
        _focus: {
          borderColor: 'accent.500',
          boxShadow: '0 0 0 1px var(--chakra-colors-accent-500)',
        },
        _hover: {
          borderColor: 'accent.500',
        },
        _disabled: {
          opacity: 0.7,
          cursor: 'not-allowed',
          color: 'text.700',
        },
      },
      icon: {
        color: 'accent.500',
      },
    },
    defaultProps: {
      variant: 'outline',
      focusBorderColor: 'accent.500',
    },
  },
  Textarea: {
    baseStyle: {
      color: 'text.900',
      borderColor: 'secondary.200',
      _focus: {
        borderColor: 'accent.500',
        boxShadow: '0 0 0 1px var(--chakra-colors-accent-500)',
      },
      _hover: {
        borderColor: 'accent.500',
      },
      _placeholder: {
        color: 'text.500',
      },
    },
    defaultProps: {
      variant: 'outline',
      focusBorderColor: 'accent.500',
    },
  },
  Card: {
    baseStyle: {
      container: {
        borderRadius: 'lg',
        overflow: 'hidden',
        boxShadow: 'lg',
        bg: 'rgba(0, 0, 0, 0.3)',
        borderColor: 'rgba(255, 255, 255, 0.1)',
      },
      header: {
        padding: '4',
        bg: 'rgba(0, 0, 0, 0.2)',
        borderBottomWidth: '1px',
        borderBottomColor: 'rgba(255, 255, 255, 0.1)',
      },
      body: {
        padding: '4',
      },
      footer: {
        padding: '4',
        borderTopWidth: '1px',
        borderTopColor: 'rgba(255, 255, 255, 0.1)',
      },
    },
  },
  Heading: {
    baseStyle: {
      color: 'text.50',
    },
  },
  Text: {
    baseStyle: {
      color: 'text.50',
    },
  },
  FormLabel: {
    baseStyle: {
      color: 'text.100',
      marginBottom: '2',
    },
  },
  Badge: {
    baseStyle: {
      borderRadius: 'md',
    },
    variants: {
      solid: (props) => ({
        bg: `${props.colorScheme}.600`,
        color: 'text.50',
      }),
      outline: (props) => ({
        borderColor: `${props.colorScheme}.600`,
        color: `${props.colorScheme}.600`,
      }),
    },
  },
  Alert: {
    baseStyle: {
      container: {
        borderRadius: 'md',
      },
    },
  },
  Modal: {
    baseStyle: {
      dialog: {
        bgGradient: 'linear(to-br, rgba(30, 58, 138, 0.9), rgba(75, 0, 130, 0.9))',
        borderRadius: 'lg',
      },
      header: {
        color: 'text.50',
      },
      body: {
        color: 'text.50',
      },
      footer: {
        color: 'text.50',
      },
    },
  },
  Tabs: {
    variants: {
      line: {
        tab: {
          color: 'text.400',
          _selected: {
            color: 'accent.500',
            borderColor: 'accent.500',
          },
        },
      },
    },
  },
};

const styles = {
  global: {
    body: {
      bgGradient: 'linear(to-r, gradient.blue, gradient.purple, gradient.red, gradient.orange, gradient.yellow)',
      color: 'text.50',
    },
    a: {
      color: 'accent.500',
      _hover: {
        textDecoration: 'underline',
      },
    },
    '::-webkit-scrollbar': {
      width: '8px',
      height: '8px',
    },
    '::-webkit-scrollbar-track': {
      bg: 'rgba(0, 0, 0, 0.2)',
    },
    '::-webkit-scrollbar-thumb': {
      bg: 'rgba(255, 255, 255, 0.2)',
      borderRadius: 'full',
    },
    '::-webkit-scrollbar-thumb:hover': {
      bg: 'rgba(255, 255, 255, 0.3)',
    },
  },
};

const config = {
  initialColorMode: 'dark',
  useSystemColorMode: false,
};

const theme = extendTheme({
  colors,
  fonts,
  components,
  styles,
  config,
});

export default theme;
