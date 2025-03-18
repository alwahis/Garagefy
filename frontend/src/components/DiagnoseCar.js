import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Select,
  Textarea,
  VStack,
  useToast,
  Text,
  Badge,
  Icon,
  useColorModeValue,
  HStack,
  Spacer,
  Divider,
  Progress,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  List,
  ListItem,
  ListIcon,
  Card,
  CardBody,
  Image,
  Stack,
  Tooltip,
  useBreakpointValue,
  Spinner
} from '@chakra-ui/react';
import { FaCarAlt, FaTools, FaExclamationTriangle, FaMoneyBill, FaWrench, FaCheckCircle, FaArrowLeft, FaInfoCircle, FaBolt, FaMapMarkerAlt } from 'react-icons/fa';
import config from '../config';
import axios from 'axios';
import RepairCostEstimate from './RepairCostEstimate';
import GarageFinder from './GarageFinder';

// Error Boundary Component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box p={4} borderRadius="md" bg="red.500" color="white">
          <Heading size="md">Something went wrong</Heading>
          <Text mt={2}>Please try refreshing the page or contact support if the problem persists.</Text>
        </Box>
      );
    }

    return this.props.children;
  }
}

const DiagnosticResult = ({ diagnosis, onFindGarages }) => {
  const getSeverityColor = (severity) => {
    const severityMap = {
      'low': 'green',
      'medium': 'yellow',
      'high': 'red',
      'unknown': 'gray'
    };
    return severityMap[severity?.toLowerCase()] || 'yellow';
  };

  // Extract the analysis text
  const analysisText = diagnosis.diagnosis?.analysis || '';
  
  // Extract severity
  const severityMatch = analysisText.match(/Severity Level:\*\* \*\*(HIGH|MEDIUM|LOW)/i);
  const severity = severityMatch ? severityMatch[1] : 'MEDIUM';

  // Extract repair costs section
  const costsSection = analysisText.match(/Estimated Repair Costs:([^]*?)(?=\n\n|$)/);
  const repairCosts = [];
  
  if (costsSection) {
    const costLines = costsSection[1].split('\n');
    costLines.forEach(line => {
      if (line.includes('$')) {
        const [service, cost] = line.split('$');
        if (service && cost) {
          const cleanService = service.replace(/^[-\s]*\*\*/, '').replace(/:\*\*$/, '').trim();
          const range = cost.split('-').map(n => n.replace(/[^0-9]/g, '')).join('-');
          // Convert USD to EUR (approximate conversion)
          const eurRange = range.split('-').map(n => Math.round(parseInt(n) * 0.92)).join('-');
          repairCosts.push({
            service: cleanService,
            range: eurRange
          });
        }
      }
    });
  }

  // Get references directly from the response
  const references = diagnosis.diagnosis?.references || [];

  // Split analysis text to show only the problem analysis
  const problemAnalysis = analysisText.split('TECHNICAL REFERENCES')[0];

  return (
    <Box 
      bg="darkBg.800" 
      borderWidth="1px" 
      borderColor="darkBg.600" 
      borderRadius="xl"
      overflow="hidden"
      boxShadow="xl"
      mt={6}
    >
      <Box bg="brand.500" p={6}>
        <HStack spacing={3}>
          <Icon as={FaExclamationTriangle} w={6} h={6} color="white" />
          <Heading size="md" color="white">Diagnosis Results</Heading>
        </HStack>
      </Box>

      <Box p={6}>
        <VStack spacing={6} align="stretch">
          <HStack>
            <Text fontWeight="bold" color="white">Overall Severity:</Text>
            <Badge
              colorScheme={getSeverityColor(severity)}
              fontSize="md"
              px={3}
              py={1}
              borderRadius="full"
            >
              {severity}
            </Badge>
          </HStack>

          {/* Problem Analysis */}
          <Box>
            <Text color="white" whiteSpace="pre-wrap">
              {problemAnalysis}
            </Text>
          </Box>

          {/* Estimated Repair Costs */}
          {repairCosts.length > 0 && (
            <Box 
              p={4} 
              borderWidth="1px" 
              borderRadius="md" 
              borderColor="blue.400" 
              bg="blue.900"
            >
              <HStack mb={3}>
                <Icon as={FaBolt} color="blue.300" />
                <Text fontWeight="bold" color="blue.300">Estimated Repair Costs:</Text>
              </HStack>
              <VStack align="stretch" spacing={2}>
                {repairCosts.map((cost, index) => (
                  <HStack key={index} justify="space-between" spacing={4}>
                    <Text color="white">{cost.service}</Text>
                    <Text color="blue.200" fontWeight="bold">{cost.range} EUR</Text>
                  </HStack>
                ))}
                <Text mt={2} fontSize="sm" color="gray.400">
                  * Prices are estimates and may vary based on your location and specific vehicle condition
                </Text>
              </VStack>
            </Box>
          )}

          {/* Technical References Section */}
          {references.length > 0 && (
            <Box 
              p={4} 
              borderWidth="1px" 
              borderRadius="md" 
              borderColor="green.400" 
              bg="green.900"
            >
              <HStack mb={3}>
                <Icon as={FaInfoCircle} color="green.300" />
                <Text fontWeight="bold" color="green.300">Technical References:</Text>
              </HStack>
              <List spacing={2}>
                {references.slice(0, 5).map((ref, idx) => (
                  <ListItem key={idx} color="white">
                    <HStack>
                      <Icon as={FaCheckCircle} color="green.300" size="sm" />
                      <Text>{ref}</Text>
                    </HStack>
                  </ListItem>
                ))}
                {references.length > 5 && (
                  <Text color="gray.400" fontSize="sm" mt={2}>
                    + {references.length - 5} more references available
                  </Text>
                )}
              </List>
            </Box>
          )}

          {/* Find Nearby Garages Button */}
          <Button
            colorScheme="blue"
            size="lg"
            leftIcon={<Icon as={FaMapMarkerAlt} />}
            onClick={onFindGarages}
            mt={4}
          >
            Find Nearby Garages
          </Button>
        </VStack>
      </Box>
    </Box>
  );
};

const DiagnoseCar = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [loadingProgress, setLoadingProgress] = useState(0);
  const [diagnosisResult, setDiagnosisResult] = useState(null);
  const [error, setError] = useState(null);
  const [carData, setCarData] = useState(null);
  const [isLoadingCarData, setIsLoadingCarData] = useState(true);
  const [isCached, setIsCached] = useState(false);
  const [currentScreen, setCurrentScreen] = useState('form');
  const [showGarageFinder, setShowGarageFinder] = useState(false);

  const toast = useToast();

  const fetchCarData = async (retryCount = 3) => {
    try {
      const response = await fetch(`${config.API_BASE_URL}${config.ENDPOINTS.CAR_DATA}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setCarData(data);
      setIsLoadingCarData(false);
    } catch (error) {
      console.error('Error fetching car data:', error);
      if (retryCount > 0) {
        setTimeout(() => fetchCarData(retryCount - 1), 2000);
      } else {
        toast({
          title: 'Connection Error',
          description: 'Could not connect to the server. Please check if the server is running.',
          status: 'error',
          duration: null,
          isClosable: true,
        });
        setIsLoadingCarData(false);
      }
    }
  };

  useEffect(() => {
    fetchCarData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setDiagnosisResult(null);
    setError(null);
    setIsCached(false);
    
    setLoadingProgress(0);
    const progressInterval = setInterval(() => {
      setLoadingProgress(prev => {
        const increment = Math.random() * 10;
        return Math.min(prev + increment, 90);
      });
    }, 300);

    try {
      // Create FormData object
      const formDataObj = new FormData();
      formDataObj.append('car_brand', formData.brand);
      formDataObj.append('car_model', formData.model);
      formDataObj.append('year', formData.year);
      formDataObj.append('symptoms', formData.symptoms);

      const response = await axios.post(
        `${config.API_BASE_URL}/api/diagnose`, 
        formDataObj,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        }
      );

      if (response.data && response.data.diagnosis) {
        setLoadingProgress(100);
        setDiagnosisResult(response.data);
        setIsCached(response.data.cached || false);
        setCurrentScreen('diagnosis');

        toast({
          title: "Success",
          description: "Your car's diagnosis has been generated.",
          status: "success",
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error('Error:', error);
      setError("Failed to generate diagnosis. Please try again.");
      toast({
        title: "Error",
        description: "Failed to generate diagnosis. Please try again.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      clearInterval(progressInterval);
      setIsLoading(false);
      setLoadingProgress(0);
    }
  };

  const handleFindGarages = () => {
    setShowGarageFinder(true);
    setCurrentScreen('garages');
  };

  const handleBackToForm = () => {
    setCurrentScreen('form');
    setShowGarageFinder(false);
    setDiagnosisResult(null);
  };

  const [formData, setFormData] = useState({
    brand: '',
    model: '',
    year: '',
    symptoms: ''
  });

  const cardBg = useColorModeValue('white', 'darkBg.800');
  const textColor = useColorModeValue('gray.700', 'gray.50');
  const labelColor = useColorModeValue('gray.700', 'gray.50');
  const borderColor = useColorModeValue('gray.200', 'darkBg.600');
  const formBg = useColorModeValue('white', 'darkBg.800');
  const formTextColor = useColorModeValue('gray.800', 'white');
  const formBorderColor = useColorModeValue('gray.200', 'darkBg.600');

  return (
    <Container maxW="container.lg" py={8}>
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading 
            as="h1" 
            size="xl" 
            mb={2}
            color="white"
            textAlign="center"
          >
            Car Diagnosis
          </Heading>
          <Text 
            color="gray.300" 
            textAlign="center"
          >
            Get instant AI-powered diagnosis for your car's problems
          </Text>
        </Box>

        {currentScreen === 'form' ? (
          <Box
            as="form"
            onSubmit={handleSubmit}
            bg={formBg}
            p={8}
            borderRadius="xl"
            borderWidth="1px"
            borderColor={formBorderColor}
            boxShadow="xl"
          >
            <VStack spacing={6}>
              <FormControl isRequired>
                <FormLabel color={labelColor}>Car Brand</FormLabel>
                <Select
                  name="brand"
                  value={formData.brand}
                  onChange={handleInputChange}
                  placeholder="Select car brand"
                  color={formTextColor}
                >
                  {carData && Object.keys(carData).map((brand) => (
                    <option key={brand} value={brand}>{brand}</option>
                  ))}
                </Select>
              </FormControl>

              <FormControl isRequired>
                <FormLabel color={labelColor}>Model</FormLabel>
                <Select
                  name="model"
                  value={formData.model}
                  onChange={handleInputChange}
                  placeholder="Select car model"
                  color={formTextColor}
                  isDisabled={!formData.brand}
                >
                  {formData.brand && carData && carData[formData.brand]?.models.map(model => (
                    <option key={model} value={model}>{model}</option>
                  ))}
                </Select>
              </FormControl>

              <FormControl isRequired>
                <FormLabel color={labelColor}>Year</FormLabel>
                <Input
                  name="year"
                  type="number"
                  value={formData.year}
                  onChange={handleInputChange}
                  placeholder="Enter car year"
                  color={formTextColor}
                  min="1990"
                  max="2025"
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel color={labelColor}>Symptoms</FormLabel>
                <Textarea
                  name="symptoms"
                  value={formData.symptoms}
                  onChange={handleInputChange}
                  placeholder="Describe the problems you're experiencing with your car..."
                  color={formTextColor}
                  rows={4}
                />
              </FormControl>

              <Button
                type="submit"
                colorScheme="blue"
                size="lg"
                width="full"
                isLoading={isLoading}
                loadingText="Analyzing..."
              >
                Get Diagnosis
              </Button>

              {isLoading && (
                <Box w="100%">
                  <Progress
                    value={loadingProgress}
                    size="sm"
                    colorScheme="blue"
                    isAnimated
                    hasStripe
                  />
                </Box>
              )}
            </VStack>
          </Box>
        ) : currentScreen === 'diagnosis' ? (
          <>
            <Button
              leftIcon={<Icon as={FaArrowLeft} />}
              onClick={handleBackToForm}
              variant="outline"
              colorScheme="blue"
              alignSelf="flex-start"
            >
              Back to Form
            </Button>
            <DiagnosticResult
              diagnosis={diagnosisResult}
              onFindGarages={handleFindGarages}
            />
          </>
        ) : (
          <>
            <Button
              leftIcon={<Icon as={FaArrowLeft} />}
              onClick={() => setCurrentScreen('diagnosis')}
              variant="outline"
              colorScheme="blue"
              alignSelf="flex-start"
            >
              Back to Diagnosis
            </Button>
            <GarageFinder />
          </>
        )}
      </VStack>
    </Container>
  );
};

export default DiagnoseCar;
