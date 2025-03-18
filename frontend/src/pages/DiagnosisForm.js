import React, { useState } from 'react';
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
  const [selectedBrand, setSelectedBrand] = useState('');
  const [carModel, setCarModel] = useState('');
  const [carYear, setCarYear] = useState('');
  const toast = useToast();

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
                <FormLabel>Car Brand</FormLabel>
                <Select
                  placeholder="Choose brand"
                  value={selectedBrand}
                  onChange={(e) => setSelectedBrand(e.target.value)}
                >
                  {carBrands.map((brand) => (
                    <option key={brand} value={brand}>
                      {brand}
                    </option>
                  ))}
                </Select>
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Car Model</FormLabel>
                <Input
                  placeholder="e.g., Civic"
                  value={carModel}
                  onChange={(e) => setCarModel(e.target.value)}
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Year</FormLabel>
                <Select
                  placeholder="Select year"
                  value={carYear}
                  onChange={(e) => setCarYear(e.target.value)}
                >
                  {years.map((year) => (
                    <option key={year} value={year}>
                      {year}
                    </option>
                  ))}
                </Select>
              </FormControl>
            </SimpleGrid>

            <FormControl isRequired>
              <FormLabel>Problem Description</FormLabel>
              <Textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe the symptoms, sounds, or issues you're experiencing with your car..."
                minH="200px"
              />
            </FormControl>

            <Button
              type="submit"
              colorScheme="brand"
              size="lg"
              isLoading={loading}
              w="100%"
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
