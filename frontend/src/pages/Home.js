import React from 'react';
import { 
  Box, 
  Container, 
  Heading, 
  VStack, 
  Button, 
  Text, 
  SimpleGrid, 
  Flex, 
  Icon, 
  useColorModeValue 
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { FaTools, FaMapMarkerAlt, FaWrench, FaRobot, FaArrowRight } from 'react-icons/fa';

const FeatureCard = ({ icon, title, description, iconBg, ...rest }) => {
  return (
    <Box
      p={5}
      shadow="md"
      borderWidth="1px"
      borderRadius="lg"
      bg="white"
      borderColor="secondary.200"
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-5px)', shadow: 'lg' }}
      {...rest}
    >
      <Flex direction="column" align="center" textAlign="center">
        <Icon as={icon} boxSize={10} color={iconBg} mb={4} />
        <Heading fontSize="xl" mb={2} color="text.900">{title}</Heading>
        <Text color="text.700">{description}</Text>
      </Flex>
    </Box>
  );
};

const ServiceItem = ({ icon, title }) => (
  <Flex align="center" mb={4}>
    <Icon as={icon} boxSize={6} color="brand.600" mr={3} />
    <Text fontWeight="bold" color="text.900">{title}</Text>
  </Flex>
);

const Home = () => {
  const navigate = useNavigate();
  const bgGradient = useColorModeValue(
    'linear(to-b, brand.600, secondary.600)',
    'linear(to-b, gray.700, gray.800)'
  );

  return (
    <Box bgGradient={bgGradient} minH="calc(100vh - 72px)">
      {/* Hero Section */}
      <Box py={28} bgGradient={bgGradient} color="white">
        <Container maxW="container.xl">
          <VStack spacing={8} textAlign="center">
            <Heading 
              as="h1" 
              size="2xl" 
              fontWeight="bold"
              lineHeight="shorter"
              color="white"
            >
              Your AI-Powered Car Diagnostic Assistant
            </Heading>
            <Text mb={4} fontSize={{ base: "lg", md: "xl" }} color="white">
              Your one-stop solution for car diagnostics and finding the best garages
            </Text>

            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10} mb={20}>
              <FeatureCard
                title="AI Car Diagnosis"
                icon={FaRobot}
                description="Get instant AI-powered diagnosis for your car issues."
                iconBg="brand.600"
              />
              <FeatureCard
                title="Find Nearby Garages"
                icon={FaMapMarkerAlt}
                description="Discover top-rated garages near you."
                iconBg="brand.600"
              />
              <FeatureCard
                title="Used Car Check"
                icon={FaTools}
                description="Verify a used car's history and condition before you buy."
                iconBg="brand.600"
                onClick={() => navigate('/used-car-check')}
              />
            </SimpleGrid>

            <Box
              bgGradient="linear(to-b, brand.600, secondary.600)"
              color="white"
              borderRadius="lg"
              p={8}
              textAlign="center"
              boxShadow="xl"
            >
              <Heading size="xl" mb={4}>
                Ready to diagnose your car?
              </Heading>
              <Text fontSize="lg" mb={6} maxW="2xl" mx="auto" color="white">
                Our AI-powered diagnostic tool can help identify issues with your vehicle in seconds.
                Just describe the symptoms and get an instant analysis.
              </Text>
              <Button
                variant="solid"
                size="lg"
                rightIcon={<Icon as={FaArrowRight} />}
                onClick={() => navigate('/diagnose-car')}
                bg="accent.500"
                _hover={{ bg: 'accent.600' }}
                _active={{ bg: 'accent.700' }}
                color="white"
              >
                Start Diagnosis
              </Button>
            </Box>
          </VStack>
        </Container>
      </Box>

      {/* Features Section */}
      <Box py={20} bg="white">
        <Container maxW="container.xl">
          <VStack spacing={16}>
            <VStack spacing={5} textAlign="center">
              <Heading as="h2" size="xl" color="text.900">
                Our Services
              </Heading>
              <Text maxW="2xl" fontSize="lg" color="text.700">
                We provide a range of services to help you diagnose and repair your car.
              </Text>
            </VStack>

            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10} width="full">
              <FeatureCard 
                icon={FaRobot}
                title="AI Diagnostics"
                description="Get instant AI-powered diagnostics for your car issues."
                iconBg="brand.600"
                onClick={() => navigate('/diagnosis')}
              />
              <FeatureCard 
                icon={FaMapMarkerAlt}
                title="Garage Finder"
                description="Find the nearest trusted garages with ratings, services, and contact information."
                iconBg="brand.600"
                onClick={() => navigate('/garages')}
              />
              <FeatureCard 
                icon={FaWrench}
                title="Used Car Check"
                description="Verify a used car's history and condition before you buy to avoid costly surprises."
                iconBg="brand.600"
                onClick={() => navigate('/used-car-check')}
              />
            </SimpleGrid>
          </VStack>
        </Container>
      </Box>

      {/* How It Works Section */}
      <Box py={20} bg="secondary.50">
        <Container maxW="container.xl">
          <VStack spacing={12}>
            <VStack spacing={5} textAlign="center">
              <Heading as="h2" size="xl" color="text.900">
                How It Works
              </Heading>
              <Text maxW="2xl" fontSize="lg" color="text.700">
                Our platform uses AI to diagnose car issues and provide personalized recommendations.
              </Text>
            </VStack>

            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10} width="full">
              <FeatureCard 
                icon={FaRobot}
                title="AI-Powered Diagnostics"
                description="Our AI engine analyzes your car's symptoms and provides a diagnosis."
                iconBg="brand.600"
              />
              <FeatureCard 
                icon={FaMapMarkerAlt}
                title="Garage Finder"
                description="We connect you with trusted garages near you for repairs and maintenance."
                iconBg="brand.600"
              />
              <FeatureCard 
                icon={FaWrench}
                title="Personalized Recommendations"
                description="Our platform provides personalized recommendations for your car's specific needs."
                iconBg="brand.600"
              />
            </SimpleGrid>
          </VStack>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;
