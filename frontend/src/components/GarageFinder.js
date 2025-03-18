import React, { useState, useEffect } from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Button,
  Icon,
  Heading,
  SimpleGrid,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  FormControl,
  FormLabel,
  Input,
  Select,
  Textarea,
} from '@chakra-ui/react';
import { FaMapMarkerAlt, FaPhone, FaGlobe, FaCalendarAlt } from 'react-icons/fa';
import axios from 'axios';

const GarageCard = ({ garage, onBookAppointment }) => {
  return (
    <Box
      bg="darkBg.800"
      p={6}
      borderRadius="xl"
      borderWidth="1px"
      borderColor="darkBg.600"
      _hover={{ borderColor: 'blue.400', transform: 'translateY(-2px)' }}
      transition="all 0.2s"
    >
      <VStack align="stretch" spacing={4}>
        <Heading size="md" color="white">{garage.name}</Heading>
        
        <HStack color="gray.300">
          <Icon as={FaMapMarkerAlt} />
          <Text>{garage.address}</Text>
        </HStack>

        {garage.phone && (
          <HStack color="gray.300">
            <Icon as={FaPhone} />
            <Text>{garage.phone}</Text>
          </HStack>
        )}

        {garage.website && (
          <HStack color="gray.300">
            <Icon as={FaGlobe} />
            <Text>{garage.website}</Text>
          </HStack>
        )}

        {garage.distance && (
          <Text color="blue.300" fontSize="sm">
            {garage.distance.toFixed(1)} km away
          </Text>
        )}

        <Button
          colorScheme="blue"
          leftIcon={<Icon as={FaCalendarAlt} />}
          onClick={() => onBookAppointment(garage)}
        >
          Book Appointment
        </Button>
      </VStack>
    </Box>
  );
};

const BookingModal = ({ isOpen, onClose, garage, onSubmit }) => {
  const [formData, setFormData] = useState({
    date: '',
    time: '',
    name: '',
    phone: '',
    email: '',
    service: '',
    notes: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="xl">
      <ModalOverlay />
      <ModalContent bg="darkBg.800" color="white">
        <ModalHeader>Book Appointment at {garage?.name}</ModalHeader>
        <ModalCloseButton />
        <ModalBody pb={6}>
          <form onSubmit={handleSubmit}>
            <VStack spacing={4}>
              <FormControl isRequired>
                <FormLabel>Date</FormLabel>
                <Input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleChange}
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Time</FormLabel>
                <Input
                  type="time"
                  name="time"
                  value={formData.time}
                  onChange={handleChange}
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Your Name</FormLabel>
                <Input
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Phone Number</FormLabel>
                <Input
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Email</FormLabel>
                <Input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Service Needed</FormLabel>
                <Select
                  name="service"
                  value={formData.service}
                  onChange={handleChange}
                >
                  <option value="">Select a service</option>
                  <option value="diagnosis">Diagnostic Check</option>
                  <option value="repair">Repair Service</option>
                  <option value="maintenance">Maintenance Service</option>
                </Select>
              </FormControl>

              <FormControl>
                <FormLabel>Additional Notes</FormLabel>
                <Textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleChange}
                />
              </FormControl>

              <Button type="submit" colorScheme="blue" width="full">
                Book Appointment
              </Button>
            </VStack>
          </form>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
};

const GarageFinder = () => {
  const [garages, setGarages] = useState([]);
  const [selectedGarage, setSelectedGarage] = useState(null);
  const [isBookingModalOpen, setIsBookingModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  useEffect(() => {
    fetchNearbyGarages();
  }, []);

  const fetchNearbyGarages = async () => {
    setIsLoading(true);
    try {
      // Get user's location
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject);
      });

      const { latitude, longitude } = position.coords;
      
      // Fetch garages from backend
      const response = await axios.get(`http://localhost:8098/api/garages/nearby?lat=${latitude}&lon=${longitude}`);
      setGarages(response.data);
    } catch (error) {
      console.error('Error fetching garages:', error);
      toast({
        title: 'Error',
        description: 'Failed to fetch nearby garages. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleBookAppointment = (garage) => {
    setSelectedGarage(garage);
    setIsBookingModalOpen(true);
  };

  const handleBookingSubmit = async (formData) => {
    try {
      const response = await axios.post('http://localhost:8098/api/bookings', {
        garage_id: selectedGarage.id,
        ...formData,
      });

      toast({
        title: 'Success!',
        description: 'Your appointment has been booked successfully.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

      setIsBookingModalOpen(false);
    } catch (error) {
      console.error('Error booking appointment:', error);
      toast({
        title: 'Error',
        description: 'Failed to book appointment. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box>
      <VStack spacing={6} align="stretch">
        <Heading size="lg" color="white">Nearby Garages</Heading>
        
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
          {garages.map((garage) => (
            <GarageCard
              key={garage.id}
              garage={garage}
              onBookAppointment={handleBookAppointment}
            />
          ))}
        </SimpleGrid>

        <BookingModal
          isOpen={isBookingModalOpen}
          onClose={() => setIsBookingModalOpen(false)}
          garage={selectedGarage}
          onSubmit={handleBookingSubmit}
        />
      </VStack>
    </Box>
  );
};

export default GarageFinder;
