import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  VStack,
  Heading,
  FormControl,
  FormLabel,
  Textarea,
  Button,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  useToast,
  Select,
  Input,
  SimpleGrid,
  Spinner,
  Text,
} from '@chakra-ui/react';
import axios from 'axios';
import API_BASE_URL from '../config/api';

const carBrands = [
  "Acura", "Alfa Romeo", "Aston Martin", "Audi", "Bentley", "BMW", "Bugatti",
  "Buick", "Cadillac", "Chevrolet", "Chrysler", "Citroën", "Dodge", "Ferrari",
  "Fiat", "Ford", "Genesis", "GMC", "Honda", "Hyundai", "Infiniti", "Jaguar",
  "Jeep", "Kia", "Lamborghini", "Land Rover", "Lexus", "Lincoln", "Lotus",
  "Maserati", "Mazda", "McLaren", "Mercedes-Benz", "MINI", "Mitsubishi",
  "Nissan", "Opel", "Pagani", "Peugeot", "Porsche", "Ram", "Renault",
  "Rolls-Royce", "Saab", "Subaru", "Suzuki", "Tesla", "Toyota", "Volkswagen",
  "Volvo"
];

const currentYear = new Date().getFullYear();
const years = Array.from({ length: 30 }, (_, i) => currentYear - i);

const DiagnosisForm = () => {
  const [description, setDescription] = useState('');
  const [diagnosis, setDiagnosis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingModels, setLoadingModels] = useState(false);
  const [selectedBrand, setSelectedBrand] = useState('');
  const [carModel, setCarModel] = useState('');
  const [carYear, setCarYear] = useState('');
  const [availableModels, setAvailableModels] = useState([]);
  const toast = useToast();

  // Handle brand change to update available models
  const handleBrandChange = (e) => {
    const brand = e.target.value;
    console.log('Brand changed to:', brand);
    setSelectedBrand(brand);
    setCarModel(''); // Reset model when brand changes
    
    if (brand) {
      setLoadingModels(true);
      // Try to fetch models from API, fallback to local data if API fails
      fetchModelsForBrand(brand);
    } else {
      setAvailableModels([]);
    }
  };
  
  // Function to fetch models for a selected brand
  const fetchModelsForBrand = (brand) => {
    try {
      // In a real app, you would fetch models from an API
      // For now, we'll simulate it with a timeout
      setTimeout(() => {
        let models = [];
        // Sample models for demonstration
        if (brand === 'BMW') {
          models = ['3 Series', '5 Series', 'X3', 'X5', 'i4', 'iX'];
        } else if (brand === 'Mercedes-Benz') {
          models = ['C-Class', 'E-Class', 'S-Class', 'GLC', 'GLE', 'EQS'];
        } else if (brand === 'Audi') {
          models = ['A3', 'A4', 'A6', 'Q3', 'Q5', 'e-tron'];
        } else if (brand === 'Toyota') {
          models = ['Corolla', 'Camry', 'RAV4', 'Highlander', 'Prius'];
        } else if (brand === 'Honda') {
          models = ['Civic', 'Accord', 'CR-V', 'Pilot', 'HR-V'];
        } else if (brand === 'Volkswagen') {
          models = ['Golf', 'Passat', 'Tiguan', 'ID.4', 'Atlas'];
        } else {
          models = ['Model 1', 'Model 2', 'Model 3']; // Generic models
        }
        
        // Ensure models is an array of strings
        if (Array.isArray(models)) {
          // Convert any non-string values to strings
          models = models.map(model => String(model));
        } else if (typeof models === 'object' && models !== null) {
          // If models is an object, convert to array of keys
          models = Object.keys(models);
        } else {
          // Fallback to empty array if models is invalid
          models = [];
          console.error('Invalid models data format:', models);
        }
        
        setAvailableModels(models);
        setLoadingModels(false);
      }, 500);
    } catch (error) {
      console.error('Error fetching models:', error);
      setAvailableModels([]);
      setLoadingModels(false);
      toast({
        title: 'Error',
        description: 'Failed to load car models. Please try again.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };
  
  // Effect to monitor selectedBrand changes and update models
  useEffect(() => {
    console.log('Selected brand state updated:', selectedBrand);
    if (selectedBrand) {
      fetchModelsForBrand(selectedBrand);
    }
  }, [selectedBrand]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedBrand || !carModel || !carYear) {
      toast({
        title: 'Error',
        description: 'Please fill in all required fields',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/diagnose`, {
        description,
        carBrand: selectedBrand,
        carModel,
        carYear
      });
      
      if (response.data && response.data.diagnosis) {
        setDiagnosis(response.data.diagnosis);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('Diagnosis error:', error);
      toast({
        title: 'Error',
        description: 'Failed to get diagnosis. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxW="container.md" py={10}>
      <VStack spacing={8} align="stretch">
        <Heading>Describe Your Car Problem</Heading>
        
        <form onSubmit={handleSubmit}>
          <VStack spacing={6}>
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4} w="100%">
              <FormControl isRequired>
                <FormLabel fontWeight="medium" color="text.900">Car Brand</FormLabel>
                <Select
                  placeholder="Choose brand"
                  value={selectedBrand}
                  onChange={handleBrandChange}
                  color="text.900"
                  bg="white"
                  borderColor="gray.300"
                  borderWidth="2px"
                  _hover={{ borderColor: 'brand.500' }}
                  _focus={{ 
                    borderColor: 'brand.500',
                    boxShadow: '0 0 0 1px var(--chakra-colors-brand-500)'
                  }}
                  sx={{
                    option: {
                      color: '#1a1a1a',
                      background: 'white'
                    }
                  }}
                >
                  {carBrands.map((brand) => (
                    <option key={brand} value={brand} style={{color: '#1a1a1a', background: 'white', fontWeight: 'normal'}}>
                      {brand}
                    </option>
                  ))}
                </Select>
              </FormControl>

              <FormControl isRequired>
                <FormLabel fontWeight="medium" color="text.900">Car Model</FormLabel>
                {loadingModels ? (
                  <Box display="flex" alignItems="center" mt={2}>
                    <Spinner size="sm" mr={2} color="brand.500" />
                    <Text fontSize="sm" color="text.700">Loading models...</Text>
                  </Box>
                ) : selectedBrand ? (
                  <Select
                    placeholder="Select model"
                    value={carModel}
                    onChange={(e) => setCarModel(e.target.value)}
                    color="text.900"
                    bg="white"
                    borderColor="gray.300"
                    borderWidth="2px"
                    _hover={{ borderColor: 'brand.500' }}
                    _focus={{ 
                      borderColor: 'brand.500',
                      boxShadow: '0 0 0 1px var(--chakra-colors-brand-500)'
                    }}
                    sx={{
                      option: {
                        color: '#1a1a1a',
                        background: 'white'
                      }
                    }}
                    isDisabled={availableModels.length === 0}
                  >
                    {Array.isArray(availableModels) && availableModels.map((model) => {
                      // Ensure model is a string
                      const modelStr = String(model);
                      return (
                        <option key={modelStr} value={modelStr} style={{color: '#1a1a1a', background: 'white', fontWeight: 'normal'}}>
                          {modelStr}
                        </option>
                      );
                    })}
                  </Select>
                ) : (
                  <Input
                    placeholder="First select a brand"
                    isDisabled
                    color="text.700"
                    bg="gray.50"
                    borderColor="gray.300"
                    borderWidth="2px"
                    opacity={0.7}
                    cursor="not-allowed"
                  />
                )}
              </FormControl>

              <FormControl isRequired>
                <FormLabel fontWeight="medium" color="text.900">Year</FormLabel>
                <Select
                  placeholder="Select year"
                  value={carYear}
                  onChange={(e) => setCarYear(e.target.value)}
                  color="text.900"
                  bg="white"
                  borderColor="gray.300"
                  borderWidth="2px"
                  _hover={{ borderColor: 'brand.500' }}
                  _focus={{ 
                    borderColor: 'brand.500',
                    boxShadow: '0 0 0 1px var(--chakra-colors-brand-500)'
                  }}
                  sx={{
                    option: {
                      color: '#1a1a1a',
                      background: 'white'
                    }
                  }}
                >
                  {years.map((year) => (
                    <option key={year} value={year} style={{color: '#1a1a1a', background: 'white', fontWeight: 'normal'}}>
                      {year}
                    </option>
                  ))}
                </Select>
              </FormControl>
            </SimpleGrid>

            <FormControl isRequired>
              <FormLabel fontWeight="medium" color="text.900">Problem Description</FormLabel>
              <Textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe the symptoms, sounds, or issues you're experiencing with your car..."
                minH="200px"
                color="text.900"
                bg="white"
                borderColor="gray.300"
                borderWidth="2px"
                _hover={{ borderColor: 'brand.500' }}
                _focus={{ 
                  borderColor: 'brand.500',
                  boxShadow: '0 0 0 1px var(--chakra-colors-brand-500)'
                }}
                _placeholder={{ color: 'gray.500', opacity: 1 }}
              />
            </FormControl>

            <Button
              type="submit"
              colorScheme="brand"
              size="lg"
              isLoading={loading}
              w="100%"
              fontWeight="semibold"
              py={6}
              boxShadow="md"
              _hover={{
                transform: 'translateY(-2px)',
                boxShadow: 'lg',
              }}
            >
              Get Diagnosis
            </Button>
          </VStack>
        </form>

        {diagnosis && (
          <Alert
            status="info"
            variant="subtle"
            flexDirection="column"
            alignItems="flex-start"
            p={6}
            borderRadius="md"
          >
            <AlertTitle mb={2} fontSize="lg">
              Diagnosis Result
            </AlertTitle>
            <AlertDescription whiteSpace="pre-wrap">
              {diagnosis}
            </AlertDescription>
          </Alert>
        )}
      </VStack>
    </Container>
  );
};

export default DiagnosisForm;
