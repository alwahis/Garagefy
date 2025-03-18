import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  Text,
  useToast,
  Container,
  SimpleGrid,
  Textarea,
  HStack,
  InputGroup,
  InputLeftAddon,
} from '@chakra-ui/react';
import { ArrowBackIcon, CheckCircleIcon } from '@chakra-ui/icons';
import { Link, useNavigate } from 'react-router-dom';

const AddGarage = () => {
  const [name, setName] = useState('');
  const [address, setAddress] = useState('');
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [phone, setPhone] = useState('');
  const [openingHours, setOpeningHours] = useState('');
  const [url, setUrl] = useState('');
  const [services, setServices] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [newGarage, setNewGarage] = useState(null);
  
  const toast = useToast();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!name || !address || !latitude || !longitude || !phone) {
      toast({
        title: 'Missing information',
        description: 'Please fill in all required fields',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }
    
    try {
      setLoading(true);
      
      // Parse services from text to JSON object
      let parsedServices = {};
      if (services) {
        // Simple parsing for "key: value" pairs, one per line
        const serviceLines = services.split('\n');
        serviceLines.forEach(line => {
          if (line.includes(':')) {
            const [key, value] = line.split(':').map(part => part.trim());
            parsedServices[key] = value;
          }
        });
      }
      
      const response = await fetch('http://localhost:8099/api/garages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          address,
          latitude: parseFloat(latitude),
          longitude: parseFloat(longitude),
          phone,
          opening_hours: openingHours || undefined,
          url: url || undefined,
          services: Object.keys(parsedServices).length > 0 ? parsedServices : undefined
        }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setSuccess(true);
        setNewGarage(data.garage);
        toast({
          title: 'Success!',
          description: 'Garage has been added successfully',
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
      } else {
        throw new Error(data.detail || 'Failed to add garage');
      }
    } catch (error) {
      toast({
        title: 'Error',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setName('');
    setAddress('');
    setLatitude('');
    setLongitude('');
    setPhone('');
    setOpeningHours('');
    setUrl('');
    setServices('');
    setSuccess(false);
    setNewGarage(null);
  };

  return (
    <Container maxW="container.xl" py={8}>
      <Box mb={6}>
        <Link to="/">
          <Button leftIcon={<ArrowBackIcon />} colorScheme="blue" variant="outline">
            Back to Home
          </Button>
        </Link>
      </Box>
      
      <Box 
        borderWidth="1px" 
        borderRadius="lg" 
        overflow="hidden" 
        p={6} 
        boxShadow="lg"
        bg="white"
      >
        <Heading as="h1" size="xl" mb={6} color="blue.600">
          Add New Garage
        </Heading>
        
        {success ? (
          <VStack spacing={6} align="stretch">
            <Box 
              p={6} 
              bg="green.50" 
              borderRadius="md" 
              borderLeftWidth="4px" 
              borderLeftColor="green.400"
            >
              <HStack>
                <CheckCircleIcon color="green.500" boxSize={6} />
                <Heading size="md" color="green.600">Garage Added Successfully!</Heading>
              </HStack>
              <Text mt={2}>The garage has been added to the Garagefy database.</Text>
            </Box>
            
            {newGarage && (
              <Box p={4} borderWidth="1px" borderRadius="md">
                <Heading size="md" mb={3}>Garage Details:</Heading>
                <SimpleGrid columns={2} spacing={4}>
                  <Box>
                    <Text fontWeight="bold">Name:</Text>
                    <Text>{newGarage.name}</Text>
                  </Box>
                  <Box>
                    <Text fontWeight="bold">Address:</Text>
                    <Text>{newGarage.address}</Text>
                  </Box>
                  <Box>
                    <Text fontWeight="bold">Phone:</Text>
                    <Text>{newGarage.phone}</Text>
                  </Box>
                  <Box>
                    <Text fontWeight="bold">Coordinates:</Text>
                    <Text>{newGarage.latitude}, {newGarage.longitude}</Text>
                  </Box>
                  {newGarage.opening_hours && (
                    <Box>
                      <Text fontWeight="bold">Opening Hours:</Text>
                      <Text>{newGarage.opening_hours}</Text>
                    </Box>
                  )}
                  {newGarage.url && (
                    <Box>
                      <Text fontWeight="bold">Website:</Text>
                      <Text>{newGarage.url}</Text>
                    </Box>
                  )}
                </SimpleGrid>
              </Box>
            )}
            
            <HStack spacing={4} mt={4}>
              <Button colorScheme="blue" onClick={handleReset}>
                Add Another Garage
              </Button>
              <Button variant="outline" onClick={() => navigate('/')}>
                Return to Home
              </Button>
            </HStack>
          </VStack>
        ) : (
          <form onSubmit={handleSubmit}>
            <VStack spacing={6} align="stretch">
              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
                <FormControl isRequired>
                  <FormLabel>Garage Name</FormLabel>
                  <Input 
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g., AutoTech Garage"
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Phone Number</FormLabel>
                  <InputGroup>
                    <InputLeftAddon>+</InputLeftAddon>
                    <Input 
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="352 123 456 789"
                    />
                  </InputGroup>
                </FormControl>
              </SimpleGrid>
              
              <FormControl isRequired>
                <FormLabel>Address</FormLabel>
                <Input 
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="e.g., 123 Main Street, Luxembourg City, 1234"
                />
              </FormControl>
              
              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
                <FormControl isRequired>
                  <FormLabel>Latitude</FormLabel>
                  <Input 
                    type="number" 
                    step="0.000001"
                    value={latitude}
                    onChange={(e) => setLatitude(e.target.value)}
                    placeholder="e.g., 49.611622"
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Longitude</FormLabel>
                  <Input 
                    type="number" 
                    step="0.000001"
                    value={longitude}
                    onChange={(e) => setLongitude(e.target.value)}
                    placeholder="e.g., 6.129997"
                  />
                </FormControl>
              </SimpleGrid>
              
              <FormControl>
                <FormLabel>Opening Hours</FormLabel>
                <Input 
                  value={openingHours}
                  onChange={(e) => setOpeningHours(e.target.value)}
                  placeholder="e.g., Mon-Fri: 8:00-18:00, Sat: 9:00-13:00"
                />
              </FormControl>
              
              <FormControl>
                <FormLabel>Website URL</FormLabel>
                <Input 
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="e.g., https://example.com"
                />
              </FormControl>
              
              <FormControl>
                <FormLabel>Services (one per line, format: "service: description")</FormLabel>
                <Textarea 
                  value={services}
                  onChange={(e) => setServices(e.target.value)}
                  placeholder="e.g., Oil Change: €50\nBrake Service: €120\nTire Replacement: €200"
                  rows={5}
                />
              </FormControl>
              
              <Button 
                type="submit" 
                colorScheme="blue" 
                size="lg" 
                isLoading={loading}
                loadingText="Adding..."
              >
                Add Garage
              </Button>
            </VStack>
          </form>
        )}
      </Box>
    </Container>
  );
};

export default AddGarage;
