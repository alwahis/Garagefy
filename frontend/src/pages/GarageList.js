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
  Badge,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  useDisclosure
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
  FaDirections,
  FaCalendarCheck,
  FaArrowLeft
} from 'react-icons/fa';
import axios from 'axios';
import config from '../config';
import { useLocation, useNavigate } from 'react-router-dom';
import BookingModal from '../components/BookingModal';

const GarageCard = ({ garage, onBookAppointment }) => {
  const cardBg = 'white';
  const borderColor = 'secondary.200';
  const headerBg = 'secondary.50';
  const textColor = 'text.900';
  const mutedTextColor = 'text.700';
  
  return (
    <Card 
      variant="outline" 
      bg={cardBg} 
      borderColor={borderColor}
      shadow="md"
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-5px)', shadow: 'lg' }}
      height="100%"
      cursor="pointer"
      onClick={() => onBookAppointment(garage)}
    >
      <CardHeader 
        bg={headerBg}
        borderBottomWidth="1px" 
        borderColor={borderColor}
        pb={3}
      >
        <Heading size="md" noOfLines={1} color="text.900">{garage.name}</Heading>
        {garage.distance && (
          <Flex align="center" mt={2}>
            <Icon as={FaRoute} color="brand.600" mr={1} />
            <Text fontWeight="medium" color="brand.600">
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
            <Text color={textColor}>{garage.address}</Text>
          </Flex>
          
          <Flex align="flex-start">
            <Box 
              bg="brand.600" 
              p={2} 
              borderRadius="full" 
              display="inline-flex"
              mr={2}
            >
              <Icon as={FaPhone} color="white" />
            </Box>
            <Text color={textColor}>{garage.phone}</Text>
          </Flex>
          
          <Flex align="flex-start">
            <Box 
              bg="secondary.600" 
              p={2} 
              borderRadius="full" 
              display="inline-flex"
              mr={2}
            >
              <Icon as={FaClock} color="white" />
            </Box>
            <VStack align="stretch" spacing={0}>
              <Text fontWeight="medium" color={textColor}>Opening Hours</Text>
              <Text color={mutedTextColor}>{garage.hours}</Text>
            </VStack>
          </Flex>
          
          <Flex mt={1} justify="space-between" align="center">
            <Flex>
              {Array(5).fill('').map((_, i) => (
                <Icon
                  key={i}
                  as={FaStar}
                  color={i < garage.rating ? "accent.500" : "gray.300"}
                  mr={1}
                />
              ))}
            </Flex>
            <Button 
              rightIcon={<FaCalendarCheck />} 
              colorScheme="brand" 
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                onBookAppointment(garage);
              }}
            >
              Book
            </Button>
          </Flex>
          
          <Wrap spacing={2} mt={2}>
            {garage.services?.map((service, index) => (
              <WrapItem key={index}>
                <Tag size="sm" colorScheme="secondary" borderRadius="full">
                  {service}
                </Tag>
              </WrapItem>
            ))}
          </Wrap>
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
  const [selectedGarage, setSelectedGarage] = useState(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const location = useLocation();
  const navigate = useNavigate();
  
  const selectedIssue = location.state?.selectedIssue;
  const vehicleInfo = location.state?.vehicleInfo;

  useEffect(() => {
    const fetchGarages = async (position) => {
      try {
        const { latitude, longitude } = position.coords;
        
        // If we have a selected issue, include it in the request
        let url = `${config.API_BASE_URL}${config.ENDPOINTS.GARAGES}?lat=${latitude}&lng=${longitude}`;
        if (selectedIssue) {
          url += `&service=${encodeURIComponent(selectedIssue.system)}`;
        }
        
        const response = await axios.get(url);
        
        // Handle both array and object response formats
        const garageData = Array.isArray(response.data) 
          ? response.data 
          : response.data.garages || [];
          
        setGarages(garageData);
        setFilteredGarages(garageData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching garages:', err);
        setError('Failed to fetch garages. Please try again later.');
        setLoading(false);
        
        // Even if there's an error, show some demo garages
        const demoGarages = generateDemoGarages();
        setGarages(demoGarages);
        setFilteredGarages(demoGarages);
      }
    };

    const handleLocationError = (error) => {
      console.error('Location error:', error);
      setError('Unable to access your location. Showing garages in a demo area.');
      setLoading(false);
      
      // Show demo garages if location access fails
      const demoGarages = generateDemoGarages();
      setGarages(demoGarages);
      setFilteredGarages(demoGarages);
    };

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(fetchGarages, handleLocationError);
    } else {
      setError('Geolocation is not supported by your browser. Showing garages in a demo area.');
      setLoading(false);
      
      // Show demo garages if geolocation is not supported
      const demoGarages = generateDemoGarages();
      setGarages(demoGarages);
      setFilteredGarages(demoGarages);
    }
  }, [selectedIssue]);

  // Generate demo garages to ensure we always have something to display
  const generateDemoGarages = () => {
    const services = selectedIssue 
      ? [selectedIssue.system]
      : ['Engine Repair', 'Brake Service', 'Oil Change', 'Transmission Repair', 'Electrical System'];
      
    return [
      {
        id: 1,
        name: 'Burger King Auto Service',
        address: '123 Main Street, Your City',
        phone: '(123) 456-7890',
        opening_hours: 'Mon-Fri: 8:00 AM - 6:00 PM, Sat: 9:00 AM - 3:00 PM',
        services: services.join(', '),
        distance: 1.2,
        rating: 4.8,
        reviews: 124
      },
      {
        id: 2,
        name: 'Royal Mechanics',
        address: '456 Oak Avenue, Your City',
        phone: '(123) 456-7891',
        opening_hours: 'Mon-Fri: 7:30 AM - 7:00 PM, Sat: 8:00 AM - 5:00 PM',
        services: services.join(', '),
        distance: 2.5,
        rating: 4.6,
        reviews: 89
      },
      {
        id: 3,
        name: 'Crown Auto Repair',
        address: '789 Pine Boulevard, Your City',
        phone: '(123) 456-7892',
        opening_hours: 'Mon-Sat: 8:00 AM - 8:00 PM',
        services: services.join(', '),
        distance: 3.7,
        rating: 4.5,
        reviews: 76
      }
    ];
  };

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
  
  const handleBookAppointment = (garage) => {
    setSelectedGarage(garage);
    onOpen();
  };
  
  const handleBackToDiagnosis = () => {
    navigate(-1);
  };

  if (loading) {
    return (
      <Flex justify="center" align="center" minH="calc(100vh - 72px)" direction="column">
        <Spinner size="xl" color="accent.500" thickness="4px" mb={4} />
        <Text color="text.50">Finding garages near you...</Text>
      </Flex>
    );
  }

  // Define theme color variables
  const cardBg = 'white';
  const borderColor = 'secondary.200';
  const textColor = 'text.900';
  const mutedTextColor = 'text.700';

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Box 
          p={6} 
          borderRadius="lg" 
          boxShadow="md"
          bg="rgba(0, 0, 0, 0.3)"
          color="text.50"
        >
          <VStack spacing={4} align="stretch">
            <Flex justifyContent="space-between" alignItems="center">
              <Heading size="xl" color={textColor}>
                {selectedIssue 
                  ? `Garages for ${selectedIssue.name}` 
                  : 'Find Garages Near You'}
              </Heading>
              
              {selectedIssue && (
                <Button 
                  leftIcon={<Icon as={FaArrowLeft} />} 
                  onClick={handleBackToDiagnosis}
                  colorScheme="whiteAlpha"
                  variant="outline"
                >
                  Back to Diagnosis
                </Button>
              )}
            </Flex>
            
            {vehicleInfo && (
              <Flex align="center">
                <Badge colorScheme="accent" fontSize="md" px={2} py={1}>
                  {vehicleInfo.year} {vehicleInfo.brand} {vehicleInfo.model}
                </Badge>
              </Flex>
            )}
            
            <Text fontSize="lg" color={textColor}>
              {selectedIssue 
                ? `Find the best auto repair shops that can fix ${selectedIssue.name}` 
                : 'Find the best auto repair shops in your area'}
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
            bg="rgba(0, 0, 0, 0.3)"
            borderWidth="2px"
            _focus={{ 
              borderColor: "accent.500", 
              boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" 
            }}
          />
        </InputGroup>

        {error && (
          <Alert status="warning" borderRadius="md">
            <AlertIcon />
            {error}
          </Alert>
        )}

        {filteredGarages.length === 0 ? (
          <Alert status="info" borderRadius="md">
            <AlertIcon />
            No garages found matching your search criteria.
          </Alert>
        ) : (
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
            {filteredGarages.map((garage) => (
              <GarageCard 
                key={garage.id} 
                garage={garage} 
                onBookAppointment={handleBookAppointment}
              />
            ))}
          </SimpleGrid>
        )}
      </VStack>
      
      {/* Booking Modal */}
      {selectedGarage && (
        <Modal isOpen={isOpen} onClose={onClose} size="xl">
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Book Appointment at {selectedGarage.name}</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <BookingModal 
                garage={selectedGarage} 
                issue={selectedIssue}
                vehicle={vehicleInfo}
                onClose={onClose}
              />
            </ModalBody>
          </ModalContent>
        </Modal>
      )}
    </Container>
  );
};

export default GarageList;
