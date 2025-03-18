import { extendTheme } from '@chakra-ui/react';

const colors = {
  brand: {
    50: '#ffeae8',
    100: '#ffc5c0',
    200: '#ff9f97',
    300: '#ff7a6e',
    400: '#ff5445',
    500: '#e62e1c',
    600: '#da291c', // Burger King primary red
    700: '#b32217',
    800: '#8c1a12',
    900: '#65120d',
  },
  secondary: {
    50: '#e6eeff',
    100: '#b3ccff',
    200: '#80aaff',
    300: '#4d88ff',
    400: '#1a66ff',
    500: '#0049e6',
    600: '#0033a0', // Burger King secondary blue
    700: '#002880',
    800: '#001c60',
    900: '#001040',
  },
  accent: {
    50: '#e6eeff',
    100: '#b3ccff',
    200: '#80aaff',
    300: '#4d88ff',
    400: '#1a66ff',
    500: '#104cdd', // Royal blue (replacing the yellow)
    600: '#0033a0',
    700: '#002880',
    800: '#001c60',
    900: '#001040',
  },
  gray: {
    50: '#f9f9f9',
    100: '#f0f0f0',
    200: '#e6e6e6',
    300: '#dddddd',
    400: '#d3d3d3',
    500: '#c9c9c9',
    600: '#b0b0b0',
    700: '#979797',
    800: '#7e7e7e',
    900: '#656565',
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
  darkBg: {
    50: '#f2f2f2',
    100: '#d9d9d9',
    200: '#bfbfbf',
    300: '#a6a6a6',
    400: '#8c8c8c',
    500: '#737373',
    600: '#595959',
    700: '#404040',
    800: '#262626',
    900: '#0d0d0d',
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
        bg: `${props.colorScheme}.500`,
        color: 'white',
        _hover: {
          bg: `${props.colorScheme}.600`,
          _disabled: {
            bg: `${props.colorScheme}.500`,
          },
        },
        _active: {
          bg: `${props.colorScheme}.700`,
        },
      }),
      outline: (props) => ({
        border: '2px solid',
        borderColor: `${props.colorScheme}.500`,
        color: `${props.colorScheme}.500`,
        _hover: {
          bg: `${props.colorScheme}.50`,
        },
        _active: {
          bg: `${props.colorScheme}.100`,
        },
      }),
      ghost: (props) => ({
        color: `${props.colorScheme}.500`,
        _hover: {
          bg: `${props.colorScheme}.50`,
        },
        _active: {
          bg: `${props.colorScheme}.100`,
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
        borderRadius: 'md',
      },
    },
    variants: {
      outline: {
        field: {
          borderColor: 'gray.300',
          _hover: {
            borderColor: 'gray.400',
          },
          _focus: {
            borderColor: 'brand.500',
            boxShadow: '0 0 0 1px var(--chakra-colors-brand-500)',
          },
        },
      },
    },
    defaultProps: {
      variant: 'outline',
    },
  },
  Select: {
    baseStyle: {
      field: {
        borderRadius: 'md',
      },
    },
    variants: {
      outline: {
        field: {
          borderColor: 'gray.300',
          _hover: {
            borderColor: 'gray.400',
          },
          _focus: {
            borderColor: 'brand.500',
            boxShadow: '0 0 0 1px var(--chakra-colors-brand-500)',
          },
        },
      },
    },
    defaultProps: {
      variant: 'outline',
    },
  },
  Textarea: {
    baseStyle: {
      borderRadius: 'md',
    },
    variants: {
      outline: {
        borderColor: 'gray.300',
        _hover: {
          borderColor: 'gray.400',
        },
        _focus: {
          borderColor: 'brand.500',
          boxShadow: '0 0 0 1px var(--chakra-colors-brand-500)',
        },
      },
    },
    defaultProps: {
      variant: 'outline',
    },
  },
  Card: {
    baseStyle: {
      container: {
        borderRadius: 'lg',
        overflow: 'hidden',
        boxShadow: 'md',
      },
      header: {
        padding: '4',
      },
      body: {
        padding: '4',
      },
      footer: {
        padding: '4',
      },
    },
  },
};

const styles = {
  global: {
    body: {
      bg: 'gray.100', // Lighter gray background
      color: 'gray.800',
    },
  },
};

const config = {
  initialColorMode: 'light',
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
