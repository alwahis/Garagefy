import React from 'react';
import { 
  Box, 
  Container, 
  Heading, 
  VStack, 
  Text, 
  Button,
  useBreakpointValue, 
  Icon,
  Badge,
  Image,
  SimpleGrid,
  HStack,
  Flex
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { FaCar, FaCamera, FaEnvelope, FaCheckCircle, FaArrowRight } from 'react-icons/fa';
import { MdDirectionsCar } from 'react-icons/md';
import { useLanguage } from '../i18n/LanguageContext';

const Home = () => {
  const navigate = useNavigate();
  const isMobile = useBreakpointValue({ base: true, md: false });
  const { t } = useLanguage();

  return (
    <Box 
      bg="#FFD700" 
      minH="100vh"
      position="relative"
      overflow="hidden"
    >
      {/* Decorative car damage icons - desktop only */}
      <Box
        position="absolute"
        top="10%"
        left="5%"
        fontSize="8xl"
        opacity="0.05"
        display={{ base: "none", lg: "block" }}
      >
        🚗💥
      </Box>
      <Box
        position="absolute"
        bottom="15%"
        right="5%"
        fontSize="8xl"
        opacity="0.05"
        display={{ base: "none", lg: "block" }}
      >
        🔧🚙
      </Box>

      <Container maxW="container.xl" py={{ base: 6, md: 12 }} position="relative" zIndex={1}>
        <VStack spacing={{ base: 8, md: 12 }} align="center">
          
          {/* Hero Section - Mobile Optimized */}
          <VStack spacing={4} textAlign="center" w="100%" pt={{ base: 4, md: 8 }}>
            {/* Logo */}
            <Image 
              src="/garagefy-logo.svg"
              alt="Garagefy"
              maxW={{ base: "180px", md: "280px" }}
              w="100%"
              h="auto"
              mx="auto"
              mb={2}
            />

            {/* Main Headline - Larger on mobile */}
            <Heading 
              as="h1" 
              fontSize={{ base: "4xl", md: "5xl", lg: "6xl" }}
              fontWeight="black"
              lineHeight="1.1"
              color="#1A202C"
              px={4}
            >
              {t('homeTitle')}
              <Text as="span" color="#0078D4" display="block" mt={2}>
                {t('homeSubtitle')}
              </Text>
            </Heading>

            {/* Subheadline */}
            <Text 
              fontSize={{ base: "xl", md: "2xl" }} 
              color="#1A202C" 
              fontWeight="semibold"
              px={4}
            >
              {t('homeDamageTypes')}
            </Text>

            {/* Save Badge */}
            <Badge 
              fontSize={{ base: "xl", md: "2xl" }}
              px={{ base: 6, md: 8 }}
              py={{ base: 3, md: 4 }}
              borderRadius="full"
              bg="#0078D4"
              color="white"
              textTransform="uppercase"
              fontWeight="black"
              boxShadow="0 8px 20px rgba(0,120,212,0.4)"
            >
              {t('homeSaveBadge')}
            </Badge>
          </VStack>

          {/* MEGA CTA Button - Impossible to Miss */}
          <Box
            w="100%"
            maxW="600px"
            px={4}
          >
            <Button
              size="lg"
              w="100%"
              h={{ base: "75px", md: "100px" }}
              fontSize={{ base: "lg", sm: "xl", md: "3xl" }}
              fontWeight="black"
              bg="#0078D4"
              color="white"
              borderRadius="2xl"
              boxShadow="0 15px 40px rgba(0,120,212,0.5)"
              px={{ base: 4, md: 8 }}
              whiteSpace="normal"
              textAlign="center"
              lineHeight="1.2"
              _hover={{
                transform: "translateY(-4px)",
                boxShadow: "0 20px 50px rgba(0,120,212,0.6)",
                bg: "#0066B8"
              }}
              _active={{
                transform: "translateY(-2px)"
              }}
              transition="all 0.3s"
              onClick={() => navigate('/fix-it')}
              rightIcon={<Icon as={FaArrowRight} boxSize={{ base: 5, md: 8 }} />}
              leftIcon={<Icon as={FaCar} boxSize={{ base: 5, md: 8 }} />}
            >
              {t('homeCtaButton')}
            </Button>
            
            <Text 
              textAlign="center" 
              fontSize={{ base: "sm", md: "md" }}
              color="#1A202C"
              mt={3}
              fontWeight="semibold"
            >
              ✓ {t('homeTrustFree')} • ✓ {t('homeTrustFast')} • ✓ {t('homeTrustNoObligation')}
            </Text>
          </Box>

          {/* How It Works - Mobile Friendly */}
          <Box
            w="100%"
            maxW="900px"
            bg="white"
            p={{ base: 6, md: 10 }}
            borderRadius="2xl"
            boxShadow="0 10px 30px rgba(0,0,0,0.1)"
            border="3px solid #0078D4"
          >
            <Heading
              fontSize={{ base: "2xl", md: "3xl" }}
              color="#1A202C"
              textAlign="center"
              mb={6}
              fontWeight="black"
            >
              {t('homeHowItWorks')}
            </Heading>

            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={{ base: 6, md: 8 }}>
              {/* Step 1 */}
              <VStack spacing={3}>
                <Box
                  bg="#FFD700"
                  borderRadius="full"
                  p={4}
                  boxShadow="0 4px 15px rgba(255,215,0,0.3)"
                >
                  <Icon as={FaCamera} boxSize={{ base: 8, md: 10 }} color="#0078D4" />
                </Box>
                <Badge
                  fontSize={{ base: "lg", md: "xl" }}
                  px={4}
                  py={2}
                  borderRadius="full"
                  bg="#0078D4"
                  color="white"
                  fontWeight="black"
                >
                  STEP 1
                </Badge>
                <Text 
                  fontSize={{ base: "lg", md: "xl" }}
                  fontWeight="bold"
                  color="#1A202C"
                  textAlign="center"
                >
                  {t('homeStep1Title')}
                </Text>
                <Text 
                  fontSize={{ base: "md", md: "lg" }}
                  color="gray.600"
                  textAlign="center"
                >
                  {t('homeStep1Desc')}
                </Text>
              </VStack>

              {/* Step 2 */}
              <VStack spacing={3}>
                <Box
                  bg="#FFD700"
                  borderRadius="full"
                  p={4}
                  boxShadow="0 4px 15px rgba(255,215,0,0.3)"
                >
                  <Icon as={FaEnvelope} boxSize={{ base: 8, md: 10 }} color="#0078D4" />
                </Box>
                <Badge
                  fontSize={{ base: "lg", md: "xl" }}
                  px={4}
                  py={2}
                  borderRadius="full"
                  bg="#0078D4"
                  color="white"
                  fontWeight="black"
                >
                  STEP 2
                </Badge>
                <Text 
                  fontSize={{ base: "lg", md: "xl" }}
                  fontWeight="bold"
                  color="#1A202C"
                  textAlign="center"
                >
                  {t('homeStep2Title')}
                </Text>
                <Text 
                  fontSize={{ base: "md", md: "lg" }}
                  color="gray.600"
                  textAlign="center"
                >
                  {t('homeStep2Desc')}
                </Text>
              </VStack>

              {/* Step 3 */}
              <VStack spacing={3}>
                <Box
                  bg="#FFD700"
                  borderRadius="full"
                  p={4}
                  boxShadow="0 4px 15px rgba(255,215,0,0.3)"
                >
                  <Icon as={FaCheckCircle} boxSize={{ base: 8, md: 10 }} color="#0078D4" />
                </Box>
                <Badge
                  fontSize={{ base: "lg", md: "xl" }}
                  px={4}
                  py={2}
                  borderRadius="full"
                  bg="#0078D4"
                  color="white"
                  fontWeight="black"
                >
                  STEP 3
                </Badge>
                <Text 
                  fontSize={{ base: "lg", md: "xl" }}
                  fontWeight="bold"
                  color="#1A202C"
                  textAlign="center"
                >
                  {t('homeStep3Title')}
                </Text>
                <Text 
                  fontSize={{ base: "md", md: "lg" }}
                  color="gray.600"
                  textAlign="center"
                >
                  {t('homeStep3Desc')}
                </Text>
              </VStack>
            </SimpleGrid>
          </Box>

          {/* Second CTA - Bottom of page */}
          <Box
            w="100%"
            maxW="600px"
            px={4}
            pb={8}
          >
            <Button
              size="lg"
              w="100%"
              h={{ base: "70px", md: "90px" }}
              fontSize={{ base: "xl", md: "2xl" }}
              fontWeight="black"
              bg="#0078D4"
              color="white"
              borderRadius="2xl"
              boxShadow="0 15px 40px rgba(0,120,212,0.5)"
              _hover={{
                transform: "translateY(-4px)",
                boxShadow: "0 20px 50px rgba(0,120,212,0.6)",
                bg: "#0066B8"
              }}
              transition="all 0.3s"
              onClick={() => navigate('/fix-it')}
              rightIcon={<Icon as={FaArrowRight} boxSize={{ base: 5, md: 7 }} />}
            >
              {t('homeCtaBottom')}
            </Button>
          </Box>

          {/* Trust Indicators */}
          <Flex
            direction={{ base: "column", md: "row" }}
            gap={4}
            justify="center"
            align="center"
            flexWrap="wrap"
            pb={8}
          >
            <HStack spacing={2} bg="white" px={6} py={3} borderRadius="full" boxShadow="md">
              <Icon as={FaCheckCircle} color="green.500" boxSize={5} />
              <Text fontWeight="bold" color="#1A202C">100% Free</Text>
            </HStack>
            <HStack spacing={2} bg="white" px={6} py={3} borderRadius="full" boxShadow="md">
              <Icon as={FaCheckCircle} color="green.500" boxSize={5} />
              <Text fontWeight="bold" color="#1A202C">No Obligation</Text>
            </HStack>
            <HStack spacing={2} bg="white" px={6} py={3} borderRadius="full" boxShadow="md">
              <Icon as={FaCheckCircle} color="green.500" boxSize={5} />
              <Text fontWeight="bold" color="#1A202C">2 Days Response</Text>
            </HStack>
          </Flex>

        </VStack>
      </Container>
    </Box>
  );
};

export default Home;
