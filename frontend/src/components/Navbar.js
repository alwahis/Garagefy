import React from 'react';
import {
  Box,
  Flex,
  HStack,
  Link,
  Container,
  Icon,
  Button,
  Image,
  Menu,
  MenuButton,
  MenuList,
  MenuItem
} from '@chakra-ui/react';
import { FaCarCrash, FaGlobe, FaChevronDown } from 'react-icons/fa';
import { Link as RouterLink } from 'react-router-dom';
import { useLanguage } from '../i18n/LanguageContext';

const Navbar = () => {
  const { language, changeLanguage, t } = useLanguage();

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
    { code: 'lb', name: 'Lëtzebuergesch', flag: '🇱🇺' }
  ];

  const currentLang = languages.find(lang => lang.code === language);

  return (
    <Box as="nav" bg="#FFD700" color="#1A202C" boxShadow="0 2px 10px rgba(0,0,0,0.1)" position="sticky" top="0" zIndex="999">
      <Container maxW="container.xl" py={3}>
        <Flex h={12} alignItems="center" justifyContent="space-between">
          {/* Logo */}
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

          {/* Desktop Navigation */}
          <HStack spacing={4}>
            {/* Get Quotes Button - Desktop */}
            <Button
              as={RouterLink}
              to="/fix-it"
              leftIcon={<Icon as={FaCarCrash} />}
              bg="#0078D4"
              color="white"
              size="md"
              fontWeight="bold"
              display={{ base: 'none', md: 'flex' }}
              _hover={{ 
                bg: "#1565C0",
                transform: "translateY(-2px)",
                boxShadow: "0 4px 8px rgba(30,136,229,0.3)"
              }}
              transition="all 0.2s"
            >
              {t('navGetQuotes')}
            </Button>

            {/* Language Selector */}
            <Menu>
              <MenuButton
                as={Button}
                rightIcon={<FaChevronDown />}
                leftIcon={<FaGlobe />}
                bg="white"
                color="#1A202C"
                size="md"
                fontWeight="bold"
                _hover={{ bg: "gray.100" }}
                _active={{ bg: "gray.200" }}
                minW={{ base: "auto", md: "140px" }}
                px={{ base: 3, md: 4 }}
              >
                <HStack spacing={2} display={{ base: 'none', sm: 'flex' }}>
                  <Box as="span">{currentLang.flag}</Box>
                  <Box as="span" display={{ base: 'none', md: 'inline' }}>{currentLang.name}</Box>
                </HStack>
                <Box display={{ base: 'inline', sm: 'none' }}>{currentLang.flag}</Box>
              </MenuButton>
              <MenuList bg="white" borderColor="gray.200" zIndex={1000}>
                {languages.map((lang) => (
                  <MenuItem
                    key={lang.code}
                    onClick={() => changeLanguage(lang.code)}
                    bg={language === lang.code ? "#0078D4" : "white"}
                    color={language === lang.code ? "white" : "#1A202C"}
                    _hover={{ 
                      bg: language === lang.code ? "#1565C0" : "gray.100" 
                    }}
                    fontWeight={language === lang.code ? "bold" : "normal"}
                  >
                    <HStack spacing={3}>
                      <Box fontSize="xl">{lang.flag}</Box>
                      <Box>{lang.name}</Box>
                    </HStack>
                  </MenuItem>
                ))}
              </MenuList>
            </Menu>
          </HStack>
        </Flex>

        {/* Mobile Get Quotes Button - Below navbar */}
        <Box display={{ base: 'block', md: 'none' }} mt={3}>
          <Button
            as={RouterLink}
            to="/fix-it"
            leftIcon={<Icon as={FaCarCrash} />}
            bg="#0078D4"
            color="white"
            size="md"
            fontWeight="bold"
            w="100%"
            _hover={{ 
              bg: "#1565C0",
            }}
          >
            {t('navGetQuotes')}
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default Navbar;
