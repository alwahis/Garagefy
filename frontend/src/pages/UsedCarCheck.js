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
  AlertTitle,
  AlertDescription,
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
  useToast,
  RadioGroup,
  Radio
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
  FaRegThumbsDown,
  FaArrowLeft
} from 'react-icons/fa';

// Form component
const VehicleForm = ({ formData, setFormData, formErrors, handleSubmit, hasVin, options, loadingOptions }) => {
  const { vin, make, model, year, mileage, additionalInfo, fuelType, transmissionType, condition } = formData;
  
  console.log('VehicleForm options:', options);
  
  return (
    <form onSubmit={handleSubmit}>
      <VStack spacing={6} align="stretch">
        <FormControl>
          <FormLabel display="flex" alignItems="center" fontWeight="medium" color="text.900">
            <Icon as={FaCarAlt} mr={2} color="brand.600" />
            VIN (Vehicle Identification Number)
          </FormLabel>
          <Input
            value={vin}
            onChange={(e) => setFormData({...formData, vin: e.target.value})}
            placeholder="e.g. 1HGCM82633A123456"
            bg="white"
            borderColor="secondary.200"
            _hover={{ borderColor: "accent.500" }}
            _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
          />
          <FormHelperText color="text.700">
            If you provide a VIN, the other vehicle details become optional.
          </FormHelperText>
        </FormControl>

        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
          <FormControl isRequired={!hasVin} isInvalid={formErrors.make}>
            <FormLabel display="flex" alignItems="center" fontWeight="medium" color="text.900">
              <Icon as={FaCarAlt} mr={2} color="brand.600" />
              Make {!hasVin && <Text color="red.500" ml={1}>*</Text>}
            </FormLabel>
            <Select
              value={make}
              onChange={(e) => setFormData({...formData, make: e.target.value})}
              placeholder="Select make"
              isDisabled={loadingOptions}
              bg="white"
              borderColor="secondary.200"
              _hover={{ borderColor: "accent.500" }}
              _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
            >
              {options.makes.map((make, index) => (
                <option key={index} value={make}>{make}</option>
              ))}
            </Select>
            {formErrors.make && <FormHelperText color="red.500">{formErrors.make}</FormHelperText>}
          </FormControl>
          
          <FormControl isRequired={!hasVin} isInvalid={formErrors.model}>
            <FormLabel display="flex" alignItems="center" fontWeight="medium" color="text.900">
              <Icon as={FaCarAlt} mr={2} color="brand.600" />
              Model {!hasVin && <Text color="red.500" ml={1}>*</Text>}
            </FormLabel>
            <Select
              value={model}
              onChange={(e) => setFormData({...formData, model: e.target.value})}
              placeholder="Select model"
              isDisabled={!make || loadingOptions}
              bg="white"
              borderColor="secondary.200"
              _hover={{ borderColor: "accent.500" }}
              _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
            >
              {options.models.map((model, index) => (
                <option key={index} value={model}>{model}</option>
              ))}
            </Select>
            {formErrors.model && <FormHelperText color="red.500">{formErrors.model}</FormHelperText>}
          </FormControl>
          
          <FormControl isRequired={!hasVin} isInvalid={formErrors.year}>
            <FormLabel display="flex" alignItems="center" fontWeight="medium" color="text.900">
              <Icon as={FaCalendarAlt} mr={2} color="brand.600" />
              Year {!hasVin && <Text color="red.500" ml={1}>*</Text>}
            </FormLabel>
            <Select
              value={year}
              onChange={(e) => setFormData({...formData, year: e.target.value})}
              placeholder="Select year"
              isDisabled={loadingOptions}
              bg="white"
              borderColor="secondary.200"
              _hover={{ borderColor: "accent.500" }}
              _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
            >
              {options.years.map((year, index) => (
                <option key={index} value={year}>{year}</option>
              ))}
            </Select>
            {formErrors.year && <FormHelperText color="red.500">{formErrors.year}</FormHelperText>}
          </FormControl>
        </SimpleGrid>
        
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
          <FormControl isRequired={!hasVin} isInvalid={formErrors.mileage}>
            <FormLabel display="flex" alignItems="center" fontWeight="medium" color="text.900">
              <Icon as={FaChartLine} mr={2} color="brand.600" />
              Mileage (km) {!hasVin && <Text color="red.500" ml={1}>*</Text>}
            </FormLabel>
            <Input
              type="number"
              value={mileage}
              onChange={(e) => setFormData({...formData, mileage: e.target.value})}
              placeholder="e.g. 50000"
              bg="white"
              borderColor="secondary.200"
              _hover={{ borderColor: "accent.500" }}
              _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
            />
            {formErrors.mileage && <FormHelperText color="red.500">{formErrors.mileage}</FormHelperText>}
          </FormControl>
          
          <FormControl isRequired={!hasVin} isInvalid={formErrors.fuelType}>
            <FormLabel display="flex" alignItems="center" fontWeight="medium" color="text.900">
              <Icon as={FaGasPump} mr={2} color="brand.600" />
              Fuel Type {!hasVin && <Text color="red.500" ml={1}>*</Text>}
            </FormLabel>
            <Select
              value={fuelType}
              onChange={(e) => setFormData({...formData, fuelType: e.target.value})}
              placeholder="Select fuel type"
              isDisabled={loadingOptions}
              bg="white"
              borderColor="secondary.200"
              _hover={{ borderColor: "accent.500" }}
              _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
            >
              {options.fuelTypes.map((type, index) => (
                <option key={index} value={type.id}>{type.name}</option>
              ))}
            </Select>
            {formErrors.fuelType && <FormHelperText color="red.500">{formErrors.fuelType}</FormHelperText>}
          </FormControl>
          
          <FormControl isRequired={!hasVin} isInvalid={formErrors.transmissionType}>
            <FormLabel display="flex" alignItems="center" fontWeight="medium" color="text.900">
              <Icon as={FaCog} mr={2} color="brand.600" />
              Transmission {!hasVin && <Text color="red.500" ml={1}>*</Text>}
            </FormLabel>
            <Select
              value={transmissionType}
              onChange={(e) => setFormData({...formData, transmissionType: e.target.value})}
              placeholder="Select transmission"
              isDisabled={loadingOptions}
              bg="white"
              borderColor="secondary.200"
              _hover={{ borderColor: "accent.500" }}
              _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
            >
              {options.transmissionTypes.map((type, index) => (
                <option key={index} value={type.id}>{type.name}</option>
              ))}
            </Select>
            {formErrors.transmissionType && <FormHelperText color="red.500">{formErrors.transmissionType}</FormHelperText>}
          </FormControl>
        </SimpleGrid>
        
        <FormControl>
          <FormLabel display="flex" alignItems="center" fontWeight="medium" color="text.900">
            <Icon as={FaInfoCircle} mr={2} color="brand.600" />
            Additional Information
          </FormLabel>
          <Textarea
            value={additionalInfo}
            onChange={(e) => setFormData({...formData, additionalInfo: e.target.value})}
            placeholder="Enter any additional information about the vehicle..."
            rows={4}
            bg="white"
            borderColor="secondary.200"
            _hover={{ borderColor: "accent.500" }}
            _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
          />
        </FormControl>
        
        <FormControl>
          <FormLabel display="flex" alignItems="center" fontWeight="medium" color="text.900">
            <Icon as={FaCarCrash} mr={2} color="brand.600" />
            Vehicle Condition
          </FormLabel>
          <RadioGroup 
            value={condition} 
            onChange={(value) => setFormData({...formData, condition: value})}
          >
            <Stack direction="row" spacing={5} wrap="wrap">
              <Radio value="excellent" colorScheme="green">Excellent</Radio>
              <Radio value="good" colorScheme="teal">Good</Radio>
              <Radio value="fair" colorScheme="yellow">Fair</Radio>
              <Radio value="poor" colorScheme="orange">Poor</Radio>
              <Radio value="salvage" colorScheme="red">Salvage</Radio>
            </Stack>
          </RadioGroup>
        </FormControl>
        
        <Button 
          type="submit" 
          colorScheme="accent" 
          size="lg" 
          width="full"
          leftIcon={<Icon as={FaClipboardCheck} />}
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
  const { analysis, market_data, recommendations } = checkResult;
  
  return (
    <VStack spacing={6} align="stretch">
      <Card bg="white" borderColor="secondary.200" boxShadow="lg" borderRadius="lg" overflow="hidden">
        <CardHeader bg="white" color="text.900">
          <Flex justifyContent="space-between" alignItems="center">
            <Heading size="md">
              <Flex align="center">
                <Icon as={FaCarAlt} mr={2} color="brand.600" />
                {vin ? `Vehicle Report for VIN: ${vin}` : `Vehicle Report for ${year} ${make} ${model}`}
              </Flex>
            </Heading>
            <Button 
              leftIcon={<Icon as={FaArrowLeft} />} 
              onClick={resetForm}
              variant="outline"
              borderColor="accent.500"
              color="accent.500"
              _hover={{ bg: "rgba(242, 169, 0, 0.1)" }}
            >
              New Check
            </Button>
          </Flex>
        </CardHeader>
        
        <CardBody>
          <VStack spacing={6} align="stretch">
            <Box>
              <Heading size="sm" mb={3} color="text.900">Vehicle Details</Heading>
              <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                {vin && (
                  <Box>
                    <Text fontWeight="bold" color="brand.600">VIN:</Text>
                    <Text>{vin}</Text>
                  </Box>
                )}
                <Box>
                  <Text fontWeight="bold" color="brand.600">Make:</Text>
                  <Text>{make}</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold" color="brand.600">Model:</Text>
                  <Text>{model}</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold" color="brand.600">Year:</Text>
                  <Text>{year}</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold" color="brand.600">Mileage:</Text>
                  <Text>{mileage} km</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold" color="brand.600">Fuel Type:</Text>
                  <Text>{fuelType}</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold" color="brand.600">Transmission:</Text>
                  <Text>{transmissionType}</Text>
                </Box>
              </SimpleGrid>
            </Box>
            
            <Tabs colorScheme="accent" variant="enclosed">
              <TabList>
                <Tab _selected={{ color: "accent.500", borderColor: "accent.500", borderBottomColor: "transparent" }}>
                  <Icon as={FaChartLine} mr={2} />
                  Analysis
                </Tab>
                <Tab _selected={{ color: "accent.500", borderColor: "accent.500", borderBottomColor: "transparent" }}>
                  <Icon as={FaExclamationTriangle} mr={2} />
                  Issues
                </Tab>
                <Tab _selected={{ color: "accent.500", borderColor: "accent.500", borderBottomColor: "transparent" }}>
                  <Icon as={FaEuroSign} mr={2} />
                  Value
                </Tab>
                <Tab _selected={{ color: "accent.500", borderColor: "accent.500", borderBottomColor: "transparent" }}>
                  <Icon as={FaClipboardCheck} mr={2} />
                  Recommendations
                </Tab>
              </TabList>
              
              <TabPanels>
                <TabPanel>
                  <VStack spacing={4} align="stretch">
                    <Box>
                      <Heading size="sm" mb={3} color="text.900">Reliability Score</Heading>
                      <Flex align="center" mb={2}>
                        <Progress 
                          value={analysis.reliability_score.score} 
                          max={100}
                          min={0}
                          colorScheme={
                            analysis.reliability_score.score >= 80 ? "green" :
                            analysis.reliability_score.score >= 60 ? "yellow" :
                            analysis.reliability_score.score >= 40 ? "orange" : "red"
                          }
                          flex="1"
                          borderRadius="md"
                          height="10px"
                          bg="white"
                        />
                        <Text ml={4} fontWeight="bold">
                          {analysis.reliability_score.score}/100
                        </Text>
                      </Flex>
                      <Text>
                        Rating: <Badge colorScheme={
                          analysis.reliability_score.rating === "Excellent" ? "green" :
                          analysis.reliability_score.rating === "Very Good" ? "teal" :
                          analysis.reliability_score.rating === "Good" ? "blue" :
                          analysis.reliability_score.rating === "Fair" ? "yellow" : "red"
                        }>
                          {analysis.reliability_score.rating}
                        </Badge>
                      </Text>
                    </Box>

                    <Box>
                      <Heading size="sm" mb={3} color="text.900">Mileage Assessment</Heading>
                      <Alert 
                        status={
                          analysis.mileage_assessment.category === "very_high" ? "error" : 
                          analysis.mileage_assessment.category === "high" ? "warning" : 
                          analysis.mileage_assessment.category === "average" ? "info" : 
                          "success"
                        }
                        variant="left-accent"
                        borderRadius="md"
                        bg="white"
                      >
                        <AlertIcon />
                        <Box>
                          <AlertTitle>{analysis.mileage_assessment.category === "very_high" ? "Very High Mileage" : 
                                      analysis.mileage_assessment.category === "high" ? "High Mileage" : 
                                      analysis.mileage_assessment.category === "average" ? "Average Mileage" : 
                                      "Low Mileage"}</AlertTitle>
                          <AlertDescription>
                            {analysis.mileage_assessment.category === "very_high" ? 
                              `This vehicle has very high mileage (${analysis.mileage_assessment.annual_average} km/year). Extensive wear is likely.` : 
                            analysis.mileage_assessment.category === "high" ? 
                              `This vehicle has high mileage (${analysis.mileage_assessment.annual_average} km/year). Above average wear is expected.` : 
                            analysis.mileage_assessment.category === "average" ? 
                              `This vehicle has average mileage (${analysis.mileage_assessment.annual_average} km/year). Normal wear is expected.` : 
                              `This vehicle has low mileage (${analysis.mileage_assessment.annual_average} km/year). Less wear than average is expected.`}
                          </AlertDescription>
                        </Box>
                      </Alert>
                    </Box>
                  </VStack>
                </TabPanel>

                <TabPanel>
                  <Box>
                    <Heading size="sm" mb={3} color="text.900">Known Issues</Heading>
                    {analysis.common_issues.length > 0 ? (
                      <List spacing={3}>
                        {analysis.common_issues.map((issue, index) => (
                          <ListItem key={index}>
                            <Alert 
                              status="warning"
                              variant="left-accent"
                              borderRadius="md"
                              bg="white"
                            >
                              <AlertIcon />
                              <Box>
                                <AlertTitle>Potential Issue</AlertTitle>
                                <AlertDescription>{issue}</AlertDescription>
                              </Box>
                            </Alert>
                          </ListItem>
                        ))}
                      </List>
                    ) : (
                      <Text>No common issues reported for this vehicle.</Text>
                    )}
                  </Box>
                </TabPanel>

                <TabPanel>
                  <VStack spacing={4} align="stretch">
                    <Box>
                      <Heading size="sm" mb={3} color="text.900">Market Value</Heading>
                      <Stat>
                        <StatLabel>Estimated value in {market_data.market_region}</StatLabel>
                        <StatNumber>
                          <Text fontSize="2xl" fontWeight="bold" color="brand.600">
                            €{market_data.price_estimation.estimated_price.toLocaleString()}
                          </Text>
                        </StatNumber>
                        <StatHelpText>
                          Range: €{market_data.price_estimation.price_range.low.toLocaleString()} - €{market_data.price_estimation.price_range.high.toLocaleString()}
                        </StatHelpText>
                      </Stat>
                    </Box>

                    <Box>
                      <Heading size="sm" mb={3} color="text.900">Price Factors</Heading>
                      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                        <Box>
                          <Text fontWeight="bold">Age Factor:</Text>
                          <Text>{market_data.price_estimation.factors.age_factor}</Text>
                        </Box>
                        <Box>
                          <Text fontWeight="bold">Mileage Factor:</Text>
                          <Text>{market_data.price_estimation.factors.mileage_factor}</Text>
                        </Box>
                        <Box>
                          <Text fontWeight="bold">Fuel Type Factor:</Text>
                          <Text>{market_data.price_estimation.factors.fuel_factor}</Text>
                        </Box>
                        <Box>
                          <Text fontWeight="bold">Transmission Factor:</Text>
                          <Text>{market_data.price_estimation.factors.transmission_factor}</Text>
                        </Box>
                      </SimpleGrid>
                    </Box>
                  </VStack>
                </TabPanel>

                <TabPanel>
                  <VStack spacing={4} align="stretch">
                    {recommendations.critical && recommendations.critical.length > 0 && (
                      <Box>
                        <Heading size="sm" mb={3} color="text.900">Critical Checks</Heading>
                        <List spacing={3}>
                          {recommendations.critical.map((rec, index) => (
                            <ListItem key={index}>
                              <Alert status="error" variant="left-accent" borderRadius="md" bg="white">
                                <AlertIcon />
                                <AlertDescription>{rec}</AlertDescription>
                              </Alert>
                            </ListItem>
                          ))}
                        </List>
                      </Box>
                    )}

                    {recommendations.important && recommendations.important.length > 0 && (
                      <Box>
                        <Heading size="sm" mb={3} color="text.900">Important Checks</Heading>
                        <List spacing={3}>
                          {recommendations.important.map((rec, index) => (
                            <ListItem key={index}>
                              <Alert status="warning" variant="left-accent" borderRadius="md" bg="white">
                                <AlertIcon />
                                <AlertDescription>{rec}</AlertDescription>
                              </Alert>
                            </ListItem>
                          ))}
                        </List>
                      </Box>
                    )}

                    {recommendations.model_specific && recommendations.model_specific.length > 0 && (
                      <Box>
                        <Heading size="sm" mb={3} color="text.900">Model-Specific Checks</Heading>
                        <List spacing={3}>
                          {recommendations.model_specific.map((rec, index) => (
                            <ListItem key={index}>
                              <Alert status="info" variant="left-accent" borderRadius="md" bg="white">
                                <AlertIcon />
                                <AlertDescription>{rec}</AlertDescription>
                              </Alert>
                            </ListItem>
                          ))}
                        </List>
                      </Box>
                    )}

                    {recommendations.additional && recommendations.additional.length > 0 && (
                      <Box>
                        <Heading size="sm" mb={3} color="text.900">Additional Checks</Heading>
                        <List spacing={3}>
                          {recommendations.additional.map((rec, index) => (
                            <ListItem key={index}>
                              <Alert status="success" variant="left-accent" borderRadius="md" bg="white">
                                <AlertIcon />
                                <AlertDescription>{rec}</AlertDescription>
                              </Alert>
                            </ListItem>
                          ))}
                        </List>
                      </Box>
                    )}
                  </VStack>
                </TabPanel>
              </TabPanels>
            </Tabs>
          </VStack>
        </CardBody>
      </Card>
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
  const cardBg = 'white';
  const borderColor = 'secondary.200';
  const headerBg = 'white';
  const textColor = 'text.900';
  const mutedTextColor = 'text.700';
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
          color={textColor}
        >
          <VStack spacing={4} align="stretch">
            <Heading size="xl" mb={4}>Used Car Check</Heading>
            <Text fontSize="lg">
              Get comprehensive information about a used car before you buy, including reliability scores, common issues, and market value.
            </Text>
          </VStack>
        </Box>
        
        {submitted && checkResult ? (
          <VehicleResults 
            formData={formData} 
            resetForm={resetForm} 
            checkResult={checkResult} 
          />
        ) : (
          <Card bg={cardBg} borderColor={borderColor} boxShadow="lg" borderRadius="lg" overflow="hidden">
            <CardHeader bg={headerBg} color={textColor}>
              <Heading size="md">
                <Flex align="center">
                  <Icon as={FaCarAlt} mr={2} color="brand.600" />
                  Vehicle Information
                </Flex>
              </Heading>
            </CardHeader>
            <CardBody>
              <VehicleForm 
                formData={formData}
                setFormData={setFormData}
                formErrors={formErrors}
                handleSubmit={handleSubmit}
                hasVin={hasVin}
                options={options}
                loadingOptions={loadingOptions}
              />
              
              {loading && (
                <Flex justify="center" py={10} direction="column" align="center">
                  <Spinner size="xl" color="accent.500" thickness="4px" mb={4} />
                  <Text>Analyzing vehicle data...</Text>
                </Flex>
              )}
            </CardBody>
          </Card>
        )}
      </VStack>
    </Container>
  );
};

export default UsedCarCheck;
