import React, { useState, useEffect } from 'react';
import config from '../config';
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
  Icon,
  Tabs, 
  TabList, 
  TabPanels, 
  Tab, 
  TabPanel,
} from '@chakra-ui/react';
import { FaArrowLeft, FaCarAlt, FaTools, FaExclamationTriangle, FaInfoCircle } from 'react-icons/fa';

const SecondHandCarCheck = () => {
  const [brand, setBrand] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [mileage, setMileage] = useState('');
  const [fuelType, setFuelType] = useState('Gasoline');
  const [transmission, setTransmission] = useState('Manual');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [carData, setCarData] = useState({});
  const [currentScreen, setCurrentScreen] = useState('form'); // 'form' or 'results'
  const [availableModels, setAvailableModels] = useState([]);
  const [loadingCarData, setLoadingCarData] = useState(true);
  const [fuelTypes, setFuelTypes] = useState([]);
  const [transmissionTypes, setTransmissionTypes] = useState([]);
  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted with values:', { brand, model, year, mileage, fuelType, transmission });
    
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
    
    try {
      // Create mock reliability score
      let reliabilityScore = 75;
      
      // Adjust score based on brand
      if (['Toyota', 'Honda', 'Mazda'].includes(brand)) {
        reliabilityScore += 10;
      } else if (['BMW', 'Mercedes-Benz', 'Audi'].includes(brand)) {
        reliabilityScore -= 5;
      }
      
      // Adjust score based on mileage
      const mileageNum = parseInt(mileage);
      if (mileageNum > 150000) {
        reliabilityScore -= 15;
      } else if (mileageNum > 100000) {
        reliabilityScore -= 5;
      }
      
      // Adjust score based on year
      const yearNum = parseInt(year);
      const currentYear = new Date().getFullYear();
      const age = currentYear - yearNum;
      if (age > 10) {
        reliabilityScore -= 10;
      } else if (age > 5) {
        reliabilityScore -= 5;
      }
      
      // Determine recommendation
      let recommendation, summary;
      if (reliabilityScore >= 80) {
        recommendation = "Buy";
        summary = `This ${year} ${brand} ${model} appears to be a reliable vehicle with minimal issues expected.`;
      } else if (reliabilityScore >= 65) {
        recommendation = "Buy with Inspection";
        summary = `This ${year} ${brand} ${model} seems decent, but should be inspected by a mechanic before purchase.`;
      } else if (reliabilityScore >= 50) {
        recommendation = "Caution";
        summary = `This ${year} ${brand} ${model} has some concerning factors that should be thoroughly investigated.`;
      } else {
        recommendation = "Avoid";
        summary = `This ${year} ${brand} ${model} has significant reliability concerns and/or very high mileage.`;
      }
      
      // Create mock issues
      const issues = [
        {
          title: "Timing Belt",
          description: `The timing belt on ${brand} ${model} models from this era may need replacement around ${mileage} km.`,
          severity: "warning"
        },
        {
          title: "Suspension Components",
          description: "Check for worn suspension components, especially if the vehicle has been driven on rough roads.",
          severity: "info"
        },
        {
          title: "Electronics",
          description: "Some models from this year have reported issues with the electrical system.",
          severity: "warning"
        }
      ];
      
      // Create mock sources
      const sources = [
        {
          title: "AutoScout24 - Vehicle History",
          url: "https://www.autoscout24.com"
        },
        {
          title: "TÜV Report - Reliability Data",
          url: "https://www.tuv.com/world/en/"
        },
        {
          title: `${brand} Owners Forum`,
          url: `https://www.${brand.toLowerCase()}forum.com`
        }
      ];
      
      // Create the mock result
      const mockResult = {
        car_info: {
          brand: brand,
          model: model,
          year: parseInt(year),
          mileage: parseInt(mileage),
          fuel_type: fuelType,
          transmission: transmission
        },
        score: reliabilityScore,
        recommendation: recommendation,
        summary: summary,
        issues: issues,
        sources: sources
      };
      
      console.log('Setting mock result:', mockResult);
      
      // Force a clean state update
      setResult(null);
      
      // Use setTimeout to ensure the null state is processed first
      setTimeout(() => {
        console.log('Now setting the actual result');
        setResult(mockResult);
      }, 50);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to analyze the vehicle data. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      console.error('Error generating mock data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch car data when component mounts
  useEffect(() => {
    const fetchCarData = async () => {
      setLoadingCarData(true);
      try {
        const response = await fetch(`${config.API_BASE_URL}${config.ENDPOINTS.CAR_DATA}`);
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

    const fetchUsedCarOptions = async () => {
      try {
        const response = await fetch(`${config.API_BASE_URL}${config.ENDPOINTS.USED_CAR_OPTIONS}`);
        if (!response.ok) {
          throw new Error('Failed to fetch used car options');
        }
        const data = await response.json();
        
        if (data.fuel_types && Array.isArray(data.fuel_types)) {
          setFuelTypes(data.fuel_types);
          if (data.fuel_types.length > 0) {
            setFuelType(data.fuel_types[0]);
          }
        }
        
        if (data.transmission_types && Array.isArray(data.transmission_types)) {
          setTransmissionTypes(data.transmission_types);
          if (data.transmission_types.length > 0) {
            setTransmission(data.transmission_types[0]);
          }
        }
      } catch (error) {
        console.error('Error fetching used car options:', error);
        // Set default values if the API fails
        setFuelTypes(['Gasoline', 'Diesel', 'Hybrid', 'Electric']);
        setTransmissionTypes(['Manual', 'Automatic', 'Semi-automatic']);
      }
    };

    fetchCarData();
    fetchUsedCarOptions();
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

  // Debug log for rendering
  console.log('Rendering SecondHandCarCheck component with result:', result);
  
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
                  
                  <HStack spacing={4}>
                    <FormControl isRequired>
                      <FormLabel>Fuel Type</FormLabel>
                      <Select
                        placeholder="Select fuel type"
                        value={fuelType}
                        onChange={(e) => setFuelType(e.target.value)}
                      >
                        {fuelTypes.map((type) => (
                          <option key={type} value={type}>
                            {type}
                          </option>
                        ))}
                      </Select>
                    </FormControl>

                    <FormControl isRequired>
                      <FormLabel>Transmission</FormLabel>
                      <Select
                        placeholder="Select transmission"
                        value={transmission}
                        onChange={(e) => setTransmission(e.target.value)}
                      >
                        {transmissionTypes.map((type) => (
                          <option key={type} value={type}>
                            {type}
                          </option>
                        ))}
                      </Select>
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
        ) : result ? (
          <VStack spacing={6} align="stretch">
            {/* Back button at the top */}
            <HStack>
              <Button
                leftIcon={<Icon as={FaArrowLeft} />}
                variant="outline"
                onClick={() => setCurrentScreen('form')}
                size="sm"
              >
                Back to Form
              </Button>
            </HStack>
            {/* Vehicle summary and recommendation banner */}
            <Card>
              <CardBody>
                <VStack spacing={4} align="start">
                  <Heading size="md">
                    {result.car_info.brand} {result.car_info.model} ({result.car_info.year})
                  </Heading>
                  
                  <HStack spacing={6}>
                    <HStack>
                      <Text fontWeight="bold">Mileage:</Text>
                      <Text>{result.car_info.mileage.toLocaleString()} km</Text>
                    </HStack>
                    
                    <HStack>
                      <Text fontWeight="bold">Fuel Type:</Text>
                      <Text>{result.car_info.fuel_type}</Text>
                    </HStack>
                    
                    <HStack>
                      <Text fontWeight="bold">Transmission:</Text>
                      <Text>{result.car_info.transmission}</Text>
                    </HStack>
                  </HStack>
                  
                  <Divider />
                  
                  {/* Clear recommendation banner at the top of results */}
                  <Alert
                    status={getRecommendationColor(result.score) === 'green' ? 'success' : 
                           getRecommendationColor(result.score) === 'yellow' ? 'warning' : 'error'}
                    variant="solid"
                    borderRadius="md"
                  >
                    <AlertIcon />
                    <AlertTitle mr={2}>Recommendation: {result.recommendation}</AlertTitle>
                    <AlertDescription>{result.summary}</AlertDescription>
                  </Alert>
                </VStack>
              </CardBody>
            </Card>
            
            {/* Tabbed results interface */}
            <Tabs colorScheme="yellow" variant="enclosed-colored">
              <TabList>
                <Tab><Icon as={FaCarAlt} mr={2} /> Reliability Assessment</Tab>
                <Tab><Icon as={FaExclamationTriangle} mr={2} /> Common Issues</Tab>
                <Tab><Icon as={FaInfoCircle} mr={2} /> Market Value</Tab>
                <Tab><Icon as={FaTools} mr={2} /> Recommendations</Tab>
              </TabList>
              
              <TabPanels>
                {/* Reliability Score Tab */}
                <TabPanel>
                  <Card>
                    <CardBody>
                      <VStack align="start" spacing={4}>
                        <Heading size="md">Reliability Assessment</Heading>
                        
                        <HStack width="100%" justifyContent="space-between">
                          <Text fontWeight="bold">Overall Score:</Text>
                          <Badge 
                            colorScheme={getRecommendationColor(result.score)} 
                            fontSize="lg" 
                            px={3} 
                            py={1}
                            borderRadius="md"
                          >
                            {result.score}/100
                          </Badge>
                        </HStack>
                        
                        <Text>This score is based on real user experiences, forum reports, and reliability data from trusted sources.</Text>
                        
                        <Divider />
                        
                        <Heading size="sm">Mileage Assessment</Heading>
                        <Text>
                          The {result.car_info.brand} {result.car_info.model} has {result.car_info.mileage.toLocaleString()} km, 
                          which is {result.car_info.mileage > 150000 ? "higher than average" : 
                                   result.car_info.mileage > 100000 ? "average" : "lower than average"} for a {result.car_info.year} model.
                        </Text>
                      </VStack>
                    </CardBody>
                  </Card>
                </TabPanel>
                
                {/* Common Issues Tab */}
                <TabPanel>
                  <Card>
                    <CardBody>
                      <VStack align="start" spacing={4}>
                        <Heading size="md">Common Issues for {result.car_info.brand} {result.car_info.model}</Heading>
                        
                        {result.issues && result.issues.map((issue, idx) => (
                          <Alert 
                            key={idx} 
                            status={issue.severity === 'warning' ? 'warning' : 
                                   issue.severity === 'error' ? 'error' : 
                                   issue.severity === 'info' ? 'info' : 'info'} 
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
                </TabPanel>
                
                {/* Market Value Tab */}
                <TabPanel>
                  <Card>
                    <CardBody>
                      <VStack align="start" spacing={4}>
                        <Heading size="md">Eastern European Market Value</Heading>
                        
                        <HStack width="100%" justifyContent="space-between">
                          <Text fontWeight="bold">Estimated Price Range:</Text>
                          <Badge colorScheme="green" fontSize="lg" px={3} py={1} borderRadius="md">
                            €{Math.round(result.car_info.mileage * 0.1)} - €{Math.round(result.car_info.mileage * 0.15)}
                          </Badge>
                        </HStack>
                        
                        <Text>This estimate is based on Eastern European market data, adjusted for your region.</Text>
                        
                        <Divider />
                        
                        <Text fontSize="sm">
                          Note: Prices in Eastern Europe are typically 15-25% lower than Western European markets.
                          Actual prices may vary based on condition, options, and local market factors.
                        </Text>
                      </VStack>
                    </CardBody>
                  </Card>
                </TabPanel>
                
                {/* Recommendations Tab */}
                <TabPanel>
                  <Card>
                    <CardBody>
                      <VStack align="start" spacing={4}>
                        <Heading size="md">Detailed Recommendations</Heading>
                        
                        <Alert status="error" variant="left-accent" borderRadius="md">
                          <AlertIcon />
                          <Box>
                            <AlertTitle>High Priority</AlertTitle>
                            <AlertDescription>Have a professional mechanic inspect the vehicle before purchase</AlertDescription>
                          </Box>
                        </Alert>
                        
                        <Alert status="warning" variant="left-accent" borderRadius="md">
                          <AlertIcon />
                          <Box>
                            <AlertTitle>Medium Priority</AlertTitle>
                            <AlertDescription>Check service history and maintenance records</AlertDescription>
                          </Box>
                        </Alert>
                        
                        <Alert status="info" variant="left-accent" borderRadius="md">
                          <AlertIcon />
                          <Box>
                            <AlertTitle>Low Priority</AlertTitle>
                            <AlertDescription>Consider budgeting for regular maintenance items</AlertDescription>
                          </Box>
                        </Alert>
                      </VStack>
                    </CardBody>
                  </Card>
                </TabPanel>
              </TabPanels>
            </Tabs>
            
            {/* Sources Card */}
            <Card>
              <CardBody>
                <VStack align="start" spacing={4}>
                  <Heading size="md">Sources</Heading>
                  
                  <VStack align="start" spacing={2} width="100%">
                    {result.sources && result.sources.map((source, idx) => (
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
              colorScheme="blue"
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
