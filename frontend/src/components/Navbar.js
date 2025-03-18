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
      bg: isMobile ? 'accent.500' : 'secondary.600',
      color: 'white',
      transform: isMobile ? 'none' : 'translateY(-2px)',
      boxShadow: isMobile ? 'none' : '0 4px 6px rgba(0, 0, 0, 0.1)',
    }}
    color={isMobile ? "gray.800" : "gray.200"}
    fontWeight="medium"
    transition="all 0.2s"
    display="flex"
    alignItems="center"
    fontSize={isMobile ? "lg" : "md"}
    {...rest}
  >
    {icon && <Icon as={icon} mr={2} boxSize={isMobile ? "5" : "4"} />}
    {children}
  </Link>
);

const Navbar = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const bgGradient = "linear(to-r, brand.600, secondary.600)";

  return (
    <Box 
      bgGradient={bgGradient}
      px={{ base: 2, md: 4 }}
      py={{ base: 2, md: 0 }}
      borderBottom="1px" 
      borderColor="darkBg.600"
      boxShadow="0 2px 10px rgba(0, 0, 0, 0.2)"
      position="sticky"
      top="0"
      zIndex="1000"
    >
      <Container maxW="container.xl">
        <Flex h={16} alignItems="center" justifyContent="space-between">
          <IconButton
            size="md"
            icon={<HamburgerIcon />}
            aria-label="Open Menu"
            display={{ md: 'none' }}
            onClick={onOpen}
            variant="ghost"
            color="gray.400"
            _hover={{
              bg: "secondary.600",
              color: "white",
            }}
          />
          <HStack spacing={{ base: 2, md: 8 }} alignItems="center">
            <Box>
              <Link
                as={RouterLink}
                to="/"
                fontSize={{ base: "lg", md: "xl" }}
                fontWeight="bold"
                color="white"
                _hover={{ 
                  textDecoration: 'none',
                  transform: 'scale(1.05)',
                }}
                transition="all 0.2s"
              >
                <HStack spacing={2}>
                  <Box 
                    bg="accent.500" 
                    p={1.5} 
                    borderRadius="md" 
                    display="flex" 
                    alignItems="center"
                    justifyContent="center"
                    boxShadow="0 2px 5px rgba(0, 0, 0, 0.2)"
                  >
                    <FaWrench color="white" size="1.2em" />
                  </Box>
                  <Text 
                    color="white" 
                    fontWeight="bold" 
                    fontSize={{ base: "xl", md: "2xl" }}
                  >
                    Garagefy
                  </Text>
                </HStack>
              </Link>
            </Box>
            <HStack as="nav" spacing={4} display={{ base: 'none', md: 'flex' }}>
              <NavLink to="/diagnosis" icon={FaTools}>Car Diagnosis</NavLink>
              <NavLink to="/garages" icon={FaMapMarkerAlt}>Find Garages</NavLink>
              <NavLink to="/used-car-check" icon={FaCheckCircle}>Used Car Check</NavLink>
            </HStack>
          </HStack>
        </Flex>
      </Container>

      {/* Mobile Navigation Drawer */}
      <Drawer isOpen={isOpen} placement="left" onClose={onClose} size="xs">
        <DrawerOverlay />
        <DrawerContent bg="gray.100">
          <DrawerCloseButton color="gray.800" />
          <DrawerHeader 
            bgGradient="linear(to-r, brand.600, secondary.600)" 
            color="white" 
            px={4} 
            py={6}
          >
            <HStack spacing={2}>
              <Box 
                bg="accent.500" 
                p={1.5} 
                borderRadius="md" 
                display="flex" 
                alignItems="center" 
                justifyContent="center"
              >
                <FaWrench color="white" size="1.2em" />
              </Box>
              <Text 
                color="white" 
                fontWeight="bold" 
                fontSize="xl"
              >
                Garagefy
              </Text>
            </HStack>
          </DrawerHeader>
          <DrawerBody p={0}>
            <VStack align="stretch" spacing={0} p={0} mt={0}>
              <NavLink 
                to="/" 
                icon={FaWrench} 
                isMobile
              >
                Home
              </NavLink>
              <NavLink 
                to="/diagnosis" 
                icon={FaTools} 
                isMobile
              >
                Car Diagnosis
              </NavLink>
              <NavLink 
                to="/garages" 
                icon={FaMapMarkerAlt} 
                isMobile
              >
                Find Garages
              </NavLink>
              <NavLink 
                to="/used-car-check" 
                icon={FaCheckCircle} 
                isMobile
              >
                Used Car Check
              </NavLink>
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </Box>
  );
};

export default Navbar;
