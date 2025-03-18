import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Input,
  Select,
  VStack,
  Heading,
  Text,
  Textarea,
  useToast,
  Spinner,
  Card,
  CardBody,
  Divider,
  Badge,
  HStack,
  Link,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react';

const SecondHandCarCheck = () => {
  const [brand, setBrand] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [mileage, setMileage] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [carData, setCarData] = useState({});
  const [availableModels, setAvailableModels] = useState([]);
  const [loadingCarData, setLoadingCarData] = useState(true);
  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!brand || !model || !year || !mileage) {
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
    setResult(null);

    try {
      const response = await fetch('http://localhost:8099/api/check-used-car', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          brand,
          model,
          year: parseInt(year),
          mileage: parseInt(mileage),
          price: 0, // Setting a default value since we removed the price field
          description,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get recommendation');
      }

      const data = await response.json();
      setResult(data);
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

  // Fetch car data when component mounts
  useEffect(() => {
    const fetchCarData = async () => {
      setLoadingCarData(true);
      try {
        const response = await fetch('http://localhost:8099/api/car-data');
        if (!response.ok) {
          throw new Error('Failed to fetch car data');
        }
        const data = await response.json();
        setCarData(data);
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to load car brands and models',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setLoadingCarData(false);
      }
    };

    fetchCarData();
  }, [toast]);

  // Update available models when brand changes
  useEffect(() => {
    if (brand && carData[brand]) {
      setAvailableModels(carData[brand].models);
      setModel(''); // Reset model when brand changes
    } else {
      setAvailableModels([]);
    }
  }, [brand, carData]);

  // Generate years from 2000 to current year
  const generateYears = () => {
    const years = [];
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= 2000; year--) {
      years.push(year);
    }
    return years;
  };

  const years = generateYears();

  // Get recommendation color based on score
  const getRecommendationColor = (score) => {
    if (score >= 8) return 'green';
    if (score >= 5) return 'yellow';
    return 'red';
  };

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Box textAlign="center">
          <Heading mb={4}>Second-Hand Car Check</Heading>
          <Text color="gray.600">
            Get expert advice on whether you should buy a specific used car based on real
            user experiences and online reviews.
          </Text>
        </Box>

        {!result ? (
          <Card>
            <CardBody>
              <form onSubmit={handleSubmit}>
                <VStack spacing={4} align="stretch">
                  <HStack spacing={4}>
                    <FormControl isRequired>
                      <FormLabel>Car Brand</FormLabel>
                      <Select
                        placeholder="Select brand"
                        value={brand}
                        onChange={(e) => setBrand(e.target.value)}
                        isDisabled={loadingCarData}
                      >
                        {Object.keys(carData).map((brandName) => (
                          <option key={brandName} value={brandName}>
                            {brandName}
                          </option>
                        ))}
                      </Select>
                    </FormControl>

                    <FormControl isRequired>
                      <FormLabel>Model</FormLabel>
                      <Select
                        placeholder="Select model"
                        value={model}
                        onChange={(e) => setModel(e.target.value)}
                        isDisabled={!brand || loadingCarData}
                      >
                        {availableModels.map((modelName) => (
                          <option key={modelName} value={modelName}>
                            {modelName}
                          </option>
                        ))}
                      </Select>
                    </FormControl>
                  </HStack>

                  <HStack spacing={4}>
                    <FormControl isRequired>
                      <FormLabel>Year</FormLabel>
                      <Select
                        placeholder="Select year"
                        value={year}
                        onChange={(e) => setYear(e.target.value)}
                      >
                        {years.map((y) => (
                          <option key={y} value={y}>
                            {y}
                          </option>
                        ))}
                      </Select>
                    </FormControl>

                    <FormControl isRequired>
                      <FormLabel>Mileage (km)</FormLabel>
                      <Input
                        type="number"
                        value={mileage}
                        onChange={(e) => setMileage(e.target.value)}
                        placeholder="e.g., 50000"
                      />
                    </FormControl>
                  </HStack>

                  <FormControl>
                    <FormLabel>Additional Information (optional)</FormLabel>
                    <Textarea
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                      placeholder="Enter any additional details about the car (condition, features, concerns, etc.)"
                      rows={4}
                    />
                  </FormControl>

                  <Button
                    type="submit"
                    colorScheme="yellow"
                    size="lg"
                    width="full"
                    mt={4}
                    isLoading={loading}
                    loadingText="Analyzing..."
                  >
                    Check This Car
                  </Button>
                </VStack>
              </form>
            </CardBody>
          </Card>
        ) : (
          <VStack spacing={6} align="stretch">
            <Card>
              <CardBody>
                <VStack spacing={4} align="start">
                  <Heading size="md">
                    {result.car_info.brand} {result.car_info.model} ({result.car_info.year})
                  </Heading>
                  
                  <HStack>
                    <Text fontWeight="bold">Mileage:</Text>
                    <Text>{result.car_info.mileage.toLocaleString()} km</Text>
                  </HStack>
                  
                  <Divider />
                  
                  <VStack align="start" spacing={2} width="100%">
                    <HStack width="100%" justifyContent="space-between">
                      <Text fontWeight="bold">Our Recommendation:</Text>
                      <Badge 
                        colorScheme={getRecommendationColor(result.score)} 
                        fontSize="lg" 
                        px={3} 
                        py={1}
                        borderRadius="md"
                      >
                        {result.recommendation}
                      </Badge>
                    </HStack>
                    
                    <Text>{result.summary}</Text>
                  </VStack>
                </VStack>
              </CardBody>
            </Card>
            
            <Card>
              <CardBody>
                <VStack align="start" spacing={4}>
                  <Heading size="md">Common Issues & Feedback</Heading>
                  
                  {result.issues.map((issue, idx) => (
                    <Alert 
                      key={idx} 
                      status={issue.severity} 
                      variant="left-accent" 
                      borderRadius="md"
                    >
                      <AlertIcon />
                      <Box>
                        <AlertTitle>{issue.title}</AlertTitle>
                        <AlertDescription>{issue.description}</AlertDescription>
                      </Box>
                    </Alert>
                  ))}
                </VStack>
              </CardBody>
            </Card>
            
            <Card>
              <CardBody>
                <VStack align="start" spacing={4}>
                  <Heading size="md">Sources</Heading>
                  
                  <VStack align="start" spacing={2} width="100%">
                    {result.sources.map((source, idx) => (
                      <Link 
                        key={idx} 
                        href={source.url} 
                        color="blue.500" 
                        isExternal
                      >
                        {source.title}
                      </Link>
                    ))}
                  </VStack>
                </VStack>
              </CardBody>
            </Card>
            
            <Button
              colorScheme="gray"
              onClick={() => setResult(null)}
              width="full"
            >
              Check Another Car
            </Button>
          </VStack>
        )}

        {loading && (
          <Box textAlign="center" py={10}>
            <Spinner size="xl" color="yellow.500" />
            <Text mt={4}>
              Researching this car model... This may take a moment as we check
              online forums and reviews.
            </Text>
          </Box>
        )}
      </VStack>
    </Container>
  );
};

export default SecondHandCarCheck;
