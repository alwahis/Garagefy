import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Heading,
  VStack,
  Button,
  Text,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  SimpleGrid,
  Card,
  CardBody,
  CardHeader,
  Icon,
  Flex,
  Divider,
  Alert,
  AlertIcon,
  useColorModeValue,
  Checkbox,
  CheckboxGroup,
  Stack,
  List,
  ListItem,
  ListIcon,
  FormHelperText,
  Select,
  Spinner,
  Badge,
  Progress,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  useToast
} from '@chakra-ui/react';
import { 
  FaCarAlt, 
  FaCalendarAlt, 
  FaClipboardCheck, 
  FaCheckCircle, 
  FaExclamationTriangle,
  FaTools,
  FaCarCrash,
  FaHistory,
  FaInfoCircle,
  FaGasPump,
  FaCog,
  FaEuroSign,
  FaChartLine,
  FaShieldAlt,
  FaExclamationCircle,
  FaRegThumbsUp,
  FaRegThumbsDown
} from 'react-icons/fa';

// Form component
const VehicleForm = ({ formData, setFormData, formErrors, handleSubmit, hasVin, options, loadingOptions }) => {
  const { vin, make, model, year, mileage, additionalInfo, fuelType, transmissionType, condition } = formData;
  
  console.log('VehicleForm options:', options);
  
  return (
    <form onSubmit={handleSubmit}>
      <VStack spacing={6} align="stretch">
        <FormControl>
          <FormLabel display="flex" alignItems="center">
            <Icon as={FaCarAlt} mr={2} color="accent.500" />
            VIN (Vehicle Identification Number)
          </FormLabel>
          <Input
            value={vin}
            onChange={(e) => setFormData({...formData, vin: e.target.value})}
            placeholder="e.g. 1HGCM82633A123456"
          />
          <FormHelperText>
            If you provide a VIN, the other vehicle details become optional.
          </FormHelperText>
        </FormControl>

        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
          <FormControl isRequired={!hasVin} isInvalid={formErrors.make}>
            <FormLabel display="flex" alignItems="center">
              <Icon as={FaCarAlt} mr={2} color="accent.500" />
              Make {!hasVin && <Text color="red.500" ml={1}>*</Text>}
            </FormLabel>
            <Select
              value={make}
              onChange={(e) => setFormData({...formData, make: e.target.value})}
              placeholder="Select make"
              isDisabled={loadingOptions}
            >
              {options.makes.map((make, index) => (
                <option key={index} value={make}>{make}</option>
              ))}
            </Select>
            {formErrors.make && (
              <FormHelperText color="red.500">{formErrors.make}</FormHelperText>
            )}
          </FormControl>

          <FormControl isRequired={!hasVin} isInvalid={formErrors.model}>
            <FormLabel display="flex" alignItems="center">
              <Icon as={FaCarAlt} mr={2} color="accent.500" />
              Model {!hasVin && <Text color="red.500" ml={1}>*</Text>}
            </FormLabel>
            <Select
              value={model}
              onChange={(e) => setFormData({...formData, model: e.target.value})}
              placeholder="Select model"
              isDisabled={loadingOptions}
            >
              {options.models.map((model, index) => (
                <option key={index} value={model}>{model}</option>
              ))}
            </Select>
            {formErrors.model && (
              <FormHelperText color="red.500">{formErrors.model}</FormHelperText>
            )}
          </FormControl>

          <FormControl isRequired={!hasVin} isInvalid={formErrors.year}>
            <FormLabel display="flex" alignItems="center">
              <Icon as={FaCalendarAlt} mr={2} color="accent.500" />
              Year {!hasVin && <Text color="red.500" ml={1}>*</Text>}
            </FormLabel>
            <Select
              value={year}
              onChange={(e) => setFormData({...formData, year: e.target.value})}
              placeholder="Select year"
              isDisabled={loadingOptions}
            >
              {options.years.map((year, index) => (
                <option key={index} value={year}>{year}</option>
              ))}
            </Select>
            {formErrors.year && (
              <FormHelperText color="red.500">{formErrors.year}</FormHelperText>
            )}
          </FormControl>
        </SimpleGrid>

        <FormControl isRequired={!hasVin} isInvalid={formErrors.mileage}>
          <FormLabel display="flex" alignItems="center">
            <Icon as={FaHistory} mr={2} color="accent.500" />
            Mileage {!hasVin && <Text color="red.500" ml={1}>*</Text>}
          </FormLabel>
          <Input
            type="number"
            value={mileage}
            onChange={(e) => setFormData({...formData, mileage: e.target.value})}
            placeholder="e.g. 45000"
          />
          {formErrors.mileage && (
            <FormHelperText color="red.500">{formErrors.mileage}</FormHelperText>
          )}
        </FormControl>

        <FormControl isRequired={!hasVin} isInvalid={formErrors.fuelType}>
          <FormLabel display="flex" alignItems="center">
            <Icon as={FaGasPump} mr={2} color="accent.500" />
            Fuel Type {!hasVin && <Text color="red.500" ml={1}>*</Text>}
          </FormLabel>
          <Select
            value={fuelType}
            onChange={(e) => setFormData({...formData, fuelType: e.target.value})}
            placeholder="Select fuel type"
            isDisabled={loadingOptions}
          >
            {Array.isArray(options.fuelTypes) && options.fuelTypes.map((fuel, index) => (
              <option key={index} value={fuel.id}>{fuel.name}</option>
            ))}
          </Select>
          {formErrors.fuelType && (
            <FormHelperText color="red.500">{formErrors.fuelType}</FormHelperText>
          )}
        </FormControl>

        <FormControl isRequired={!hasVin} isInvalid={formErrors.transmissionType}>
          <FormLabel display="flex" alignItems="center">
            <Icon as={FaCog} mr={2} color="accent.500" />
            Transmission Type {!hasVin && <Text color="red.500" ml={1}>*</Text>}
          </FormLabel>
          <Select
            value={transmissionType}
            onChange={(e) => setFormData({...formData, transmissionType: e.target.value})}
            placeholder="Select transmission type"
            isDisabled={loadingOptions}
          >
            {Array.isArray(options.transmissionTypes) && options.transmissionTypes.map((transmission, index) => (
              <option key={index} value={transmission.id}>{transmission.name}</option>
            ))}
          </Select>
          {formErrors.transmissionType && (
            <FormHelperText color="red.500">{formErrors.transmissionType}</FormHelperText>
          )}
        </FormControl>

        <FormControl>
          <FormLabel display="flex" alignItems="center">
            <Icon as={FaInfoCircle} mr={2} color="accent.500" />
            Additional Information
          </FormLabel>
          <Textarea
            value={additionalInfo}
            onChange={(e) => setFormData({...formData, additionalInfo: e.target.value})}
            placeholder="Please provide any additional information about the vehicle that might be helpful (e.g., known issues, accident history, etc.)"
            rows={4}
          />
        </FormControl>

        <FormControl>
          <FormLabel display="flex" alignItems="center">
            <Icon as={FaShieldAlt} mr={2} color="accent.500" />
            Condition
          </FormLabel>
          <Select
            value={condition}
            onChange={(e) => setFormData({...formData, condition: e.target.value})}
            placeholder="Select condition"
          >
            <option value="Excellent">Excellent</option>
            <option value="Good">Good</option>
            <option value="Fair">Fair</option>
            <option value="Poor">Poor</option>
          </Select>
        </FormControl>

        <Divider />

        <FormControl>
          <FormLabel display="flex" alignItems="center" mb={4}>
            <Icon as={FaClipboardCheck} mr={2} color="accent.500" />
            Pre-purchase Checklist
          </FormLabel>
          <CheckboxGroup colorScheme="accent">
            <Stack spacing={3}>
              <Checkbox>I have personally inspected the vehicle</Checkbox>
              <Checkbox>I have taken the car for a test drive</Checkbox>
              <Checkbox>I have checked the vehicle history report</Checkbox>
              <Checkbox>I have verified the title status</Checkbox>
              <Checkbox>I have had a professional mechanic inspect the vehicle</Checkbox>
            </Stack>
          </CheckboxGroup>
        </FormControl>

        <Button
          type="submit"
          colorScheme="accent"
          size="lg"
          width="full"
          bg="accent.500"
          _hover={{ bg: 'accent.600' }}
        >
          Check Vehicle
        </Button>
      </VStack>
    </form>
  );
};

// Results component
const VehicleResults = ({ formData, resetForm, checkResult }) => {
  const { vin, make, model, year, mileage, fuelType, transmissionType } = formData;
  
  if (!checkResult) {
    return (
      <VStack spacing={6} align="stretch">
        <Alert status="error" borderRadius="md">
          <AlertIcon />
          No data available. Please try again.
        </Alert>
        <Button
          colorScheme="accent"
          size="lg"
          width="full"
          onClick={resetForm}
          bg="accent.500"
          _hover={{ bg: 'accent.600' }}
        >
          Check Another Vehicle
        </Button>
      </VStack>
    );
  }
  
  const { analysis, market_data, recommendations } = checkResult;
  
  return (
    <VStack spacing={6} align="stretch">
      <Box>
        <Heading size="sm" mb={3} color="gray.600">Vehicle Details</Heading>
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
          {vin && (
            <Box>
              <Text fontWeight="bold">VIN:</Text>
              <Text>{vin}</Text>
            </Box>
          )}
          {make && (
            <Box>
              <Text fontWeight="bold">Make:</Text>
              <Text>{make}</Text>
            </Box>
          )}
          {model && (
            <Box>
              <Text fontWeight="bold">Model:</Text>
              <Text>{model}</Text>
            </Box>
          )}
          {year && (
            <Box>
              <Text fontWeight="bold">Year:</Text>
              <Text>{year}</Text>
            </Box>
          )}
          {mileage && (
            <Box>
              <Text fontWeight="bold">Mileage:</Text>
              <Text>{mileage} km</Text>
            </Box>
          )}
          {fuelType && (
            <Box>
              <Text fontWeight="bold">Fuel Type:</Text>
              <Text>{fuelType}</Text>
            </Box>
          )}
          {transmissionType && (
            <Box>
              <Text fontWeight="bold">Transmission:</Text>
              <Text>{transmissionType}</Text>
            </Box>
          )}
        </SimpleGrid>
      </Box>

      <Divider />

      <Tabs isFitted variant="enclosed" colorScheme="accent">
        <TabList>
          <Tab>Reliability</Tab>
          <Tab>Common Issues</Tab>
          <Tab>Pricing</Tab>
          <Tab>Recommendations</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <VStack spacing={4} align="stretch">
              <Box>
                <Heading size="sm" mb={3} color="gray.600">Reliability Score</Heading>
                <Flex align="center" mb={2}>
                  <Progress 
                    value={analysis.reliability_score.score} 
                    max={100} 
                    colorScheme={analysis.reliability_score.score > 75 ? "green" : analysis.reliability_score.score > 50 ? "yellow" : "red"}
                    flex="1"
                    borderRadius="md"
                    height="12px"
                    mr={4}
                  />
                  <Text fontWeight="bold">{analysis.reliability_score.score}/100</Text>
                </Flex>
                <Badge 
                  colorScheme={
                    analysis.reliability_score.rating === "Excellent" ? "green" : 
                    analysis.reliability_score.rating === "Very Good" ? "green" : 
                    analysis.reliability_score.rating === "Good" ? "blue" : 
                    analysis.reliability_score.rating === "Fair" ? "yellow" : "red"
                  }
                  fontSize="md"
                  px={2}
                  py={1}
                  borderRadius="md"
                >
                  {analysis.reliability_score.rating}
                </Badge>
              </Box>

              <Box>
                <Heading size="sm" mb={3} color="gray.600">Mileage Assessment</Heading>
                <Alert 
                  status={
                    analysis.mileage_assessment.category === "low" ? "success" : 
                    analysis.mileage_assessment.category === "average" ? "info" : 
                    analysis.mileage_assessment.category === "high" ? "warning" : "error"
                  }
                  borderRadius="md" 
                  mb={3}
                >
                  <AlertIcon />
                  {analysis.mileage_assessment.condition} condition - {analysis.mileage_assessment.range}
                </Alert>
                <Text>{analysis.mileage_assessment.description}</Text>
                <Text mt={2}>
                  <Text as="span" fontWeight="bold">Annual average:</Text> {analysis.mileage_assessment.annual_average} km/year
                </Text>
              </Box>
            </VStack>
          </TabPanel>

          <TabPanel>
            <Box>
              <Heading size="sm" mb={3} color="gray.600">Known Issues</Heading>
              {analysis.common_issues.length > 0 ? (
                <List spacing={3}>
                  {analysis.common_issues.map((issue, index) => (
                    <ListItem key={index}>
                      <ListIcon 
                        as={issue.includes("No specific data") ? FaInfoCircle : FaExclamationTriangle} 
                        color={issue.includes("No specific data") ? "blue.500" : "orange.500"} 
                      />
                      {issue}
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Alert status="info" borderRadius="md">
                  <AlertIcon />
                  No common issues reported for this vehicle
                </Alert>
              )}
            </Box>
          </TabPanel>

          <TabPanel>
            <VStack spacing={4} align="stretch">
              <Box>
                <Heading size="sm" mb={3} color="gray.600">Market Value</Heading>
                <Stat>
                  <StatLabel>Estimated value in {market_data.market_region}</StatLabel>
                  <StatNumber>
                    <Icon as={FaEuroSign} /> {market_data.price_estimation.estimated_price.toLocaleString()}
                  </StatNumber>
                  <StatHelpText>
                    Range: {market_data.price_estimation.price_range.low.toLocaleString()} - {market_data.price_estimation.price_range.high.toLocaleString()} {market_data.price_estimation.currency}
                  </StatHelpText>
                </Stat>
              </Box>

              <Box>
                <Heading size="sm" mb={3} color="gray.600">Price Factors</Heading>
                <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                  <Box>
                    <Text fontWeight="bold">Age:</Text>
                    <Flex align="center">
                      <Icon 
                        as={market_data.price_estimation.factors.age_factor >= 0.8 ? FaRegThumbsUp : FaRegThumbsDown} 
                        color={market_data.price_estimation.factors.age_factor >= 0.8 ? "green.500" : "red.500"} 
                        mr={2} 
                      />
                      <Text>Factor: {market_data.price_estimation.factors.age_factor.toFixed(2)}</Text>
                    </Flex>
                  </Box>
                  <Box>
                    <Text fontWeight="bold">Mileage:</Text>
                    <Flex align="center">
                      <Icon 
                        as={market_data.price_estimation.factors.mileage_factor >= 0.9 ? FaRegThumbsUp : FaRegThumbsDown} 
                        color={market_data.price_estimation.factors.mileage_factor >= 0.9 ? "green.500" : "red.500"} 
                        mr={2} 
                      />
                      <Text>Factor: {market_data.price_estimation.factors.mileage_factor.toFixed(2)}</Text>
                    </Flex>
                  </Box>
                  <Box>
                    <Text fontWeight="bold">Fuel Type:</Text>
                    <Flex align="center">
                      <Icon 
                        as={market_data.price_estimation.factors.fuel_factor >= 1.0 ? FaRegThumbsUp : FaRegThumbsDown} 
                        color={market_data.price_estimation.factors.fuel_factor >= 1.0 ? "green.500" : "red.500"} 
                        mr={2} 
                      />
                      <Text>Factor: {market_data.price_estimation.factors.fuel_factor.toFixed(2)}</Text>
                    </Flex>
                  </Box>
                  <Box>
                    <Text fontWeight="bold">Transmission:</Text>
                    <Flex align="center">
                      <Icon 
                        as={market_data.price_estimation.factors.transmission_factor >= 1.0 ? FaRegThumbsUp : FaRegThumbsDown} 
                        color={market_data.price_estimation.factors.transmission_factor >= 1.0 ? "green.500" : "red.500"} 
                        mr={2} 
                      />
                      <Text>Factor: {market_data.price_estimation.factors.transmission_factor.toFixed(2)}</Text>
                    </Flex>
                  </Box>
                </SimpleGrid>
              </Box>

              <Box>
                <Heading size="sm" mb={3} color="gray.600">Data Sources</Heading>
                <Text>Price data based on {market_data.data_sources.join(", ")}</Text>
              </Box>
            </VStack>
          </TabPanel>

          <TabPanel>
            <VStack spacing={4} align="stretch">
              {recommendations.critical && recommendations.critical.length > 0 && (
                <Box>
                  <Heading size="sm" mb={3} color="gray.600">Critical Checks</Heading>
                  <List spacing={3}>
                    {recommendations.critical.map((rec, index) => (
                      <ListItem key={index}>
                        <ListIcon as={FaExclamationCircle} color="red.500" />
                        {rec}
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}

              {recommendations.important && recommendations.important.length > 0 && (
                <Box>
                  <Heading size="sm" mb={3} color="gray.600">Important Checks</Heading>
                  <List spacing={3}>
                    {recommendations.important.map((rec, index) => (
                      <ListItem key={index}>
                        <ListIcon as={FaExclamationTriangle} color="orange.500" />
                        {rec}
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}

              {recommendations.model_specific && recommendations.model_specific.length > 0 && (
                <Box>
                  <Heading size="sm" mb={3} color="gray.600">Model-Specific Checks</Heading>
                  <List spacing={3}>
                    {recommendations.model_specific.map((rec, index) => (
                      <ListItem key={index}>
                        <ListIcon as={FaTools} color="blue.500" />
                        {rec}
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}

              {recommendations.additional && recommendations.additional.length > 0 && (
                <Box>
                  <Heading size="sm" mb={3} color="gray.600">Additional Checks</Heading>
                  <List spacing={3}>
                    {recommendations.additional.map((rec, index) => (
                      <ListItem key={index}>
                        <ListIcon as={FaCheckCircle} color="green.500" />
                        {rec}
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}
            </VStack>
          </TabPanel>
        </TabPanels>
      </Tabs>

      <Button
        colorScheme="accent"
        size="lg"
        width="full"
        onClick={resetForm}
        bg="accent.500"
        _hover={{ bg: 'accent.600' }}
      >
        Check Another Vehicle
      </Button>
    </VStack>
  );
};

const UsedCarCheck = () => {
  // Define all state in one object for easier management
  const [formData, setFormData] = useState({
    vin: '',
    make: '',
    model: '',
    year: '',
    mileage: '',
    additionalInfo: '',
    fuelType: '',
    transmissionType: '',
    condition: ''
  });
  const [submitted, setSubmitted] = useState(false);
  const [hasVin, setHasVin] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [checkResult, setCheckResult] = useState(null);
  const [options, setOptions] = useState({
    makes: [],
    models: [],
    years: [],
    fuelTypes: [],
    transmissionTypes: []
  });
  const [loadingOptions, setLoadingOptions] = useState(true);
  
  // Define all theme-related variables
  const cardBg = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('transparent', 'gray.600');
  const headerBg = useColorModeValue('brand.50', 'gray.800');
  const toast = useToast();

  // Fetch dropdown options on component mount
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        setLoadingOptions(true);
        console.log('Fetching car options...');
        const response = await fetch('http://localhost:8099/api/used-car/options');
        console.log('Response status:', response.status);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch car options: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Received options data:', data);
        console.log('fuelTypes from API:', data.fuelTypes);
        console.log('transmissionTypes from API:', data.transmissionTypes);
        
        setOptions({
          makes: data.makes || [],
          models: [],
          years: data.years || [],
          fuelTypes: data.fuelTypes || [],
          transmissionTypes: data.transmissionTypes || []
        });
      } catch (error) {
        console.error('Error fetching car options:', error);
        toast({
          title: 'Error',
          description: `Failed to load car options: ${error.message}`,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setLoadingOptions(false);
      }
    };
    
    fetchOptions();
  }, [toast]);
  
  // Update models when make changes
  useEffect(() => {
    const updateModels = async () => {
      if (!formData.make) {
        setOptions(prev => ({ ...prev, models: [] }));
        return;
      }
      
      try {
        console.log('Fetching models for make:', formData.make);
        const response = await fetch('http://localhost:8099/api/used-car/options');
        console.log('Response status:', response.status);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch car models: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Models data:', data);
        
        if (data.models_by_make && data.models_by_make[formData.make]) {
          setOptions(prev => ({ 
            ...prev, 
            models: data.models_by_make[formData.make] 
          }));
        } else {
          setOptions(prev => ({ ...prev, models: [] }));
        }
      } catch (error) {
        console.error('Error fetching car models:', error);
        setOptions(prev => ({ ...prev, models: [] }));
      }
    };
    
    updateModels();
  }, [formData.make]);

  // Update hasVin whenever vin changes
  useEffect(() => {
    setHasVin(formData.vin.trim().length > 0);
  }, [formData.vin]);

  const validateForm = () => {
    const errors = {};
    
    if (!hasVin) {
      // If no VIN, require other fields
      if (!formData.make.trim()) errors.make = "Make is required when VIN is not provided";
      if (!formData.model.trim()) errors.model = "Model is required when VIN is not provided";
      if (!formData.year) errors.year = "Year is required when VIN is not provided";
      if (!formData.mileage) errors.mileage = "Mileage is required when VIN is not provided";
      if (!formData.fuelType) errors.fuelType = "Fuel type is required when VIN is not provided";
      if (!formData.transmissionType) errors.transmissionType = "Transmission type is required when VIN is not provided";
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      try {
        setLoading(true);
        
        // Prepare request data
        const requestData = {
          make: formData.make,
          model: formData.model,
          year: parseInt(formData.year),
          mileage: parseInt(formData.mileage),
          fuel_type: formData.fuelType,
          transmission: formData.transmissionType
        };
        
        // Call the API
        const response = await fetch('http://localhost:8099/api/used-car/check', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData),
        });
        
        if (!response.ok) {
          throw new Error('Failed to check vehicle');
        }
        
        const result = await response.json();
        setCheckResult(result);
        setSubmitted(true);
      } catch (error) {
        console.error('Error checking vehicle:', error);
        toast({
          title: 'Error',
          description: 'Failed to check vehicle. Please try again later.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setLoading(false);
      }
    }
  };

  const resetForm = () => {
    setSubmitted(false);
    setCheckResult(null);
    setFormData({
      vin: '',
      make: '',
      model: '',
      year: '',
      mileage: '',
      additionalInfo: '',
      fuelType: '',
      transmissionType: '',
      condition: ''
    });
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
            <Heading size="xl">Used Car Check</Heading>
            <Text fontSize="lg">
              Verify a used car's history and condition before you buy
            </Text>
          </VStack>
        </Box>

        <Card bg={cardBg} borderColor={borderColor} shadow="md">
          <CardHeader bg={headerBg}>
            <Heading size="md" color="brand.600">
              {!submitted 
                ? "Vehicle Information" 
                : (formData.vin 
                    ? `Vehicle Report for VIN: ${formData.vin}` 
                    : `Vehicle Report for ${formData.year} ${formData.make} ${formData.model}`
                  )
              }
            </Heading>
          </CardHeader>
          <CardBody>
            {!submitted 
              ? <VehicleForm 
                  formData={formData} 
                  setFormData={setFormData} 
                  formErrors={formErrors} 
                  handleSubmit={handleSubmit} 
                  hasVin={hasVin} 
                  options={options} 
                  loadingOptions={loadingOptions} 
                />
              : <VehicleResults 
                  formData={formData} 
                  resetForm={resetForm} 
                  checkResult={checkResult} 
                />
            }
          </CardBody>
        </Card>
      </VStack>
    </Container>
  );
};

export default UsedCarCheck;
