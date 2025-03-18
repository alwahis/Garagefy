import React from 'react';
import {
  Box,
  Button,
  Container,
  Heading,
  Text,
  VStack,
  SimpleGrid,
  Icon,
  useColorModeValue,
  Flex,
  Image,
  HStack,
  Badge,
  Divider,
} from '@chakra-ui/react';
import { 
  FaTools, 
  FaSearch, 
  FaCar, 
  FaCheckCircle, 
  FaOilCan, 
  FaCog, 
  FaWrench,
  FaTachometerAlt,
  FaMapMarkedAlt,
  FaArrowRight
} from 'react-icons/fa';
import { Link as RouterLink } from 'react-router-dom';

const FeatureCard = ({ title, description, icon, to }) => {
  const cardBg = useColorModeValue('darkBg.800', 'darkBg.700');
  const borderColor = useColorModeValue('brand.700', 'brand.600');
  const accentColor = useColorModeValue('accent.500', 'accent.400');

  return (
    <Box
      as={RouterLink}
      to={to}
      p={6}
      bg={cardBg}
      borderRadius="xl"
      borderWidth="1px"
      borderColor={borderColor}
      position="relative"
      overflow="hidden"
      _hover={{ 
        transform: 'translateY(-4px)', 
        boxShadow: '0 12px 20px rgba(0, 0, 0, 0.2)',
        borderColor: 'brand.500',
      }}
      transition="all 0.3s"
      boxShadow="0 4px 12px rgba(0, 0, 0, 0.15)"
    >
      {/* Decorative element - resembles a car part or tool */}
      <Box
        position="absolute"
        top="-20px"
        right="-20px"
        w="100px"
        h="100px"
        bg={`linear-gradient(45deg, transparent 30%, ${accentColor} 30%)`}
        opacity="0.1"
        borderRadius="full"
      />
      
      <VStack spacing={4} align="flex-start">
        <Flex
          w={14}
          h={14}
          bg="brand.600"
          rounded="lg"
          align="center"
          justify="center"
          mb={2}
          boxShadow="0 4px 8px rgba(0, 0, 0, 0.2)"
          position="relative"
          _after={{
            content: '""',
            position: 'absolute',
            top: '0',
            left: '0',
            right: '0',
            bottom: '0',
            borderRadius: 'lg',
            background: 'linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 50%)',
          }}
        >
          <Icon as={icon} w={7} h={7} color="white" />
        </Flex>
        <Heading size="md" color="white" fontWeight="700">
          {title}
        </Heading>
        <Divider borderColor="darkBg.600" />
        <Text color="gray.300" fontSize="md">{description}</Text>
        <HStack spacing={2} alignSelf="flex-end">
          <Text color="brand.400" fontWeight="bold" fontSize="sm">Learn more</Text>
          <Icon as={FaArrowRight} color="brand.400" w={3} h={3} />
        </HStack>
      </VStack>
    </Box>
  );
};

const ServiceItem = ({ icon, title }) => (
  <HStack spacing={3} align="center">
    <Flex
      w={10}
      h={10}
      bg="rgba(255,255,255,0.1)"
      rounded="md"
      align="center"
      justify="center"
    >
      <Icon as={icon} w={5} h={5} color="accent.400" />
    </Flex>
    <Text color="white" fontWeight="500">{title}</Text>
  </HStack>
);

const Home = () => {
  return (
    <Box>
      {/* Hero Section */}
      <Box
        bg="darkBg.900"
        py={20}
        position="relative"
        overflow="hidden"
        backgroundImage="url('/images/garage-hero-bg.jpg')"
        backgroundSize="cover"
        backgroundPosition="center"
        _before={{
          content: '""',
          position: 'absolute',
          top: 0,
          right: 0,
          bottom: 0,
          left: 0,
          bg: 'darkBg.900',
          opacity: 0.85,
        }}
      >
        {/* Decorative elements */}
        <Box
          position="absolute"
          top="-100px"
          right="-100px"
          w="300px"
          h="300px"
          bg="brand.500"
          opacity="0.05"
          borderRadius="full"
          zIndex="0"
        />
        <Box
          position="absolute"
          bottom="-50px"
          left="-50px"
          w="200px"
          h="200px"
          bg="accent.500"
          opacity="0.05"
          borderRadius="full"
          zIndex="0"
        />
        
        <Container maxW="container.xl" position="relative" zIndex="1">
          <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={10} alignItems="center">
            <VStack spacing={8} align="flex-start">
              <Badge colorScheme="blue" px={3} py={1} borderRadius="full" fontSize="sm" fontWeight="bold">
                AI-POWERED CAR DIAGNOSTICS
              </Badge>
              <Heading
                size="2xl"
                color="white"
                lineHeight="shorter"
                fontWeight="bold"
                maxW="800px"
                bgGradient="linear(to-r, white, gray.300)"
                bgClip="text"
              >
                Your Ultimate Garage &
                <br />
                Car Maintenance Partner
              </Heading>
              <Text fontSize="xl" color="gray.300" maxW="600px">
                Find trusted garages, get expert car diagnostics, and keep your
                vehicle in perfect condition with Garagefy's AI-powered platform.
              </Text>
              
              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4} width="100%">
                <ServiceItem icon={FaWrench} title="Expert Repairs" />
                <ServiceItem icon={FaOilCan} title="Regular Maintenance" />
                <ServiceItem icon={FaTachometerAlt} title="Performance Checks" />
                <ServiceItem icon={FaCog} title="Part Replacements" />
              </SimpleGrid>
              
              <HStack spacing={4}>
                <Button
                  as={RouterLink}
                  to="/find-garage"
                  size="lg"
                  colorScheme="brand"
                  _hover={{
                    transform: 'translateY(-2px)',
                    boxShadow: '0 6px 12px rgba(0, 0, 0, 0.2)',
                  }}
                  boxShadow="0 4px 8px rgba(0, 0, 0, 0.2)"
                  rightIcon={<FaMapMarkedAlt />}
                >
                  Find a Garage Now
                </Button>
                <Button
                  as={RouterLink}
                  to="/diagnose-car"
                  size="lg"
                  variant="outline"
                  colorScheme="brand"
                  _hover={{
                    transform: 'translateY(-2px)',
                    boxShadow: '0 6px 12px rgba(0, 0, 0, 0.1)',
                  }}
                  rightIcon={<FaTools />}
                >
                  Diagnose My Car
                </Button>
              </HStack>
            </VStack>
            
            <Box
              display={{ base: 'none', lg: 'block' }}
              position="relative"
              height="500px"
            >
              <Image
                src="/images/mechanic-car.png"
                alt="Mechanic working on car"
                position="absolute"
                bottom="0"
                right="0"
                maxH="100%"
                objectFit="contain"
                zIndex="2"
              />
            </Box>
          </SimpleGrid>
        </Container>
      </Box>

      {/* Features Section */}
      <Box bg="darkBg.800" py={20}>
        <Container maxW="container.xl">
          <VStack spacing={16}>
            <VStack spacing={4} textAlign="center">
              <Heading 
                size="xl" 
                color="white"
                position="relative"
                _after={{
                  content: '""',
                  position: 'absolute',
                  bottom: '-12px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: '80px',
                  height: '4px',
                  bg: 'brand.500',
                  borderRadius: 'full',
                }}
              >
                Our Services
              </Heading>
              <Text color="gray.400" maxW="700px" pt={6}>
                Garagefy provides a comprehensive suite of tools to keep your vehicle running smoothly
                and help you find the best service providers.
              </Text>
            </VStack>
            
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10} width="100%">
              <FeatureCard
                icon={FaMapMarkedAlt}
                title="Find Garages"
                description="Locate trusted garages near you with detailed reviews, ratings, and specialties from real customers."
                to="/find-garage"
              />
              <FeatureCard
                icon={FaTools}
                title="Car Diagnostics"
                description="Get instant AI-powered diagnostics for your car problems using our advanced system that analyzes symptoms."
                to="/diagnose-car"
              />
              <FeatureCard
                icon={FaCheckCircle}
                title="Second-Hand Car Check"
                description="Get expert advice on whether you should buy a specific used car based on real user experiences and reliability data."
                to="/used-car-check"
              />
            </SimpleGrid>
            
            {/* How It Works Section */}
            <Box 
              mt={20} 
              p={8} 
              borderRadius="xl" 
              bg="darkBg.700" 
              width="100%"
              boxShadow="0 8px 16px rgba(0, 0, 0, 0.2)"
              position="relative"
              overflow="hidden"
            >
              {/* Decorative gear elements */}
              <Box
                position="absolute"
                top="-30px"
                right="-30px"
                opacity="0.1"
                zIndex="0"
              >
                <Icon as={FaCog} w={40} h={40} color="accent.500" />
              </Box>
              <Box
                position="absolute"
                bottom="-20px"
                left="-20px"
                opacity="0.1"
                zIndex="0"
              >
                <Icon as={FaCog} w={24} h={24} color="brand.500" />
              </Box>
              
              <VStack spacing={8} position="relative" zIndex="1">
                <Heading size="lg" color="white">How Garagefy Works</Heading>
                
                <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8} width="100%">
                  <VStack spacing={4} align="center" textAlign="center">
                    <Flex
                      w={16}
                      h={16}
                      bg="brand.600"
                      rounded="full"
                      align="center"
                      justify="center"
                      boxShadow="0 4px 8px rgba(0, 0, 0, 0.2)"
                    >
                      <Text fontSize="2xl" fontWeight="bold" color="white">1</Text>
                    </Flex>
                    <Heading size="md" color="white">Describe Your Issue</Heading>
                    <Text color="gray.300">Tell us about your car problem or what kind of garage you're looking for</Text>
                  </VStack>
                  
                  <VStack spacing={4} align="center" textAlign="center">
                    <Flex
                      w={16}
                      h={16}
                      bg="brand.600"
                      rounded="full"
                      align="center"
                      justify="center"
                      boxShadow="0 4px 8px rgba(0, 0, 0, 0.2)"
                    >
                      <Text fontSize="2xl" fontWeight="bold" color="white">2</Text>
                    </Flex>
                    <Heading size="md" color="white">Get AI Analysis</Heading>
                    <Text color="gray.300">Our AI analyzes your issue and provides recommendations or finds nearby garages</Text>
                  </VStack>
                  
                  <VStack spacing={4} align="center" textAlign="center">
                    <Flex
                      w={16}
                      h={16}
                      bg="brand.600"
                      rounded="full"
                      align="center"
                      justify="center"
                      boxShadow="0 4px 8px rgba(0, 0, 0, 0.2)"
                    >
                      <Text fontSize="2xl" fontWeight="bold" color="white">3</Text>
                    </Flex>
                    <Heading size="md" color="white">Take Action</Heading>
                    <Text color="gray.300">Book an appointment with a garage or follow the diagnostic recommendations</Text>
                  </VStack>
                </SimpleGrid>
              </VStack>
            </Box>
          </VStack>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;
