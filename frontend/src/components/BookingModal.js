import React, { useState } from 'react';
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
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
  useColorModeValue
} from '@chakra-ui/react';
import { FaTools, FaCalendarCheck, FaClock, FaMapMarkerAlt, FaCarAlt } from 'react-icons/fa';
import config from '../config';

const BookingModal = ({ isOpen, onClose, garage, selectedIssue = null }) => {
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [carInfo, setCarInfo] = useState('');
  const [service, setService] = useState(selectedIssue ? selectedIssue.name : '');
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const accentBg = useColorModeValue('brand.50', 'gray.700');

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
          diagnosis_issue: selectedIssue ? selectedIssue.name : null,
          diagnosis_system: selectedIssue ? selectedIssue.system : null
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to book appointment');
      }

      const data = await response.json();
      
      toast({
        title: 'Booking Successful',
        description: `Your appointment has been booked for ${date} at ${time}. Booking reference: ${data.booking_id}`,
        status: 'success',
        duration: 9000,
        isClosable: true,
      });
      
      // Reset form and close modal
      setDate('');
      setTime('');
      setName('');
      setPhone('');
      setEmail('');
      setCarInfo('');
      setService('');
      onClose();
    } catch (error) {
      toast({
        title: 'Booking Failed',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="lg">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader bg={accentBg} borderTopRadius="md">
          <Text>Book an Appointment</Text>
          <Flex align="center" mt={1}>
            <Text fontSize="md" fontWeight="normal">{garage?.name}</Text>
          </Flex>
        </ModalHeader>
        <ModalCloseButton />
        <ModalBody pt={4}>
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
                
                {selectedIssue && (
                  <Box mt={2}>
                    <Text fontWeight="bold" mb={1}>Diagnosed Issue:</Text>
                    <Flex>
                      <Badge colorScheme="red" p={2} borderRadius="md">
                        {selectedIssue.name} ({selectedIssue.probability}% probability)
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

            <FormControl isRequired>
              <FormLabel>Your Name</FormLabel>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter your full name"
              />
            </FormControl>

            <HStack spacing={4}>
              <FormControl isRequired>
                <FormLabel>Phone</FormLabel>
                <Input
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="Enter your phone number"
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Email</FormLabel>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                />
              </FormControl>
            </HStack>

            <FormControl isRequired>
              <FormLabel display="flex" alignItems="center">
                <Icon as={FaTools} mr={2} color="brand.600" />
                Service Needed
              </FormLabel>
              <Select
                placeholder="Select service"
                value={service}
                onChange={(e) => setService(e.target.value)}
              >
                {selectedIssue && (
                  <option value={selectedIssue.name}>{selectedIssue.name} Repair</option>
                )}
                <option value="Regular Maintenance">Regular Maintenance</option>
                <option value="Oil Change">Oil Change</option>
                <option value="Brake Service">Brake Service</option>
                <option value="Tire Replacement">Tire Replacement</option>
                <option value="Engine Repair">Engine Repair</option>
                <option value="Electrical System">Electrical System</option>
                <option value="Diagnostic">Diagnostic</option>
                <option value="Other">Other</option>
              </Select>
            </FormControl>

            <FormControl>
              <FormLabel display="flex" alignItems="center">
                <Icon as={FaCarAlt} mr={2} color="brand.600" />
                Car Information (optional)
              </FormLabel>
              <Textarea
                value={carInfo}
                onChange={(e) => setCarInfo(e.target.value)}
                placeholder="Enter your car make, model, year, and any specific issues"
              />
            </FormControl>
          </VStack>
        </ModalBody>

        <ModalFooter>
          <Button variant="ghost" mr={3} onClick={onClose}>
            Cancel
          </Button>
          <Button 
            colorScheme="brand" 
            onClick={handleSubmit}
            isLoading={loading}
            loadingText="Booking..."
            leftIcon={<Icon as={FaCalendarCheck} />}
          >
            Book Appointment
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default BookingModal;
