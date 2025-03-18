import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  HStack,
  Text,
  Heading,
  Container,
  SimpleGrid,
  useToast,
  Icon,
  Badge,
  Divider,
  Skeleton,
  Alert,
  AlertIcon,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  ModalFooter,
  Select,
  Textarea,
  useDisclosure,
  Spinner,
  Card,
  CardBody,
  Stack,
  List,
  ListItem,
  ListIcon,
  Flex
} from '@chakra-ui/react';
import { 
  FaMapMarkerAlt, 
  FaPhone, 
  FaGlobe, 
  FaCalendarAlt, 
  FaStar, 
  FaTools, 
  FaCar,
  FaCheck,
  FaLocationArrow,
  FaMapMarked
} from 'react-icons/fa';
import config from '../config';
import axios from 'axios';

const GarageCard = ({ garage, onBookAppointment }) => {
  return (
    <Card
      bg="white"
      shadow="lg"
      borderRadius="xl"
      overflow="hidden"
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-8px)', shadow: '2xl' }}
    >
      <CardBody p={0}>
        <Box bg="brand.500" p={4}>
          <Heading size="md" color="white" noOfLines={1}>{garage.name}</Heading>
        </Box>
        
        <VStack align="stretch" spacing={3} p={4}>
          <HStack>
            <Icon as={FaMapMarkerAlt} color="brand.500" />
            <Text color="gray.700" fontSize="sm" fontWeight="medium">{garage.address}</Text>
          </HStack>
          
          <HStack>
            <Icon as={FaPhone} color="brand.500" />
            <Text color="gray.700" fontSize="sm">{garage.phone || 'No phone available'}</Text>
          </HStack>
          
          {garage.specialties && garage.specialties.length > 0 && (
            <Box>
              <Text fontSize="sm" fontWeight="bold" color="gray.600">Specialties:</Text>
              <Flex mt={1} flexWrap="wrap" gap={1}>
                {garage.specialties.map((specialty, idx) => (
                  <Badge key={idx} colorScheme="blue" fontSize="xs">
                    {specialty}
                  </Badge>
                ))}
              </Flex>
            </Box>
          )}
          
          {typeof garage.distance === 'number' && (
            <HStack>
              <Icon as={FaLocationArrow} color="green.500" />
              <Text color="green.600" fontWeight="bold">
                {garage.distance.toFixed(1)} km away
              </Text>
            </HStack>
          )}
          
          <Divider />
          
          <Button 
            colorScheme="brand" 
            leftIcon={<Icon as={FaCalendarAlt} />}
            onClick={() => onBookAppointment(garage)}
            size="md"
            borderRadius="lg"
            w="full"
          >
            Book Appointment
          </Button>
        </VStack>
      </CardBody>
    </Card>
  );
};

const BookingModal = ({ isOpen, onClose, garage, onSubmit }) => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    date: '',
    time: '',
    service: '',
    comments: ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await onSubmit({
        ...formData,
        garage_id: garage.id
      });
      onClose();
    } catch (error) {
      console.error('Booking error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <Modal isOpen={isOpen} onClose={onClose} size="xl">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader bg="brand.500" color="white">
          Book Appointment at {garage?.name}
        </ModalHeader>
        <ModalCloseButton color="white" />
        
        <ModalBody py={6}>
          <form onSubmit={handleSubmit}>
            <VStack spacing={4}>
              <FormControl isRequired>
                <FormLabel>Your Name</FormLabel>
                <Input 
                  name="name" 
                  value={formData.name} 
                  onChange={handleChange} 
                  placeholder="Enter your full name"
                  focusBorderColor="brand.500"
                />
              </FormControl>
              
              <HStack w="full">
                <FormControl isRequired>
                  <FormLabel>Phone</FormLabel>
                  <Input 
                    name="phone" 
                    value={formData.phone} 
                    onChange={handleChange}
                    placeholder="Your phone number" 
                    focusBorderColor="brand.500"
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Email</FormLabel>
                  <Input 
                    name="email" 
                    type="email" 
                    value={formData.email} 
                    onChange={handleChange}
                    placeholder="Your email address" 
                    focusBorderColor="brand.500"
                  />
                </FormControl>
              </HStack>
              
              <HStack w="full">
                <FormControl isRequired>
                  <FormLabel>Date</FormLabel>
                  <Input 
                    name="date" 
                    type="date" 
                    value={formData.date} 
                    onChange={handleChange}
                    min={new Date().toISOString().split('T')[0]}
                    focusBorderColor="brand.500"
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Time</FormLabel>
                  <Input 
                    name="time" 
                    type="time" 
                    value={formData.time} 
                    onChange={handleChange} 
                    focusBorderColor="brand.500"
                  />
                </FormControl>
              </HStack>
              
              <FormControl isRequired>
                <FormLabel>Service Needed</FormLabel>
                <Select 
                  name="service" 
                  value={formData.service} 
                  onChange={handleChange}
                  placeholder="Select a service"
                  focusBorderColor="brand.500"
                >
                  <option value="diagnosis">Diagnostic Check</option>
                  <option value="repair">Repair Service</option>
                  <option value="maintenance">Maintenance Service</option>
                  <option value="inspection">Vehicle Inspection</option>
                  <option value="other">Other</option>
                </Select>
              </FormControl>
              
              <FormControl>
                <FormLabel>Additional Comments</FormLabel>
                <Textarea 
                  name="comments" 
                  value={formData.comments} 
                  onChange={handleChange}
                  placeholder="Describe your car issue or any special requests"
                  focusBorderColor="brand.500"
                />
              </FormControl>
            </VStack>
          </form>
        </ModalBody>
        
        <ModalFooter>
          <Button variant="outline" mr={3} onClick={onClose}>
            Cancel
          </Button>
          <Button 
            colorScheme="brand" 
            onClick={handleSubmit}
            isLoading={isSubmitting}
            loadingText="Booking..."
          >
            Book Appointment
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

const FindGarage = () => {
  const [location, setLocation] = useState({ latitude: null, longitude: null });
  const [garages, setGarages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLocating, setIsLocating] = useState(false);
  const [error, setError] = useState(null);
  const [selectedGarage, setSelectedGarage] = useState(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const toast = useToast();
  
  const getLocation = () => {
    setIsLocating(true);
    setError(null);
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
          setIsLocating(false);
          fetchNearbyGarages(position.coords.latitude, position.coords.longitude);
        },
        (error) => {
          console.error('Error getting location:', error);
          setIsLocating(false);
          setError('Could not access your location. Please allow location access or enter your address manually.');
        },
        { enableHighAccuracy: true }
      );
    } else {
      setIsLocating(false);
      setError('Geolocation is not supported by your browser.');
    }
  };
  
  useEffect(() => {
    // Get user location on component mount
    getLocation();
  }, []);
  
  const fetchNearbyGarages = async (latitude, longitude) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${config.API_BASE_URL}/find-garages`, {
        latitude,
        longitude,
        max_distance: 20 // 20km radius
      });
      
      if (response.data && response.data.garages) {
        setGarages(response.data.garages);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('Error fetching garages:', error);
      setError('Failed to fetch nearby garages. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleOpenBooking = (garage) => {
    setSelectedGarage(garage);
    onOpen();
  };
  
  const handleBookAppointment = async (bookingData) => {
    try {
      const response = await axios.post(`${config.API_BASE_URL}/api/bookings`, bookingData);
      
      if (response.data && response.data.reference) {
        toast({
          title: 'Booking Successful',
          description: `Your appointment has been scheduled. Reference: ${response.data.reference}`,
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error('Error booking appointment:', error);
      toast({
        title: 'Booking Failed',
        description: 'There was an error booking your appointment. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      throw error;
    }
  };
  
  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Box textAlign="center">
          <Heading size="xl" mb={2} color="brand.600">Find Nearby Garages</Heading>
          <Text color="gray.600">Discover trusted automotive repair shops in your area</Text>
        </Box>
        
        <Box 
          bg="white" 
          p={6} 
          borderRadius="xl" 
          shadow="md"
          borderWidth="1px"
          borderColor="gray.200"
        >
          <VStack spacing={4}>
            <HStack w="full" justify="space-between">
              <Box>
                <Heading size="md" mb={2}>Your Location</Heading>
                {location.latitude && location.longitude ? (
                  <HStack>
                    <Icon as={FaMapMarked} color="green.500" />
                    <Text>
                      Location obtained ({location.latitude.toFixed(4)}, {location.longitude.toFixed(4)})
                    </Text>
                  </HStack>
                ) : (
                  <Text color="gray.500">No location data available</Text>
                )}
              </Box>
              <Button
                leftIcon={<Icon as={FaLocationArrow} />}
                colorScheme="brand"
                onClick={getLocation}
                isLoading={isLocating}
                loadingText="Locating..."
              >
                Update Location
              </Button>
            </HStack>
            
            {error && (
              <Alert status="error" borderRadius="md">
                <AlertIcon />
                {error}
              </Alert>
            )}
          </VStack>
        </Box>
        
        <Box>
          <Heading size="lg" mb={4} color="brand.500">
            {isLoading ? 'Searching for garages...' : 
              garages.length > 0 ? `Found ${garages.length} garages nearby` : 'No garages found'}
          </Heading>
          
          {isLoading ? (
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
              {[1, 2, 3].map(i => (
                <Skeleton key={i} height="240px" borderRadius="lg" />
              ))}
            </SimpleGrid>
          ) : (
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
              {garages.map(garage => (
                <GarageCard
                  key={garage.id}
                  garage={garage}
                  onBookAppointment={handleOpenBooking}
                />
              ))}
              
              {garages.length === 0 && !isLoading && !error && (
                <Box 
                  p={6} 
                  borderWidth="1px" 
                  borderRadius="lg" 
                  borderStyle="dashed"
                  borderColor="gray.300"
                  bg="gray.50"
                  textAlign="center"
                  gridColumn={{ lg: "span 3" }}
                >
                  <Icon as={FaMapMarkerAlt} w={10} h={10} color="gray.400" mb={4} />
                  <Heading size="md" mb={2} color="gray.500">No Garages Found</Heading>
                  <Text color="gray.500">
                    Try updating your location or increasing the search radius.
                  </Text>
                </Box>
              )}
            </SimpleGrid>
          )}
        </Box>
      </VStack>
      
      {selectedGarage && (
        <BookingModal
          isOpen={isOpen}
          onClose={onClose}
          garage={selectedGarage}
          onSubmit={handleBookAppointment}
        />
      )}
    </Container>
  );
};

export default FindGarage;
