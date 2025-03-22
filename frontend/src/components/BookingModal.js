import React, { useState, useEffect } from 'react';
import {
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  VStack,
  useToast,
  Text,
  Textarea,
  HStack,
  Box,
  Badge,
  Icon,
  Flex,
  Divider,
  useColorModeValue,
  Alert,
  AlertIcon,
  SimpleGrid
} from '@chakra-ui/react';
import { FaTools, FaCalendarCheck, FaClock, FaMapMarkerAlt, FaCarAlt, FaCheck } from 'react-icons/fa';
import config from '../config';

const BookingModal = ({ garage, issue, vehicle, onClose }) => {
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [carInfo, setCarInfo] = useState(vehicle ? `${vehicle.year} ${vehicle.brand} ${vehicle.model}` : '');
  const [service, setService] = useState(issue ? issue.name : '');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [bookingReference, setBookingReference] = useState(null);
  
  const toast = useToast();
  const accentBg = useColorModeValue('brand.50', 'gray.700');
  const buttonColorScheme = 'brand';

  // Generate available time slots
  const generateTimeSlots = () => {
    const slots = [];
    for (let hour = 8; hour <= 17; hour++) {
      const formattedHour = hour.toString().padStart(2, '0');
      slots.push(`${formattedHour}:00`);
      if (hour < 17) {
        slots.push(`${formattedHour}:30`);
      }
    }
    return slots;
  };

  const timeSlots = generateTimeSlots();

  // Get tomorrow's date as the minimum selectable date
  const getTomorrowDate = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().split('T')[0];
  };

  // Get date 30 days from now as the maximum selectable date
  const getMaxDate = () => {
    const maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + 30);
    return maxDate.toISOString().split('T')[0];
  };

  const handleSubmit = async () => {
    if (!date || !time || !name || !phone || !email || !service) {
      toast({
        title: 'Missing information',
        description: 'Please fill in all required fields',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    setLoading(true);

    try {
      // Generate a mock booking reference for demo purposes
      const mockBookingId = `BK-${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;
      
      // Simulate API call with a timeout
      setTimeout(() => {
        setSuccess(true);
        setBookingReference(mockBookingId);
        setLoading(false);
        
        toast({
          title: 'Booking Successful',
          description: `Your appointment has been booked for ${date} at ${time}. Booking reference: ${mockBookingId}`,
          status: 'success',
          duration: 9000,
          isClosable: true,
        });
      }, 1500);
      
      // In a real implementation, you would make an API call like this:
      /*
      const response = await fetch(`${config.API_BASE_URL}/api/bookings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          garage_id: garage.id,
          date,
          time,
          name,
          phone,
          email,
          car_info: carInfo,
          service,
          notes,
          diagnosis_issue: issue ? issue.name : null,
          diagnosis_system: issue ? issue.system : null
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to book appointment');
      }

      const data = await response.json();
      setSuccess(true);
      setBookingReference(data.booking_id);
      */
      
    } catch (error) {
      toast({
        title: 'Booking Failed',
        description: error.message || 'An error occurred while booking your appointment',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      setLoading(false);
    }
  };

  if (success) {
    return (
      <VStack spacing={6} align="stretch" py={4}>
        <Box 
          p={6} 
          bg="green.50" 
          borderRadius="md" 
          borderWidth="1px" 
          borderColor="green.200"
        >
          <VStack spacing={4} align="center">
            <Icon as={FaCheck} boxSize={12} color="green.500" />
            <Text fontSize="xl" fontWeight="bold" textAlign="center">
              Appointment Booked Successfully!
            </Text>
            <Text textAlign="center">
              Your appointment at {garage.name} has been confirmed for {date} at {time}.
            </Text>
            <Box bg="white" p={4} borderRadius="md" width="100%">
              <Text fontWeight="bold" mb={2}>Booking Reference:</Text>
              <Text fontSize="xl" fontWeight="bold" color="brand.600">
                {bookingReference}
              </Text>
              <Text fontSize="sm" mt={2} color="gray.500">
                Please save this reference number for your records.
              </Text>
            </Box>
          </VStack>
        </Box>
        
        <Box p={4} bg="gray.50" borderRadius="md">
          <Text fontWeight="bold" mb={3}>Appointment Details:</Text>
          <SimpleGrid columns={2} spacing={4}>
            <Box>
              <Text fontWeight="bold">Date:</Text>
              <Text>{date}</Text>
            </Box>
            <Box>
              <Text fontWeight="bold">Time:</Text>
              <Text>{time}</Text>
            </Box>
            <Box>
              <Text fontWeight="bold">Service:</Text>
              <Text>{service}</Text>
            </Box>
            <Box>
              <Text fontWeight="bold">Vehicle:</Text>
              <Text>{carInfo}</Text>
            </Box>
          </SimpleGrid>
        </Box>
        
        <Button 
          colorScheme={buttonColorScheme} 
          onClick={onClose} 
          size="lg"
        >
          Close
        </Button>
      </VStack>
    );
  }

  return (
    <VStack spacing={4} align="stretch">
      <Box p={4} bg="gray.50" borderRadius="md">
        <VStack align="stretch" spacing={3}>
          <Flex align="center">
            <Icon as={FaMapMarkerAlt} mr={2} color="brand.600" />
            <Text>{garage?.address}</Text>
          </Flex>
          
          {garage?.phone && (
            <Flex align="center">
              <Icon as={FaClock} mr={2} color="brand.600" />
              <Text>{garage?.opening_hours || 'Opening hours not available'}</Text>
            </Flex>
          )}
          
          {issue && (
            <Box mt={2}>
              <Text fontWeight="bold" mb={1}>Diagnosed Issue:</Text>
              <Flex>
                <Badge colorScheme="red" p={2} borderRadius="md">
                  {issue.name} ({issue.probability}% probability)
                </Badge>
              </Flex>
            </Box>
          )}
          
          {vehicle && (
            <Box mt={2}>
              <Text fontWeight="bold" mb={1}>Vehicle:</Text>
              <Flex>
                <Badge colorScheme="blue" p={2} borderRadius="md">
                  {vehicle.year} {vehicle.brand} {vehicle.model}
                </Badge>
              </Flex>
            </Box>
          )}
        </VStack>
      </Box>

      <Divider />
      
      <Text fontWeight="bold" fontSize="lg">Appointment Details</Text>

      <FormControl isRequired>
        <FormLabel>Date</FormLabel>
        <Input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          min={getTomorrowDate()}
          max={getMaxDate()}
        />
      </FormControl>

      <FormControl isRequired>
        <FormLabel>Time</FormLabel>
        <Select
          placeholder="Select time"
          value={time}
          onChange={(e) => setTime(e.target.value)}
        >
          {timeSlots.map((slot) => (
            <option key={slot} value={slot}>
              {slot}
            </option>
          ))}
        </Select>
      </FormControl>

      <Divider />
      
      <Text fontWeight="bold" fontSize="lg">Personal Information</Text>

      <FormControl isRequired>
        <FormLabel>Full Name</FormLabel>
        <Input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter your full name"
        />
      </FormControl>

      <FormControl isRequired>
        <FormLabel>Phone Number</FormLabel>
        <Input
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder="Enter your phone number"
          type="tel"
        />
      </FormControl>

      <FormControl isRequired>
        <FormLabel>Email</FormLabel>
        <Input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email address"
          type="email"
        />
      </FormControl>

      <Divider />
      
      <Text fontWeight="bold" fontSize="lg">Service Details</Text>

      <FormControl isRequired>
        <FormLabel>Vehicle Information</FormLabel>
        <Input
          value={carInfo}
          onChange={(e) => setCarInfo(e.target.value)}
          placeholder="Year, Make, Model"
        />
      </FormControl>

      <FormControl isRequired>
        <FormLabel>Service Needed</FormLabel>
        <Input
          value={service}
          onChange={(e) => setService(e.target.value)}
          placeholder="Describe the service needed"
        />
      </FormControl>

      <FormControl>
        <FormLabel>Additional Notes</FormLabel>
        <Textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Any additional information the garage should know"
          rows={3}
        />
      </FormControl>

      <Alert status="info" borderRadius="md">
        <AlertIcon />
        <Text fontSize="sm">
          By booking an appointment, you agree to the garage's cancellation policy. You can cancel or reschedule up to 24 hours before your appointment.
        </Text>
      </Alert>

      <Button
        colorScheme={buttonColorScheme}
        size="lg"
        onClick={handleSubmit}
        isLoading={loading}
        loadingText="Booking..."
        leftIcon={<Icon as={FaCalendarCheck} />}
      >
        Book Appointment
      </Button>
    </VStack>
  );
};

export default BookingModal;
