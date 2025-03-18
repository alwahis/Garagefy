import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Textarea,
  VStack,
  useToast,
  Text,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Container,
  Heading,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Icon,
  Flex,
  Badge,
  SimpleGrid,
  useColorModeValue,
  Spinner,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Progress,
  Grid,
  GridItem,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  RadioGroup,
  Radio,
  Stack,
  Link
} from '@chakra-ui/react';
import { 
  FaCarAlt, 
  FaCalendarAlt, 
  FaExclamationTriangle, 
  FaGasPump, 
  FaCogs,
  FaTachometerAlt,
  FaCheckCircle,
  FaExclamationCircle,
  FaMapMarkerAlt,
  FaPhoneAlt,
  FaClock,
  FaTools,
  FaCalendarCheck
} from 'react-icons/fa';
import config from '../config';
import axios from 'axios';
import BookingModal from './BookingModal';

const DiagnosisForm = () => {
  const [carBrands, setCarBrands] = useState({});
  const [selectedBrand, setSelectedBrand] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [year, setYear] = useState('');
  const [fuelType, setFuelType] = useState('');
  const [transmissionType, setTransmissionType] = useState('');
  const [mileage, setMileage] = useState('');
  const [symptoms, setSymptoms] = useState('');
  const [loading, setLoading] = useState(false);
  const [diagnosis, setDiagnosis] = useState(null);
  const [error, setError] = useState(null);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [recommendedGarages, setRecommendedGarages] = useState([]);
  const [garagesLoading, setGaragesLoading] = useState(false);
  const [bookingGarage, setBookingGarage] = useState(null);
  const [isBookingModalOpen, setIsBookingModalOpen] = useState(false);
  
  const toast = useToast();

  // Define color mode values outside of conditional statements and callbacks
  const cardBg = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('transparent', 'gray.600');
  const headerBg = useColorModeValue('brand.600', 'brand.700');
  const textColor = useColorModeValue('gray.800', 'white');
  const mutedTextColor = useColorModeValue('gray.600', 'gray.400');
  const buttonColorScheme = 'brand';
  const issueCardBg = useColorModeValue('white', 'gray.700');
  const issueCardBorder = useColorModeValue('gray.200', 'gray.600');
  const garageCardBg = useColorModeValue('white', 'gray.700');
  const garageCardBorder = useColorModeValue('gray.200', 'gray.600');

  const fuelTypes = [
    { id: 'petrol', name: 'Petrol' },
    { id: 'diesel', name: 'Diesel' },
    { id: 'electric', name: 'Electric' },
    { id: 'hybrid', name: 'Hybrid' },
    { id: 'plug_in_hybrid', name: 'Plug-in Hybrid' },
    { id: 'lpg', name: 'LPG' },
    { id: 'cng', name: 'CNG' }
  ];

  const transmissionTypes = [
    { id: 'manual', name: 'Manual' },
    { id: 'automatic', name: 'Automatic' },
    { id: 'semi_automatic', name: 'Semi-Automatic' },
    { id: 'cvt', name: 'CVT' },
    { id: 'dual_clutch', name: 'Dual Clutch' }
  ];

  const fetchCarData = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}${config.ENDPOINTS.CAR_DATA}`);
      if (!response.ok) throw new Error('Failed to fetch car data');
      const data = await response.json();
      setCarBrands(data);
    } catch (error) {
      console.error('Error fetching car data:', error);
      toast({
        title: 'Error',
        description: 'Failed to load car brands and models',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  useEffect(() => {
    fetchCarData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setDiagnosis(null);
    setSelectedIssue(null);
    setRecommendedGarages([]);
    
    console.log('DiagnosisForm handleSubmit called');
    console.log('Form values:', { 
      selectedBrand, 
      selectedModel, 
      year, 
      symptoms, 
      fuelType, 
      transmissionType, 
      mileage 
    });

    // Validation
    if (!selectedBrand || !selectedModel || !year || !symptoms) {
      toast({
        title: 'Missing Information',
        description: 'Please fill in all required fields',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      setLoading(false);
      return;
    }

    try {
      // Create a JSON payload instead of FormData
      const payload = {
        car_brand: selectedBrand,
        model: selectedModel,
        year: parseInt(year),
        symptoms: symptoms
      };
      
      // Adding new fields if they exist
      if (fuelType) payload.fuel_type = fuelType;
      if (transmissionType) payload.transmission_type = transmissionType;
      if (mileage) payload.mileage = parseInt(mileage);

      console.log('Sending diagnosis request with payload:', payload);
      const requestUrl = `${config.API_BASE_URL}${config.ENDPOINTS.DIAGNOSE}`;
      console.log('Request URL:', requestUrl);

      console.log('Making fetch request with the following options:');
      console.log('Method: POST');
      console.log('Headers:', { 'Content-Type': 'application/json' });
      console.log('Body:', JSON.stringify(payload));

      const response = await fetch(requestUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
        body: JSON.stringify(payload),
        credentials: 'same-origin',
      });

      console.log('Response status:', response.status);
      console.log('Response status text:', response.statusText);
      console.log('Response headers:', Object.fromEntries([...response.headers]));

      if (!response.ok) {
        console.error('Diagnosis API error:', response.status, response.statusText);
        const errorText = await response.text();
        console.error('Error response:', errorText);
        
        // Show a more detailed error message to the user
        toast({
          title: 'Diagnosis Failed',
          description: `Error ${response.status}: ${response.statusText || 'Unknown error'}. ${errorText || ''}`,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
        
        throw new Error(`Failed to get diagnosis: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Diagnosis API response:', data);
      
      // Process the diagnosis data to extract the possible issues
      const result = data.diagnosis;
      
      // Create mock issues with probabilities if not provided by API
      if (!result.issues) {
        // Extract issues from analysis text (for demo purposes)
        const analysisText = result.analysis;
        const possibleIssues = extractIssuesFromAnalysis(analysisText);
        result.issues = possibleIssues;
      }
      
      setDiagnosis(result);
      
      // Scroll to results
      setTimeout(() => {
        if (document.getElementById('diagnosis-results')) {
          document.getElementById('diagnosis-results').scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    } catch (error) {
      console.error('Error in diagnosis submission:', error);
      
      toast({
        title: 'Diagnosis Failed',
        description: error.message || 'An unexpected error occurred. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      
      setLoading(false);
    }
  };

  // Function to extract issues from analysis text if the API doesn't provide structured issues
  const extractIssuesFromAnalysis = (analysisText) => {
    // This is a simplified extraction logic for demo purposes
    // In a real application, you might want a more sophisticated parsing method
    
    // Sample issues that might be found in car diagnostics
    const commonIssues = [
      { name: 'Faulty brake pads', system: 'Braking System' },
      { name: 'ABS sensor failure', system: 'Braking System' },
      { name: 'Low oil pressure', system: 'Engine' },
      { name: 'Worn spark plugs', system: 'Engine' },
      { name: 'Damaged fuel injectors', system: 'Fuel System' },
      { name: 'Bad fuel pump', system: 'Fuel System' },
      { name: 'Failing alternator', system: 'Electrical System' },
      { name: 'Dead battery', system: 'Electrical System' },
      { name: 'Slipping transmission', system: 'Transmission' },
      { name: 'Worn clutch', system: 'Transmission' },
      { name: 'Leaking shock absorbers', system: 'Suspension' },
      { name: 'Worn ball joints', system: 'Suspension' },
      { name: 'Bad oxygen sensor', system: 'Emissions System' },
      { name: 'Faulty catalytic converter', system: 'Emissions System' },
      { name: 'Damaged radiator', system: 'Cooling System' },
      { name: 'Failed water pump', system: 'Cooling System' }
    ];
    
    // Select 2-4 random issues that might be relevant based on text matching
    const text = analysisText.toLowerCase();
    const matchingIssues = commonIssues.filter(issue => 
      text.includes(issue.name.toLowerCase()) || 
      text.includes(issue.system.toLowerCase())
    );
    
    // If we don't have enough matching issues, add some random ones
    let possibleIssues = [...matchingIssues];
    while (possibleIssues.length < 3) {
      const randomIndex = Math.floor(Math.random() * commonIssues.length);
      const randomIssue = commonIssues[randomIndex];
      if (!possibleIssues.some(issue => issue.name === randomIssue.name)) {
        possibleIssues.push(randomIssue);
      }
    }
    
    // Trim to at most 3 issues
    possibleIssues = possibleIssues.slice(0, 3);
    
    // Assign random probabilities that sum to 100
    let remainingProbability = 100;
    return possibleIssues.map((issue, index) => {
      // For the last item, assign the remaining probability
      if (index === possibleIssues.length - 1) {
        return {
          ...issue,
          probability: remainingProbability
        };
      }
      
      // Otherwise, assign a random probability between 20 and remainingProbability - 10
      // (to ensure each issue has at least 10% probability)
      const maxProb = remainingProbability - (10 * (possibleIssues.length - 1 - index));
      const minProb = Math.min(20, maxProb);
      const probability = Math.floor(Math.random() * (maxProb - minProb + 1)) + minProb;
      
      remainingProbability -= probability;
      
      return {
        ...issue,
        probability
      };
    }).sort((a, b) => b.probability - a.probability); // Sort by probability descending
  };

  const handleIssueSelect = async (issue) => {
    setSelectedIssue(issue);
    setGaragesLoading(true);
    
    try {
      // Get user's location
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          try {
            const { latitude, longitude } = position.coords;
            
            // Fetch garages that can handle this issue
            const response = await axios.get(
              `${config.API_BASE_URL}${config.ENDPOINTS.GARAGES}?lat=${latitude}&lng=${longitude}&service=${encodeURIComponent(issue.system)}`
            );
            
            if (response.data && Array.isArray(response.data)) {
              setRecommendedGarages(response.data);
            } else {
              setRecommendedGarages([]);
              toast({
                title: 'No garages found',
                description: 'We couldn\'t find garages that handle this issue in your area.',
                status: 'info',
                duration: 5000,
                isClosable: true,
              });
            }
          } catch (error) {
            console.error('Error fetching garages:', error);
            toast({
              title: 'Error',
              description: 'Failed to fetch garages. Please try again.',
              status: 'error',
              duration: 5000,
              isClosable: true,
            });
            setRecommendedGarages([]);
          } finally {
            setGaragesLoading(false);
          }
        },
        (error) => {
          console.error('Geolocation error:', error);
          toast({
            title: 'Location access denied',
            description: 'Please enable location access to find garages near you.',
            status: 'error',
            duration: 5000,
            isClosable: true,
          });
          setGaragesLoading(false);
        }
      );
    } catch (error) {
      console.error('Error in geolocation:', error);
      setGaragesLoading(false);
    }
  };

  const handleBookAppointment = (garage) => {
    setBookingGarage(garage);
    setIsBookingModalOpen(true);
  };

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Box 
          p={6} 
          borderRadius="lg" 
          bg="white" 
          boxShadow="md"
          bgGradient="linear(to-r, brand.600, secondary.600)"
          color="white"
        >
          <VStack spacing={4} align="stretch">
            <Heading size="xl">Car Symptom Diagnosis</Heading>
            <Text fontSize="lg">
              Analyze your car's symptoms for a quick and accurate diagnosis
            </Text>
          </VStack>
        </Box>

        <Card bg={cardBg} borderColor={borderColor} shadow="md">
          <CardHeader>
            <Heading size="md">Vehicle Information</Heading>
          </CardHeader>
          <CardBody>
            <form onSubmit={handleSubmit}>
              <VStack spacing={6} align="stretch">
                <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                  <FormControl isRequired>
                    <FormLabel display="flex" alignItems="center">
                      <Icon as={FaCarAlt} mr={2} color="brand.600" />
                      Car Brand
                    </FormLabel>
                    <Select
                      placeholder="Select car brand"
                      value={selectedBrand}
                      onChange={(e) => {
                        setSelectedBrand(e.target.value);
                        setSelectedModel('');
                      }}
                    >
                      {Object.keys(carBrands).map((brand) => (
                        <option key={brand} value={brand}>
                          {brand}
                        </option>
                      ))}
                    </Select>
                  </FormControl>

                  <FormControl isRequired>
                    <FormLabel display="flex" alignItems="center">
                      <Icon as={FaCarAlt} mr={2} color="brand.600" />
                      Model
                    </FormLabel>
                    <Select
                      placeholder="Select model"
                      value={selectedModel}
                      onChange={(e) => setSelectedModel(e.target.value)}
                      isDisabled={!selectedBrand}
                    >
                      {selectedBrand &&
                        carBrands[selectedBrand]?.models.map((model) => (
                          <option key={model} value={model}>
                            {model}
                          </option>
                        ))}
                    </Select>
                  </FormControl>

                  <FormControl isRequired>
                    <FormLabel display="flex" alignItems="center">
                      <Icon as={FaCalendarAlt} mr={2} color="brand.600" />
                      Year
                    </FormLabel>
                    <Input
                      type="number"
                      value={year}
                      onChange={(e) => setYear(e.target.value)}
                      placeholder="Enter car year"
                      min="1900"
                      max={new Date().getFullYear() + 1}
                    />
                  </FormControl>
                </SimpleGrid>

                <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                  <FormControl>
                    <FormLabel display="flex" alignItems="center">
                      <Icon as={FaGasPump} mr={2} color="brand.600" />
                      Fuel Type
                    </FormLabel>
                    <Select
                      placeholder="Select fuel type"
                      value={fuelType}
                      onChange={(e) => setFuelType(e.target.value)}
                    >
                      {fuelTypes.map((type) => (
                        <option key={type.id} value={type.id}>
                          {type.name}
                        </option>
                      ))}
                    </Select>
                  </FormControl>

                  <FormControl>
                    <FormLabel display="flex" alignItems="center">
                      <Icon as={FaCogs} mr={2} color="brand.600" />
                      Transmission
                    </FormLabel>
                    <Select
                      placeholder="Select transmission"
                      value={transmissionType}
                      onChange={(e) => setTransmissionType(e.target.value)}
                    >
                      {transmissionTypes.map((type) => (
                        <option key={type.id} value={type.id}>
                          {type.name}
                        </option>
                      ))}
                    </Select>
                  </FormControl>

                  <FormControl>
                    <FormLabel display="flex" alignItems="center">
                      <Icon as={FaTachometerAlt} mr={2} color="brand.600" />
                      Mileage
                    </FormLabel>
                    <Input
                      type="number"
                      value={mileage}
                      onChange={(e) => setMileage(e.target.value)}
                      placeholder="Enter mileage in km"
                      min="0"
                    />
                  </FormControl>
                </SimpleGrid>

                <FormControl isRequired>
                  <FormLabel display="flex" alignItems="center">
                    <Icon as={FaExclamationTriangle} mr={2} color="brand.600" />
                    Symptoms
                  </FormLabel>
                  <Textarea
                    value={symptoms}
                    onChange={(e) => setSymptoms(e.target.value)}
                    placeholder="Describe the problems you're experiencing with your car in detail. For example: 'My car makes a grinding noise when I brake and the steering wheel vibrates.'"
                    rows={5}
                  />
                </FormControl>

                <Button
                  type="submit"
                  colorScheme={buttonColorScheme}
                  size="lg"
                  width="full"
                  isLoading={loading}
                  loadingText="Analyzing..."
                  bg="accent.500"
                  _hover={{ bg: 'accent.600' }}
                >
                  Get Diagnosis
                </Button>
              </VStack>
            </form>
          </CardBody>
        </Card>

        {error && (
          <Alert status="error" borderRadius="md">
            <AlertIcon />
            <AlertTitle mr={2}>Error!</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {loading && (
          <Flex justify="center" py={10}>
            <VStack>
              <Spinner size="xl" color="accent.500" thickness="4px" />
              <Text mt={4} color="gray.600">Analyzing your car's symptoms...</Text>
            </VStack>
          </Flex>
        )}

        {diagnosis && (
          <Card
            id="diagnosis-results"
            bg={cardBg}
            shadow="md"
            borderColor={borderColor}
            mt={8}
          >
            <CardHeader 
              bg={headerBg} 
              borderBottomWidth="1px" 
              borderColor={borderColor}
            >
              <Heading size="md" color={textColor}>Diagnosis Results</Heading>
            </CardHeader>
            <CardBody>
              <VStack align="stretch" spacing={6}>
                <Box>
                  <Text fontWeight="bold" mb={2} color={mutedTextColor}>Vehicle Information:</Text>
                  <Flex align="center">
                    <Badge colorScheme="brand" fontSize="md" px={2} py={1}>
                      {diagnosis.vehicle_info.year} {diagnosis.vehicle_info.brand}{' '}
                      {diagnosis.vehicle_info.model}
                    </Badge>
                  </Flex>
                </Box>
                
                <Divider />
                
                <Box>
                  <Text fontWeight="bold" mb={2} color={mutedTextColor}>Symptoms Reported:</Text>
                  <Text bg="white" p={3} borderRadius="md" borderWidth="1px" borderColor="transparent">
                    {diagnosis.symptoms}
                  </Text>
                </Box>
                
                <Divider />
                
                <Box>
                  <Text fontWeight="bold" mb={4} color={mutedTextColor}>Possible Issues:</Text>
                  <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                    {diagnosis.issues && diagnosis.issues.map((issue, index) => (
                      <Card 
                        key={index} 
                        variant="outline" 
                        cursor="pointer"
                        onClick={() => handleIssueSelect(issue)}
                        borderColor={selectedIssue === issue ? "brand.500" : issueCardBorder}
                        boxShadow={selectedIssue === issue ? "md" : "sm"}
                        _hover={{ boxShadow: "md" }}
                        transition="all 0.2s"
                        height="100%"
                        bg={issueCardBg}
                      >
                        <CardBody>
                          <VStack align="stretch" spacing={4}>
                            <Heading size="sm">{issue.name}</Heading>
                            <Text color={mutedTextColor} fontSize="sm">{issue.system}</Text>
                            <Box>
                              <Text fontSize="sm" mb={1}>Probability: {issue.probability}%</Text>
                              <Progress 
                                value={issue.probability} 
                                colorScheme={
                                  issue.probability > 70 ? "red" : 
                                  issue.probability > 40 ? "yellow" : 
                                  "green"
                                }
                                borderRadius="md"
                                size="sm"
                              />
                            </Box>
                            <Button 
                              size="sm" 
                              colorScheme={buttonColorScheme}
                              onClick={(e) => {
                                e.stopPropagation();
                                handleIssueSelect(issue);
                              }}
                            >
                              Find Garages
                            </Button>
                          </VStack>
                        </CardBody>
                      </Card>
                    ))}
                  </SimpleGrid>
                </Box>
                
                <Divider />
                
                <Box>
                  <Text fontWeight="bold" mb={2} color={mutedTextColor}>Analysis:</Text>
                  <Text 
                    whiteSpace="pre-wrap" 
                    bg="white" 
                    p={4} 
                    borderRadius="md" 
                    borderWidth="1px" 
                    borderColor="transparent"
                  >
                    {diagnosis.analysis}
                  </Text>
                </Box>
                
                {selectedIssue && (
                  <Box mt={6}>
                    <Heading size="md" mb={4}>Recommended Garages for {selectedIssue.name}</Heading>
                    
                    {garagesLoading ? (
                      <Flex justify="center" py={10}>
                        <VStack>
                          <Spinner size="xl" color="accent.500" thickness="4px" />
                          <Text mt={4} color="gray.600">Finding garages near you...</Text>
                        </VStack>
                      </Flex>
                    ) : recommendedGarages.length > 0 ? (
                      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
                        {recommendedGarages.map((garage) => (
                          <Card 
                            key={garage.id} 
                            variant="outline" 
                            borderColor={garageCardBorder}
                            transition="all 0.3s"
                            _hover={{ transform: 'translateY(-5px)', shadow: 'lg' }}
                            bg={garageCardBg}
                          >
                            <CardHeader 
                              bg={headerBg} 
                              borderBottomWidth="1px" 
                              borderColor={borderColor}
                              pb={3}
                            >
                              <Heading size="md" noOfLines={1}>{garage.name}</Heading>
                              {garage.distance && (
                                <Flex align="center" mt={2}>
                                  <Icon as={FaMapMarkerAlt} color="secondary.500" mr={1} />
                                  <Text fontWeight="medium" color="secondary.600">
                                    {garage.distance.toFixed(1)} km away
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
                                  <Text>{garage.address}</Text>
                                </Flex>
                                
                                <Flex align="center">
                                  <Icon as={FaPhoneAlt} color="secondary.500" mr={2} />
                                  <Link href={`tel:${garage.phone}`} color="blue.600" fontWeight="medium">
                                    {garage.phone}
                                  </Link>
                                </Flex>
                                
                                <Flex align="flex-start">
                                  <Icon as={FaClock} color="secondary.500" mt={1} mr={2} />
                                  <Text>{garage.opening_hours}</Text>
                                </Flex>
                                
                                <Box>
                                  <Text fontWeight="bold" mb={2} display="flex" alignItems="center">
                                    <Icon as={FaTools} mr={2} color="accent.500" />
                                    Services
                                  </Text>
                                  <Text color={mutedTextColor}>
                                    {Array.isArray(garage.services) 
                                      ? garage.services.join(', ')
                                      : typeof garage.services === 'string'
                                        ? garage.services
                                        : 'Various services available'}
                                  </Text>
                                </Box>
                                
                                <Button 
                                  colorScheme={buttonColorScheme} 
                                  leftIcon={<Icon as={FaCalendarCheck} />}
                                  onClick={() => handleBookAppointment(garage)}
                                >
                                  Book Appointment
                                </Button>
                              </VStack>
                            </CardBody>
                          </Card>
                        ))}
                      </SimpleGrid>
                    ) : (
                      <Alert status="info" borderRadius="md">
                        <AlertIcon />
                        <AlertTitle mr={2}>No garages found</AlertTitle>
                        <AlertDescription>We couldn't find any garages in your area that specialize in this issue.</AlertDescription>
                      </Alert>
                    )}
                  </Box>
                )}
                
                <Alert status="info" borderRadius="md">
                  <AlertIcon />
                  <Text fontSize="sm">{diagnosis.disclaimer}</Text>
                </Alert>
              </VStack>
            </CardBody>
          </Card>
        )}
      </VStack>
      
      {bookingGarage && (
        <BookingModal 
          isOpen={isBookingModalOpen} 
          onClose={() => setIsBookingModalOpen(false)} 
          garage={bookingGarage} 
          selectedIssue={selectedIssue}
        />
      )}
    </Container>
  );
};

export default DiagnosisForm;
