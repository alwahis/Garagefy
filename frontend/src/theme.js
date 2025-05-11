import { extendTheme } from '@chakra-ui/react';

const colors = {
  brand: {
    50: '#e6f2ff',
    100: '#b3d9ff',
    200: '#80bfff',
    300: '#4da6ff',
    400: '#1a8cff',
    500: '#0073e6',
    600: '#0052a3', // Primary Blue - Darkened for better contrast
    700: '#003d7a',
    800: '#002952',
    900: '#001a33',
  },
  secondary: {
    50: '#f2f9ff',
    100: '#d9edff',
    200: '#c0e0ff',
    300: '#a6d4ff',
    400: '#8dc7ff',
    500: '#73bbff',
    600: '#407299', // Darkened for better contrast
    700: '#264566',
    800: '#0d1933',
    900: '#060d1a',
  },
  accent: {
    50: '#fff8e6',
    100: '#ffeab3',
    200: '#ffdc80',
    300: '#ffce4d',
    400: '#ffc01a',
    500: '#cc8f00', // Darkened for better contrast
    600: '#996b00',
    700: '#664700',
    800: '#332300',
    900: '#1a1200',
  },
  text: {
    50: '#ffffff', // Pure White
    100: '#f8f8f8',
    200: '#f0f0f0',
    300: '#e0e0e0',
    400: '#cccccc',
    500: '#a0a0a0', // Darkened for better contrast
    600: '#787878',
    700: '#505050',
    800: '#2d2d2d',
    900: '#1A202C',
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
      fontWeight: 'bold',
      borderRadius: 'md',
      boxShadow: 'md',
    },
    variants: {
      solid: (props) => ({
        bg: props.colorScheme === 'accent' 
          ? 'accent.600' 
          : `${props.colorScheme}.700`,
        color: 'white',
        _hover: {
          bg: props.colorScheme === 'accent' 
            ? 'accent.700' 
            : `${props.colorScheme}.800`,
          transform: 'translateY(-2px)',
          boxShadow: 'lg',
          _disabled: {
            bg: props.colorScheme === 'accent' 
              ? 'accent.600' 
              : `${props.colorScheme}.700`,
            transform: 'none',
            boxShadow: 'none',
          },
        },
        _active: {
          bg: props.colorScheme === 'accent' 
            ? 'accent.800' 
            : `${props.colorScheme}.900`,
          transform: 'translateY(0)',
        },
      }),
      outline: (props) => ({
        border: '2px solid',
        borderColor: props.colorScheme === 'accent' 
          ? 'accent.600' 
          : `${props.colorScheme}.700`,
        color: props.colorScheme === 'accent' 
          ? 'accent.700' 
          : `${props.colorScheme}.700`,
        fontWeight: 'bold',
        _hover: {
          bg: props.colorScheme === 'accent' 
            ? 'accent.50' 
            : `${props.colorScheme}.50`,
          borderColor: props.colorScheme === 'accent' 
            ? 'accent.700' 
            : `${props.colorScheme}.800`,
          transform: 'translateY(-2px)',
          boxShadow: 'md',
        },
        _active: {
          bg: props.colorScheme === 'accent' 
            ? 'accent.100' 
            : `${props.colorScheme}.100`,
          transform: 'translateY(0)',
        },
      }),
      ghost: (props) => ({
        color: props.colorScheme === 'accent' 
          ? 'accent.700' 
          : `${props.colorScheme}.700`,
        fontWeight: 'bold',
        _hover: {
          bg: props.colorScheme === 'accent' 
            ? 'accent.50' 
            : `${props.colorScheme}.50`,
          transform: 'translateY(-2px)',
        },
        _active: {
          bg: props.colorScheme === 'accent' 
            ? 'accent.100' 
            : `${props.colorScheme}.100`,
          transform: 'translateY(0)',
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
        backgroundColor: 'white',
        borderColor: 'gray.300',
        borderWidth: '2px',
        _focus: {
          borderColor: 'brand.600',
          boxShadow: '0 0 0 1px var(--chakra-colors-brand-600)',
        },
        _hover: {
          borderColor: 'brand.500',
        },
        _placeholder: {
          color: 'text.600',
          opacity: 0.8,
        },
        _disabled: {
          opacity: 0.7,
          cursor: 'not-allowed',
          color: 'text.700',
          backgroundColor: 'gray.50',
          borderColor: 'gray.200',
        },
      },
    },
    defaultProps: {
      variant: 'outline',
      focusBorderColor: 'brand.600',
    },
  },
  Select: {
    baseStyle: {
      field: {
        color: 'text.900',
        backgroundColor: 'white',
        borderColor: 'gray.300',
        borderWidth: '2px',
        _focus: {
          borderColor: 'brand.600',
          boxShadow: '0 0 0 1px var(--chakra-colors-brand-600)',
        },
        _hover: {
          borderColor: 'brand.500',
        },
        _disabled: {
          opacity: 0.7,
          cursor: 'not-allowed',
          color: 'text.700',
          backgroundColor: 'gray.50',
          borderColor: 'gray.200',
        },
        option: {
          color: 'text.900',
          backgroundColor: 'white',
          fontWeight: 'normal',
        },
      },
      icon: {
        color: 'brand.600',
        fontSize: '1.25em',
      },
    },
    defaultProps: {
      variant: 'outline',
      focusBorderColor: 'brand.600',
    },
  },
  Textarea: {
    baseStyle: {
      color: 'text.900',
      backgroundColor: 'white',
      borderColor: 'gray.300',
      borderWidth: '2px',
      _focus: {
        borderColor: 'brand.600',
        boxShadow: '0 0 0 1px var(--chakra-colors-brand-600)',
      },
      _hover: {
        borderColor: 'brand.500',
      },
      _placeholder: {
        color: 'text.600',
        opacity: 0.8,
      },
      _disabled: {
        opacity: 0.7,
        cursor: 'not-allowed',
        color: 'text.700',
        backgroundColor: 'gray.50',
        borderColor: 'gray.200',
      },
    },
    defaultProps: {
      variant: 'outline',
      focusBorderColor: 'brand.600',
    },
  },
  Card: {
    baseStyle: {
      container: {
        borderRadius: 'lg',
        overflow: 'hidden',
        boxShadow: 'lg',
        bg: 'white',
        borderColor: 'gray.300',
        borderWidth: '1px',
      },
      header: {
        padding: '5',
        bg: 'gray.50',
        borderBottomWidth: '2px',
        borderBottomColor: 'gray.200',
      },
      body: {
        padding: '5',
      },
      footer: {
        padding: '5',
        borderTopWidth: '2px',
        borderTopColor: 'gray.200',
        bg: 'gray.50',
      },
    },
  },
  Heading: {
    baseStyle: {
      color: 'text.900',
      fontWeight: 'bold',
    },
    sizes: {
      xl: {
        fontSize: ['3xl', '4xl'],
        lineHeight: 1.2,
      },
      lg: {
        fontSize: ['2xl', '3xl'],
        lineHeight: 1.2,
      },
      md: {
        fontSize: ['xl', '2xl'],
        lineHeight: 1.3,
      },
      sm: {
        fontSize: ['lg', 'xl'],
        lineHeight: 1.4,
      },
    },
  },
  Text: {
    baseStyle: {
      color: 'text.700',
    },
    variants: {
      primary: {
        color: 'text.900',
        fontWeight: 'medium',
      },
      secondary: {
        color: 'text.700',
      },
      muted: {
        color: 'text.600',
        fontSize: 'sm',
      },
    },
  },
  FormLabel: {
    baseStyle: {
      color: 'text.900',
      marginBottom: '2',
      fontWeight: 'medium',
    },
  },
  Badge: {
    baseStyle: {
      borderRadius: 'md',
      fontWeight: 'medium',
      px: 2,
      py: 1,
    },
    variants: {
      solid: (props) => ({
        bg: `${props.colorScheme}.600`,
        color: 'white',
      }),
      outline: (props) => ({
        borderColor: `${props.colorScheme}.600`,
        color: `${props.colorScheme}.700`,
        borderWidth: '2px',
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
