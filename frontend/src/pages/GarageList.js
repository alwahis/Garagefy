import React, { useState, useEffect } from 'react';
import {
  Box,
  VStack,
  Heading,
  Text,
  Container,
  Card,
  CardBody,
  Link,
  Spinner,
  Alert,
  AlertIcon,
  SimpleGrid,
  Icon,
  Flex,
  Button,
  Divider,
  useColorModeValue,
  CardHeader,
  Input,
  InputGroup,
  InputLeftElement,
  Wrap,
  WrapItem,
  Tag,
  Badge
} from '@chakra-ui/react';
import { 
  FaMapMarkerAlt, 
  FaPhone, 
  FaClock, 
  FaTools, 
  FaExternalLinkAlt, 
  FaSearch,
  FaStar,
  FaRoute,
  FaPhoneAlt,
  FaDirections
} from 'react-icons/fa';
import axios from 'axios';
import config from '../config';

const GarageCard = ({ garage }) => {
  const cardBg = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('transparent', 'gray.600');
  
  return (
    <Card 
      variant="outline" 
      bg={cardBg} 
      borderColor={borderColor}
      shadow="md"
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-5px)', shadow: 'lg' }}
      height="100%"
    >
      <CardHeader 
        bg={useColorModeValue('brand.50', 'gray.800')} 
        borderBottomWidth="1px" 
        borderColor={borderColor}
        pb={3}
      >
        <Heading size="md" noOfLines={1}>{garage.name}</Heading>
        {garage.distance && (
          <Flex align="center" mt={2}>
            <Icon as={FaRoute} color="secondary.500" mr={1} />
            <Text fontWeight="medium" color="secondary.600">
              {garage.distance} km away
            </Text>
          </Flex>
        )}
      </CardHeader>
      <CardBody>
        <VStack align="stretch" spacing={4}>
          <Flex align="flex-start">
            <Box 
              bg="accent.500" 
              p={2} 
              borderRadius="full" 
              display="inline-flex"
              mr={2}
            >
              <Icon as={FaMapMarkerAlt} color="white" />
            </Box>
            <Text>{garage.address}</Text>
          </Flex>
          
          <Flex align="center">
            <Icon as={FaPhone} color="secondary.500" mr={2} />
            <Link href={`tel:${garage.phone}`} color="blue.600" fontWeight="medium">
              {garage.phone}
            </Link>
          </Flex>
          
          <Flex align="flex-start">
            <Icon as={FaClock} color="secondary.500" mt={1} mr={2} />
            <Text>{garage.opening_hours}</Text>
          </Flex>
          
          {garage.rating && (
            <Flex align="center">
              <Icon as={FaStar} color="brand.400" mr={2} />
              <Text fontWeight="bold">{garage.rating} / 5</Text>
              {garage.reviews && (
                <Text ml={2} color="gray.500" fontSize="sm">
                  ({garage.reviews} reviews)
                </Text>
              )}
            </Flex>
          )}
          
          <Divider />
          
          <Box>
            <Text fontWeight="bold" mb={2} display="flex" alignItems="center">
              <Icon as={FaTools} mr={2} color="accent.500" />
              Services
            </Text>
            <Wrap spacing={2}>
              {garage.services && garage.services.split(',').map((service, idx) => (
                <WrapItem key={idx}>
                  <Tag colorScheme="accent" size="md">
                    {service.trim()}
                  </Tag>
                </WrapItem>
              ))}
            </Wrap>
          </Box>
          
          <Button 
            as={Link} 
            href={garage.url} 
            isExternal 
            colorScheme="accent" 
            variant="outline"
            rightIcon={<FaExternalLinkAlt />}
            mt={2}
          >
            Visit Website
          </Button>
        </VStack>
      </CardBody>
    </Card>
  );
};

const GarageList = () => {
  const [garages, setGarages] = useState([]);
  const [filteredGarages, setFilteredGarages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const cardBg = useColorModeValue('white', 'gray.700');

  useEffect(() => {
    const fetchGarages = async (position) => {
      try {
        const { latitude, longitude } = position.coords;
        const response = await axios.get(`${config.API_BASE_URL}${config.ENDPOINTS.GARAGES}?lat=${latitude}&lng=${longitude}`);
        setGarages(response.data.garages);
        setFilteredGarages(response.data.garages);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching garages:', err);
        setError('Failed to fetch garages. Please try again later.');
        setLoading(false);
      }
    };

    const handleLocationError = (error) => {
      setError('Unable to access your location. Please enable location services.');
      setLoading(false);
    };

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(fetchGarages, handleLocationError);
    } else {
      setError('Geolocation is not supported by your browser.');
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredGarages(garages);
    } else {
      const filtered = garages.filter(garage => 
        garage.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        garage.services?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        garage.address.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredGarages(filtered);
    }
  }, [searchTerm, garages]);

  if (loading) {
    return (
      <Flex justify="center" align="center" minH="calc(100vh - 72px)" direction="column">
        <Spinner size="xl" color="accent.500" thickness="4px" mb={4} />
        <Text color="gray.600">Finding garages near you...</Text>
      </Flex>
    );
  }

  if (error) {
    return (
      <Container maxW="container.xl" py={8}>
        <Alert status="error" borderRadius="md">
          <AlertIcon />
          {error}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Box 
          p={6} 
          borderRadius="lg" 
          bg="white" 
          boxShadow="md"
          bgGradient="linear(to-r, brand.600, secondary.600)"
          color="white"
        >
          <VStack spacing={4} align="stretch">
            <Heading size="xl">Find Garages Near You</Heading>
            <Text fontSize="lg">
              Find the best auto repair shops in your area
            </Text>
          </VStack>
        </Box>

        <InputGroup size="lg" mx="auto" maxW="container.md">
          <InputLeftElement pointerEvents="none">
            <Icon as={FaSearch} color="accent.500" />
          </InputLeftElement>
          <Input 
            placeholder="Search by garage name, service, or location..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            bg="white"
            borderWidth="2px"
            _focus={{ 
              borderColor: "accent.500", 
              boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" 
            }}
          />
        </InputGroup>

        {filteredGarages.length === 0 ? (
          <Alert status="info" borderRadius="md">
            <AlertIcon />
            No garages found matching your search criteria.
          </Alert>
        ) : (
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
            {filteredGarages.map((garage) => (
              <GarageCard key={garage.id} garage={garage} />
            ))}
          </SimpleGrid>
        )}
      </VStack>
    </Container>
  );
};

export default GarageList;
