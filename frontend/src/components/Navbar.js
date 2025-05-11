import React from 'react';
import {
  Box,
  Flex,
  HStack,
  Link,
  IconButton,
  useDisclosure,
  Container,
  Icon,
  Text,
  VStack,
  Drawer,
  DrawerBody,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
} from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';
import { FaMapMarkerAlt, FaTools, FaCheckCircle, FaWrench } from 'react-icons/fa';
import { Link as RouterLink } from 'react-router-dom';

const NavLink = ({ children, to, icon, isMobile = false, ...rest }) => (
  <Link
    as={RouterLink}
    to={to}
    px={4}
    py={isMobile ? 4 : 2}
    rounded="md"
    width={isMobile ? "full" : "auto"}
    _hover={{
      textDecoration: 'none',
      bg: isMobile ? 'accent.500' : 'rgba(255, 255, 255, 0.15)',
      color: isMobile ? 'black' : 'black',
      transform: isMobile ? 'none' : 'translateY(-2px)',
      boxShadow: isMobile ? 'none' : '0 4px 6px rgba(0, 0, 0, 0.3)',
    }}
    color={isMobile ? "black" : "black"}
    fontWeight="medium"
    transition="all 0.2s"
    display="flex"
    alignItems="center"
    fontSize={isMobile ? "lg" : "md"}
    {...rest}
  >
    {icon && <Icon as={icon} mr={2} boxSize={isMobile ? "5" : "4"} color={isMobile ? "black" : "black"} />}
    {children}
  </Link>
);

const Navbar = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Box as="nav" bg="brand.600" color="black" boxShadow="md" position="sticky" top="0" zIndex="999">
      <Container maxW="container.xl" py={2}>
        <Flex h={16} alignItems="center" justifyContent="space-between">
          <HStack spacing={8} alignItems="center">
            <Box fontWeight="bold" fontSize="xl" color="black">
              <Link as={RouterLink} to="/" _hover={{ textDecoration: 'none', color: 'black' }}>
                <Flex align="center">
                  <Icon as={FaWrench} mr={2} color="black" />
                  <Text color="black">Garagefy</Text>
                </Flex>
              </Link>
            </Box>
            <HStack as="nav" spacing={4} display={{ base: 'none', md: 'flex' }}>
              <NavLink to="/find-garage" icon={FaMapMarkerAlt} color="black">Find Garage</NavLink>
              <NavLink to="/diagnose-car" icon={FaTools} color="black">Diagnose Car</NavLink>
              <NavLink to="/used-car-check" icon={FaCheckCircle} color="black">Used Car Check</NavLink>
            </HStack>
          </HStack>
          <IconButton
            size="md"
            icon={<HamburgerIcon />}
            aria-label="Open Menu"
            display={{ md: 'none' }}
            onClick={onOpen}
            bg="transparent"
            color="black"
            _hover={{ bg: 'rgba(255, 255, 255, 0.15)' }}
          />
        </Flex>
      </Container>

      <Drawer isOpen={isOpen} placement="right" onClose={onClose} size="full">
        <DrawerOverlay />
        <DrawerContent bg="brand.600">
          <DrawerCloseButton color="black" />
          <DrawerHeader color="black">Menu</DrawerHeader>
          <DrawerBody>
            <VStack spacing={4} align="stretch">
              <NavLink to="/find-garage" icon={FaMapMarkerAlt} isMobile color="black">Find Garage</NavLink>
              <NavLink to="/diagnose-car" icon={FaTools} isMobile color="black">Diagnose Car</NavLink>
              <NavLink to="/used-car-check" icon={FaCheckCircle} isMobile color="black">Used Car Check</NavLink>
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </Box>
  );
};

export default Navbar;
