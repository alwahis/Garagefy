import React from 'react';
import { Box, Flex, Heading, Link, HStack, Icon, useColorModeValue } from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { FaWrench, FaCarCrash, FaHome } from 'react-icons/fa';

const NavLink = ({ to, icon, children, isActive }) => {
  const activeBg = useColorModeValue('white', 'gray.800');
  const inactiveBg = 'transparent';
  const activeColor = 'teal.500';
  const inactiveColor = useColorModeValue('gray.100', 'gray.400');

  return (
    <Link
      as={RouterLink}
      to={to}
      px={4}
      py={2}
      rounded="md"
      bg={isActive ? activeBg : inactiveBg}
      color={isActive ? activeColor : inactiveColor}
      display="flex"
      alignItems="center"
      _hover={{
        textDecoration: 'none',
        bg: isActive ? activeBg : 'whiteAlpha.200',
        transform: 'translateY(-2px)',
      }}
      transition="all 0.2s"
    >
      <Icon as={icon} mr={2} />
      {children}
    </Link>
  );
};

const Header = () => {
  const location = useLocation();
  const bgColor = useColorModeValue('teal.600', 'gray.900');
  const borderColor = useColorModeValue('teal.500', 'gray.700');

  return (
    <Box 
      bg={bgColor} 
      px={4} 
      position="sticky" 
      top={0} 
      zIndex={1000}
      borderBottom="3px solid"
      borderColor={borderColor}
      boxShadow="lg"
    >
      <Flex 
        maxW="container.xl" 
        mx="auto" 
        h={16} 
        align="center" 
        justify="space-between"
      >
        <Link 
          as={RouterLink} 
          to="/" 
          _hover={{ textDecoration: 'none' }}
        >
          <Heading 
            size="lg" 
            color="white" 
            fontWeight="extrabold"
            letterSpacing="tight"
            display="flex"
            alignItems="center"
            _hover={{ transform: 'scale(1.05)' }}
            transition="all 0.2s"
          >
            <Icon as={FaWrench} mr={2} transform="rotate(-45deg)" />
            Garagefy
          </Heading>
        </Link>

        <HStack spacing={4} display={{ base: 'none', md: 'flex' }}>
          <NavLink 
            to="/" 
            icon={FaHome}
            isActive={location.pathname === '/'}
          >
            Home
          </NavLink>
          <NavLink 
            to="/find-garage" 
            icon={FaWrench}
            isActive={location.pathname === '/find-garage'}
          >
            Find Garage
          </NavLink>
          <NavLink 
            to="/diagnose-car" 
            icon={FaCarCrash}
            isActive={location.pathname === '/diagnose-car'}
          >
            Diagnose Car
          </NavLink>
        </HStack>
      </Flex>
    </Box>
  );
};

export default Header;
