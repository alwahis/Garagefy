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
  Button,
  Image
} from '@chakra-ui/react';
import { HamburgerIcon, CloseIcon } from '@chakra-ui/icons';
import { FaCarCrash } from 'react-icons/fa';
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
      bg: isMobile ? '#0078D4' : 'rgba(30, 136, 229, 0.1)',
      color: isMobile ? 'white' : '#0078D4',
      transform: isMobile ? 'none' : 'translateY(-2px)',
    }}
    color={isMobile ? "#1A202C" : "#1A202C"}
    fontWeight="bold"
    transition="all 0.2s"
    display="flex"
    alignItems="center"
    fontSize={isMobile ? "xl" : "md"}
    {...rest}
  >
    {icon && <Icon as={icon} mr={2} boxSize={isMobile ? "6" : "5"} />}
    {children}
  </Link>
);

const Navbar = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Box as="nav" bg="#FFD700" color="#1A202C" boxShadow="0 2px 10px rgba(0,0,0,0.1)" position="sticky" top="0" zIndex="999">
      <Container maxW="container.xl" py={3}>
        <Flex h={12} alignItems="center" justifyContent="space-between">
          <HStack spacing={8} alignItems="center">
            <Box>
              <Link as={RouterLink} to="/" _hover={{ opacity: 0.8 }} display="flex" alignItems="center">
                <Image 
                  src="/garagefy-logo.svg"
                  alt="Garagefy"
                  h={{ base: "30px", md: "40px" }}
                  w="auto"
                />
              </Link>
            </Box>
            <HStack as="nav" spacing={2} display={{ base: 'none', md: 'flex' }}>
              <Button
                as={RouterLink}
                to="/fix-it"
                leftIcon={<Icon as={FaCarCrash} />}
                bg="#0078D4"
                color="white"
                size="md"
                fontWeight="bold"
                _hover={{ 
                  bg: "#1565C0",
                  transform: "translateY(-2px)",
                  boxShadow: "0 4px 8px rgba(30,136,229,0.3)"
                }}
                transition="all 0.2s"
              >
                Get Free Quotes
              </Button>
            </HStack>
          </HStack>
          <IconButton
            size="md"
            icon={<HamburgerIcon />}
            aria-label="Open Menu"
            display={{ md: 'none' }}
            onClick={onOpen}
            bg="#0078D4"
            color="white"
            _hover={{ bg: '#1565C0' }}
          />
        </Flex>
      </Container>

      <Drawer isOpen={isOpen} placement="right" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent bg="#FFD700">
          <DrawerCloseButton color="#1A202C" size="lg" />
          <DrawerHeader display="flex" justifyContent="center" py={4}>
            <Image 
              src="/garagefy-logo.svg"
              alt="Garagefy"
              h="35px"
              w="auto"
            />
          </DrawerHeader>
          <DrawerBody>
            <VStack spacing={4} align="stretch" mt={8}>
              <Button
                as={RouterLink}
                to="/"
                size="lg"
                bg="white"
                color="#1A202C"
                fontWeight="bold"
                _hover={{ bg: "gray.100" }}
                onClick={onClose}
              >
                Home
              </Button>
              <Button
                as={RouterLink}
                to="/fix-it"
                leftIcon={<Icon as={FaCarCrash} />}
                size="lg"
                bg="#0078D4"
                color="white"
                fontWeight="bold"
                _hover={{ bg: "#1565C0" }}
                onClick={onClose}
              >
                Get Free Quotes
              </Button>
            </VStack>
          </DrawerBody>
        </DrawerContent>
      </Drawer>
    </Box>
  );
};

export default Navbar;
