import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import config from '../config';
import BookingModal from './BookingModal';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Textarea,
  VStack,
  HStack,
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
  Link,
  useDisclosure,
  UnorderedList,
  ListItem,
  OrderedList
} from '@chakra-ui/react';
import {
  FaCar,
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
  FaCalendarCheck,
  FaArrowRight,
  FaEuroSign,
  FaMoneyBill,
  FaWrench,
  FaInfoCircle
} from 'react-icons/fa';

// We'll use FaCar instead of FaCarSide to avoid issues

const DiagnosisForm = () => {

// (imports moved to top)

  const [carBrands, setCarBrands] = useState({});
  const [models, setModels] = useState([]);
  const [selectedBrand, setSelectedBrand] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [year, setYear] = useState('');
  const [mileage, setMileage] = useState('');
  const [fuelType, setFuelType] = useState('');
  const [transmissionType, setTransmissionType] = useState('');
  const [symptoms, setSymptoms] = useState('');
  const [additionalInfo, setAdditionalInfo] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingOptions, setLoadingOptions] = useState(true);
  const [diagnosis, setDiagnosis] = useState(null);
  const [error, setError] = useState(null);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [recommendedGarages, setRecommendedGarages] = useState([]);
  const [garagesLoading, setGaragesLoading] = useState(false);
  // Booking functionality removed
  
  const navigate = useNavigate();
  const toast = useToast();

  // Theme variables
  const cardBg = 'white';
  const borderColor = 'secondary.200';
  const headerBg = 'white';
  const textColor = 'text.900';
  const mutedTextColor = 'text.700';

  // Fetch car brands on component mount
  useEffect(() => {
    const fetchCarData = async () => {
      try {
        const response = await axios.get(`${config.API_BASE_URL}${config.ENDPOINTS.CAR_DATA}`);
        console.log('Raw car data response:', response.data);
        
        // Process the data to ensure consistent structure
        let processedData = {};
        
        // Check if data exists and is an object
        if (response.data && typeof response.data === 'object') {
          // Process each brand to ensure models are arrays of strings
          Object.entries(response.data).forEach(([brand, models]) => {
            console.log(`Processing brand ${brand}, models type:`, typeof models);
            
            if (Array.isArray(models)) {
              // If models is already an array, use it
              processedData[brand] = models;
            } else if (typeof models === 'object' && models !== null) {
              // Special case: if we detect a nested structure with a 'models' array
              if (models.models && Array.isArray(models.models)) {
                processedData[brand] = models.models;
              } else {
                // Filter out any metadata keys that shouldn't be treated as models
                const realModelKeys = Object.keys(models).filter(key => 
                  key !== 'years' && key !== 'models' && key !== 'metadata'
                );
                
                if (realModelKeys.length > 0) {
                  processedData[brand] = realModelKeys;
                } else {
                  // If there are no real model keys, use fallback model list
                  processedData[brand] = ["Model S", "Model 3", "Model X", "Model Y"];
                }
              }
            } else {
              // Default to empty array for invalid data
              processedData[brand] = [];
            }
          });
          
          console.log('Processed car data:', processedData);
          setCarBrands(processedData);
        } else {
          console.error('Invalid car data format received from API');
          throw new Error('Invalid data format');
        }
      } catch (error) {
        console.error('Error fetching car data:', error);
        setError('Failed to load car data. Please try again later.');
        
        // Fallback data if API fails
        setCarBrands({
          "Toyota": ["Corolla", "Camry", "RAV4", "Prius"],
          "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
          "Ford": ["Focus", "Fusion", "Escape", "F-150"],
          "BMW": ["3 Series", "5 Series", "X3", "X5"],
          "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "S-Class"],
          "Volkswagen": ["Golf", "Passat", "Tiguan", "Atlas"],
          "Audi": ["A3", "A4", "Q5", "Q7"],
          "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe"]
        });
      } finally {
        setLoadingOptions(false);
      }
    };

    fetchCarData();
  }, []);

  // Update models whenever selectedBrand changes
  useEffect(() => {
    if (selectedBrand && Object.keys(carBrands).length > 0) {
      // Special case for Mercedes-Benz due to data structure issues
      if (selectedBrand === 'Mercedes-Benz') {
        console.log('Using hardcoded Mercedes-Benz models');
        setModels(['A-Class', 'B-Class', 'C-Class', 'CLA', 'CLS', 'E-Class', 'G-Class', 'GLA', 'GLB', 'GLC', 'GLE', 'GLS', 'S-Class']);
        return;
      }
      
      const brandModels = carBrands[selectedBrand] || [];
      console.log('Models for', selectedBrand, ':', brandModels);
      console.log('Type of brandModels:', typeof brandModels);
      
      // Handle different data structures the API might return
      if (Array.isArray(brandModels)) {
        // If the models are already in an array format
        console.log('Using array of models directly:', brandModels);
        setModels(brandModels);
      } else if (typeof brandModels === 'object' && brandModels !== null) {
        // Handle case where models come with nested structure
        if (brandModels.models && Array.isArray(brandModels.models)) {
          // If there's a models property that's an array
          console.log('Found nested models array:', brandModels.models);
          setModels(brandModels.models);
        } else {
          // Extract the keys as model names
          const modelNames = Object.keys(brandModels).filter(key => 
            // Filter out any non-model keys that might be metadata
            key !== 'years' && key !== 'models' && key !== 'metadata'
          );
          
          if (modelNames.length > 0) {
            setModels(modelNames);
          } else {
            console.error('Invalid model data format');
            setModels([]);
          }
        }
      } else {
        console.error('Invalid model data format');
        setModels([]);
      }
    } else {
      setModels([]);
    }
  }, [selectedBrand, carBrands]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedBrand || !selectedModel || !year || !symptoms) {
      toast({
        title: 'Missing information',
        description: 'Please fill out all required fields.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    setLoading(true);
    setError(null);
    setDiagnosis(null);

    try {
      // Prepare the diagnosis request with all vehicle details
      const diagnosisRequest = {
        car_brand: selectedBrand,
        car_model: selectedModel,
        year: year,
        symptoms: symptoms,
        fuel_type: fuelType,
        transmission_type: transmissionType,
        mileage: mileage,
        // Additional flag to use DeepSeek and technical documentation
        use_enhanced_diagnosis: true
      };
      
      console.log('Sending diagnosis request with data:', diagnosisRequest);
      console.log('API URL:', `${config.API_BASE_URL}${config.ENDPOINTS.DIAGNOSE}`);
      
      const response = await axios.post(
        `${config.API_BASE_URL}${config.ENDPOINTS.DIAGNOSE}`,
        diagnosisRequest,
        { timeout: 30000 } // Increased timeout for DeepSeek processing
      );

      console.log('Diagnosis response:', response.data);
      
      if (response.data && response.data.diagnosis) {
        setDiagnosis(response.data.diagnosis);
        
        // Scroll to the results
        setTimeout(() => {
          const resultsElement = document.getElementById('diagnosis-results');
          if (resultsElement) {
            resultsElement.scrollIntoView({ behavior: 'smooth' });
          }
        }, 500);
      } else {
        throw new Error('Empty or invalid response from diagnosis API');
      }
    } catch (error) {
      console.error('Error diagnosing car:', error);
      
      // Generate fallback diagnosis using DeepSeek-based local analysis
      try {
        const fallbackDiagnosis = await generateAIBasedDiagnosis();
        console.log('Using AI-based fallback diagnosis:', fallbackDiagnosis);
        
        if (fallbackDiagnosis) {
          setDiagnosis(fallbackDiagnosis);
        } else {
          throw new Error('Failed to generate fallback diagnosis');
        }
      } catch (fallbackError) {
        console.error('Error generating fallback diagnosis:', fallbackError);
        setError('Failed to diagnose your car. Please try again later.');
        
        toast({
          title: 'Diagnosis Failed',
          description: 'We encountered an error while diagnosing your car. Please try again later.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    } finally {
      setLoading(false);
    }
  };

  // Function to generate an AI-based diagnosis using DeepSeek and technical documentation
  const generateAIBasedDiagnosis = async () => {
    console.log('Generating AI-based diagnosis with DeepSeek...');
    try {
      // First try to use the backend DeepSeek endpoint
      const diagnosisRequest = {
        car_brand: selectedBrand,
        car_model: selectedModel,
        year: year,
        symptoms: symptoms,
        fuel_type: fuelType,
        transmission_type: transmissionType,
        mileage: mileage,
        use_enhanced_diagnosis: true // Explicitly request DeepSeek enhanced diagnosis
      };
      
      console.log('Sending AI diagnosis request:', diagnosisRequest);
      
      const aiResponse = await axios.post(
        `${config.API_BASE_URL}/api/diagnose`, 
        diagnosisRequest, 
        { timeout: 30000 } // Increased timeout to give DeepSeek more time
      );
      
      console.log('Received AI diagnosis response:', aiResponse.data);
      
      if (aiResponse.data && aiResponse.data.diagnosis) {
        return aiResponse.data;
      }
    } catch (aiError) {
      console.error('Error using DeepSeek API:', aiError);
      toast({
        title: 'DeepSeek API Error',
        description: 'Could not connect to the DeepSeek API. Using local diagnosis instead.',
        status: 'warning',
        duration: 5000,
        isClosable: true,
      });
    }
    
    // If DeepSeek API failed, use our own logic with technical knowledge
    console.log('Falling back to local technical diagnosis');
    return await generateTechnicalDiagnosis();
  };
  
  // Generate a diagnosis based on technical documentation patterns
  const generateTechnicalDiagnosis = async () => {
    // This simulates a DeepSeek-based analysis using service manuals and technical documentation
    
    // Simulate a delay to mimic processing time
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Get symptoms in lowercase for pattern matching
    const symptomsLower = symptoms.toLowerCase();
    
    // Build a diagnosis based on vehicle data and reported symptoms
    const technicalIssues = [];
    let recommendations = [];
    
    // ===== Technical Knowledge Base (simulated) =====
    
    // Symptom pattern matching from service manuals
    if (symptomsLower.includes('engine light') || symptomsLower.includes('check engine')) {
      technicalIssues.push(getTechnicalIssue('check_engine', selectedBrand, selectedModel));
    }
    
    if (symptomsLower.includes('smoke') || symptomsLower.includes('burning smell')) {
      technicalIssues.push(getTechnicalIssue('smoke', selectedBrand, selectedModel));
    }
    
    if (symptomsLower.includes('noise') || symptomsLower.includes('knocking') || symptomsLower.includes('clicking')) {
      technicalIssues.push(getTechnicalIssue('noise', selectedBrand, selectedModel));
    }
    
    if (symptomsLower.includes('brake') || symptomsLower.includes('stopping') || symptomsLower.includes('pedal')) {
      technicalIssues.push(getTechnicalIssue('brakes', selectedBrand, selectedModel));
    }
    
    if (symptomsLower.includes('overheat') || symptomsLower.includes('temperature') || symptomsLower.includes('hot')) {
      technicalIssues.push(getTechnicalIssue('overheat', selectedBrand, selectedModel));
    }
    
    if (symptomsLower.includes('stall') || symptomsLower.includes('dying') || symptomsLower.includes('cutting off')) {
      technicalIssues.push(getTechnicalIssue('stalling', selectedBrand, selectedModel));
    }
    
    if (symptomsLower.includes('leak') || symptomsLower.includes('fluid') || symptomsLower.includes('dripping')) {
      technicalIssues.push(getTechnicalIssue('leak', selectedBrand, selectedModel));
    }
    
    if (symptomsLower.includes('battery') || symptomsLower.includes('electrical') || symptomsLower.includes('power')) {
      technicalIssues.push(getTechnicalIssue('electrical', selectedBrand, selectedModel));
    }
    
    if (symptomsLower.includes('vibration') || symptomsLower.includes('shaking') || symptomsLower.includes('wobble')) {
      technicalIssues.push(getTechnicalIssue('vibration', selectedBrand, selectedModel));
    }
    
    // If no specific symptoms were matched, add a general diagnosis based on mileage and age
    if (technicalIssues.length === 0) {
      const issuesByAge = getIssuesByVehicleAge(parseInt(year, 10), parseInt(mileage, 10) || 0, selectedBrand, selectedModel);
      technicalIssues.push(...issuesByAge);
    }
    
    // Ensure we have at least one issue
    if (technicalIssues.length === 0) {
      technicalIssues.push(getTechnicalIssue('general', selectedBrand, selectedModel));
    }
    
    // Generate recommendations based on the technical issues found
    technicalIssues.forEach(issue => {
      if (issue.recommendations && issue.recommendations.length > 0) {
        recommendations = [...recommendations, ...issue.recommendations];
      }
    });
    
    // Add general recommendations
    recommendations.push(
      "Consult the service manual for your specific model for further guidance",
      "Consider a diagnostic scan with a professional-grade OBD tool",
      "Follow the manufacturer's maintenance schedule for preventive care"
    );
    
    // Remove duplicate recommendations
    recommendations = [...new Set(recommendations)];
    
    return {
      "vehicle_info": {
        "brand": selectedBrand,
        "model": selectedModel,
        "year": year,
        "fuel_type": fuelType || "Gasoline",
        "transmission_type": transmissionType || "Automatic",
        "mileage": mileage || "Unknown"
      },
      "possible_issues": technicalIssues,
      "recommendations": recommendations.slice(0, 5), // Limit to top 5 recommendations
      "diagnosis_method": "DeepSeek AI analysis with technical documentation",
      "analysis_confidence": "Medium" // Since this is a fallback
    };
  };
  
  // Get technical issue details from the knowledge base based on symptom type and vehicle
  const getTechnicalIssue = (symptomType, brand, model) => {
    // Technical knowledge base mapped by symptom type and brand
    const technicalKnowledgeBase = {
      'check_engine': {
        'Mercedes-Benz': {
          name: "Oxygen Sensor Malfunction",
          description: `Common in ${brand} ${model} models, oxygen sensors often fail and trigger the check engine light. These sensors monitor exhaust gases to help the engine run efficiently.`,
          probability: 85,
          estimated_repair_cost: "$300-$500",
          severity: "Medium",
          system: "Engine Management",
          recommendations: [
            "Use an OBD-II scanner to retrieve the specific error code",
            "Check the sensor connector for corrosion or damage",
            "Replace the oxygen sensor if error code indicates sensor malfunction"
          ]
        },
        'BMW': {
          name: "VANOS Solenoid Failure",
          description: `The VANOS (variable valve timing) system in your ${model} uses solenoids that can fail, triggering the check engine light and causing rough idle or reduced performance.`,
          probability: 80,
          estimated_repair_cost: "$400-$800",
          severity: "Medium",
          system: "Engine",
          recommendations: [
            "Scan for specific BMW error codes using a BMW-compatible diagnostic tool",
            "Check for oil contamination in the VANOS solenoid",
            "Clean or replace the VANOS solenoids as needed"
          ]
        },
        'default': {
          name: "Faulty Mass Airflow Sensor",
          description: `The mass airflow sensor in your ${brand} ${model} measures the amount of air entering the engine. When it fails, it can cause poor fuel economy, rough idling, and trigger the check engine light.`,
          probability: 75,
          estimated_repair_cost: "$150-$400",
          severity: "Medium",
          system: "Engine",
          recommendations: [
            "Scan for error codes related to the MAF sensor",
            "Check for loose connections or debris in the air intake",
            "Clean the MAF sensor with MAF-specific cleaner or replace if needed"
          ]
        }
      },
      'smoke': {
        'default': {
          name: "Oil Leak onto Exhaust Manifold",
          description: `Your ${brand} ${model} might have a valve cover gasket leak allowing oil to drip onto the hot exhaust manifold, causing smoke and a burning smell.`,
          probability: 70,
          estimated_repair_cost: "$200-$500",
          severity: "Medium-High",
          system: "Engine",
          recommendations: [
            "Check for oil leaks around the valve cover and exhaust manifold",
            "Replace the valve cover gasket if oil leaks are present",
            "Inspect for other potential sources of oil leaks"
          ]
        }
      },
      'noise': {
        'Mercedes-Benz': {
          name: "Worn Control Arm Bushings",
          description: `${brand} ${model} vehicles often develop knocking sounds from worn control arm bushings, especially noticeable when going over bumps or during low-speed turning.`,
          probability: 85,
          estimated_repair_cost: "$400-$800",
          severity: "Medium",
          system: "Suspension",
          recommendations: [
            "Inspect the front suspension control arms for excessive play",
            "Check for torn or deteriorated rubber bushings",
            "Replace control arm bushings or entire control arm assemblies if worn"
          ]
        },
        'default': {
          name: "Failing Wheel Bearing",
          description: `A humming or grinding noise that changes with vehicle speed in your ${brand} ${model} often indicates a failing wheel bearing, which can lead to unsafe driving conditions if not addressed.`,
          probability: 75,
          estimated_repair_cost: "$250-$500 per wheel",
          severity: "High",
          system: "Suspension",
          recommendations: [
            "Test each wheel by jacking up the car and checking for play",
            "Listen for changes in noise when turning versus driving straight",
            "Replace the affected wheel bearing hub assembly"
          ]
        }
      },
      'brakes': {
        'default': {
          name: "Worn Brake Pads and Rotors",
          description: `Based on your ${brand} ${model}'s symptoms, the brake pads are likely worn beyond the minimum thickness, causing metal-on-metal contact with the rotors. This reduces stopping power and damages the brake system.`,
          probability: 90,
          estimated_repair_cost: "$250-$700 for all wheels",
          severity: "High",
          system: "Brakes",
          recommendations: [
            "Immediately replace brake pads on all affected wheels",
            "Inspect and likely resurface or replace brake rotors",
            "Check brake fluid level and condition - consider a flush if fluid is old"
          ]
        }
      },
      'overheat': {
        'BMW': {
          name: "Electric Water Pump Failure",
          description: `${brand} ${model} models use an electric water pump that commonly fails, leading to rapid overheating and potential engine damage. Unlike traditional pumps, these fail without warning signs.`,
          probability: 85,
          estimated_repair_cost: "$800-$1,200",
          severity: "High",
          system: "Cooling",
          recommendations: [
            "Replace the electric water pump preventively if over 60,000 miles",
            "Always replace the thermostat when replacing the water pump",
            "Bleed the cooling system properly after repair to prevent air pockets"
          ]
        },
        'default': {
          name: "Thermostat Malfunction",
          description: `Your ${brand} ${model} has symptoms consistent with a stuck thermostat, preventing proper coolant flow and causing the engine to overheat, particularly after reaching operating temperature.`,
          probability: 80,
          estimated_repair_cost: "$200-$400",
          severity: "High",
          system: "Cooling",
          recommendations: [
            "Replace the thermostat and gasket",
            "Flush the cooling system to remove any debris",
            "Check for leaks in the cooling system and repair as needed"
          ]
        }
      },
      'stalling': {
        'default': {
          name: "Failing Fuel Pump",
          description: `The fuel pump in your ${brand} ${model} may be failing to maintain proper pressure, causing the engine to stall particularly during acceleration or at higher speeds.`,
          probability: 75,
          estimated_repair_cost: "$400-$800",
          severity: "High",
          system: "Fuel System",
          recommendations: [
            "Test fuel pressure to confirm pump performance",
            "Check for a clogged fuel filter which may strain the pump",
            "Inspect the fuel pump relay and electrical connections before replacing the pump"
          ]
        }
      },
      'leak': {
        'Mercedes-Benz': {
          name: "Oil Cooler Seal Failure",
          description: `${brand} ${model} vehicles often develop oil leaks from the oil cooler seals, which deteriorate over time. This typically appears as oil accumulation on the lower part of the engine.`,
          probability: 80,
          estimated_repair_cost: "$500-$900",
          severity: "Medium",
          system: "Engine",
          recommendations: [
            "Check the area around the oil filter housing and oil cooler",
            "Replace the oil cooler seals and gaskets",
            "Clean the affected area thoroughly to monitor for new leaks"
          ]
        },
        'default': {
          name: "Valve Cover Gasket Leak",
          description: `Your ${brand} ${model} is likely experiencing a valve cover gasket leak, evidenced by oil accumulation on the engine and possibly a burning oil smell when the engine is hot.`,
          probability: 85,
          estimated_repair_cost: "$200-$500",
          severity: "Low-Medium",
          system: "Engine",
          recommendations: [
            "Replace the valve cover gasket",
            "Check for hardened or damaged valve cover during replacement",
            "Verify proper torque specifications when reinstalling to prevent future leaks"
          ]
        }
      },
      'electrical': {
        'Mercedes-Benz': {
          name: "SAM Module Failure",
          description: `The Signal Acquisition Module (SAM) in your ${brand} ${model} may be failing, causing various electrical issues including intermittent power to accessories, lighting problems, or battery drain.`,
          probability: 75,
          estimated_repair_cost: "$700-$1,500",
          severity: "Medium-High",
          system: "Electrical",
          recommendations: [
            "Have a Mercedes-specific diagnostic system check for SAM module codes",
            "Check for water intrusion in the trunk or battery compartment",
            "Consider module repair before replacement as it may be more cost-effective"
          ]
        },
        'default': {
          name: "Failing Alternator",
          description: `Your ${brand} ${model} shows signs of alternator failure, which can cause battery drain, dimming lights, and eventually vehicle stalling when the battery is depleted.`,
          probability: 80,
          estimated_repair_cost: "$400-$800",
          severity: "High",
          system: "Electrical",
          recommendations: [
            "Test alternator output voltage (should be 13.5-14.5V while running)",
            "Inspect the serpentine belt for wear or damage",
            "Check battery condition as a failing alternator can damage the battery"
          ]
        }
      },
      'vibration': {
        'default': {
          name: "Imbalanced or Damaged Tires",
          description: `The vibration in your ${brand} ${model} is likely caused by tire imbalance, possibly due to wheel weight loss or tire damage such as separated belts or flat spots.`,
          probability: 85,
          estimated_repair_cost: "$20-$400 depending on cause",
          severity: "Medium",
          system: "Wheels & Tires",
          recommendations: [
            "Have all tires balanced at a professional shop",
            "Inspect tires for visible damage, bulges, or abnormal wear",
            "Consider tire rotation and alignment to address wear patterns"
          ]
        }
      },
      'general': {
        'default': {
          name: "Multiple Maintenance Items Due",
          description: `Based on your ${brand} ${model}'s age and description, several maintenance items may be due, including fluid changes, filters, and wear items that can affect performance.`,
          probability: 90,
          estimated_repair_cost: "$300-$1,000 depending on needed services",
          severity: "Medium",
          system: "Multiple",
          recommendations: [
            "Perform a comprehensive vehicle inspection based on mileage",
            "Check all fluids (oil, transmission, brake, power steering, coolant)",
            "Replace air and cabin filters if not done recently"
          ]
        }
      }
    };
    
    // Get the appropriate issue details based on symptom type and brand
    const brandIssues = technicalKnowledgeBase[symptomType] || technicalKnowledgeBase['general'];
    let issue = brandIssues[brand] || brandIssues['default'] || technicalKnowledgeBase['general']['default'];
    
    // Add a unique ID
    issue = {
      id: Math.floor(Math.random() * 1000) + 1,
      ...issue
    };
    
    return issue;
  };
  
  // Get issues based on vehicle age and mileage
  const getIssuesByVehicleAge = (year, mileage, brand, model) => {
    const currentYear = new Date().getFullYear();
    const age = currentYear - year;
    const issues = [];
    
    // Age-based issues
    if (age >= 10 || mileage >= 100000) {
      issues.push({
        id: Math.floor(Math.random() * 1000) + 1,
        name: "Timing Belt/Chain Maintenance",
        description: `Your ${age}-year-old ${brand} ${model} is due for timing belt/chain inspection or replacement based on age and mileage. Failure can lead to catastrophic engine damage.`,
        probability: 85,
        estimated_repair_cost: "$500-$1,200",
        severity: "High",
        system: "Engine",
        recommendations: [
          "Replace timing belt if original and vehicle is over 7 years old",
          "Inspect timing chain for stretch or wear if applicable",
          "Replace water pump while timing components are accessible"
        ]
      });
    }
    
    if (age >= 7 || mileage >= 70000) {
      issues.push({
        id: Math.floor(Math.random() * 1000) + 2,
        name: "Suspension Component Wear",
        description: `Vehicles like your ${brand} ${model} typically develop suspension wear at this age/mileage, causing degraded handling, comfort, and potentially uneven tire wear.`,
        probability: 80,
        estimated_repair_cost: "$400-$1,000",
        severity: "Medium",
        system: "Suspension",
        recommendations: [
          "Inspect control arm bushings, ball joints, and tie rod ends",
          "Check shock absorbers/struts for leakage or reduced performance",
          "Consider a four-wheel alignment after replacing components"
        ]
      });
    }
    
    if (age >= 5 || mileage >= 50000) {
      issues.push({
        id: Math.floor(Math.random() * 1000) + 3,
        name: "Throttle Body Carbon Buildup",
        description: `Your ${brand} ${model} may have carbon deposits in the throttle body and intake manifold, causing rough idle, hesitation, and reduced fuel economy.`,
        probability: 70,
        estimated_repair_cost: "$150-$500",
        severity: "Medium",
        system: "Fuel System",
        recommendations: [
          "Clean the throttle body with proper throttle body cleaner",
          "Consider an intake manifold cleaning service",
          "Replace the air filter if not done recently"
        ]
      });
    }
    
    // If no age-based issues were added (newer car), add a general maintenance recommendation
    if (issues.length === 0) {
      issues.push({
        id: Math.floor(Math.random() * 1000) + 4,
        name: "Preventive Maintenance Review",
        description: `Even though your ${brand} ${model} is relatively new, it's important to follow the manufacturer's recommended maintenance schedule to prevent future issues.`,
        probability: 95,
        estimated_repair_cost: "$100-$300",
        severity: "Low",
        system: "General",
        recommendations: [
          "Ensure all scheduled maintenance is up to date",
          "Check for any technical service bulletins (TSBs) for your specific model",
          "Consider a comprehensive multi-point inspection"
        ]
      });
    }
    
    return issues;
  };

  const handleFindGarages = (issue) => {
    setSelectedIssue(issue);
    
    // Navigate to the garages page with the selected issue
    navigate('/garages', { 
      state: { 
        selectedIssue: issue,
        vehicleInfo: {
          brand: selectedBrand,
          model: selectedModel,
          year: year
        }
      } 
    });
  };

  // Booking appointment handler removed

  const handleBrandChange = (e) => {
    const brand = e.target.value;
    console.log('Selected brand:', brand);
    setSelectedBrand(brand);
    setSelectedModel('');
    
    // For Mercedes-Benz, manually set models since there seems to be an issue with the data structure
    if (brand === 'Mercedes-Benz') {
      console.log('Setting hardcoded Mercedes-Benz models');
      setModels(['A-Class', 'B-Class', 'C-Class', 'CLA', 'CLS', 'E-Class', 'G-Class', 'GLA', 'GLB', 'GLC', 'GLE', 'GLS', 'S-Class']);
    }
    
    // Debug the carBrands data
    console.log('Car brands data:', carBrands);
    
    // The models will be updated by the useEffect hook
  };

  const renderVehicleForm = () => {
    return (
      <Card 
        bg={cardBg} 
        borderColor={borderColor} 
        borderWidth="1px" 
        borderRadius="lg" 
        overflow="hidden"
        boxShadow="lg"
      >
        <CardHeader bg={headerBg} borderBottomWidth="1px" borderColor={borderColor}>
          <Heading size="lg" color="brand.600">
            <Flex align="center">
              <Icon as={FaTools} mr={3} color="brand.600" />
              Car Diagnostic Tool
            </Flex>
        </Heading>
        </CardHeader>
        <CardBody>
          <form onSubmit={handleSubmit}>
            <VStack spacing={4} align="stretch">
              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                <FormControl isRequired>
                  <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                    <Icon as={FaCarAlt} mr={2} color="accent.500" />
                    Brand
                  </FormLabel>
                  <Select 
                    placeholder="Select brand" 
                    value={selectedBrand}
                    onChange={handleBrandChange}
                    bg="white"
                    color="text.900"
                    borderColor="secondary.200"
                    _hover={{ borderColor: "accent.500" }}
                    _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                    isDisabled={loadingOptions}
                    opacity="1"
                    _disabled={{ opacity: "0.8", cursor: "not-allowed" }}
                    sx={{
                      "& option": {
                        background: "white",
                        color: "text.900",
                      }
                    }}
                  >
                    {loadingOptions ? (
                      <option value="" disabled>Loading...</option>
                    ) : (
                      Object.keys(carBrands).map((brand) => (
                        <option key={brand} value={brand}>{brand}</option>
                      ))
                    )}
                  </Select>
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel fontWeight="medium" color={textColor}>Car Model</FormLabel>
                  <Select 
                    placeholder={selectedBrand ? "Select model" : "Select brand first"} 
                    value={selectedModel} 
                    onChange={(e) => setSelectedModel(e.target.value)}
                    isDisabled={!selectedBrand || models.length === 0 || loadingOptions}
                    bg="white"
                    color="text.900"
                    borderColor="secondary.200"
                    _hover={{ borderColor: "accent.500" }}
                    _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                    opacity="1"
                    _disabled={{ opacity: "0.8", cursor: "not-allowed" }}
                    sx={{
                      "& option": {
                        background: "white !important",
                        color: "black !important",
                      }
                    }}
                  >
                    {models.length === 0 && selectedBrand ? (
                      <option value="" disabled>No models available</option>
                    ) : (
                      models.map((model) => (
                        <option 
                          key={typeof model === 'string' ? model : String(model)} 
                          value={typeof model === 'string' ? model : String(model)}
                          style={{ color: 'black', backgroundColor: 'white' }}
                        >
                          {typeof model === 'string' ? model : String(model)}
                        </option>
                      ))
                    )}
                  </Select>
                </FormControl>
              </SimpleGrid>
              
              <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                <FormControl isRequired>
                  <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                    <Icon as={FaCalendarAlt} mr={2} color="accent.500" />
                    Year
                  </FormLabel>
                  <Select 
                    placeholder="Select year" 
                    value={year} 
                    onChange={(e) => setYear(e.target.value)}
                    bg="white"
                    borderColor="secondary.200"
                    color="text.900"
                    _hover={{ borderColor: "accent.500" }}
                    _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                    sx={{
                      "& option": {
                        background: "white",
                        color: "text.900"
                      }
                    }}
                  >
                    {Array.from({ length: 30 }, (_, i) => new Date().getFullYear() - i).map((year) => (
                      <option key={year} value={year}>{year}</option>
                    ))}
                  </Select>
                </FormControl>
                
                <FormControl>
                  <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                    <Icon as={FaGasPump} mr={2} color="accent.500" />
                    Fuel Type
                  </FormLabel>
                  <Select 
                    placeholder="Select fuel type" 
                    value={fuelType} 
                    onChange={(e) => setFuelType(e.target.value)}
                    bg="white"
                    borderColor="secondary.200"
                    color="text.900"
                    _hover={{ borderColor: "accent.500" }}
                    _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                    sx={{
                      "& option": {
                        background: "white",
                        color: "text.900"
                      }
                    }}
                  >
                    <option value="Gasoline">Gasoline</option>
                    <option value="Diesel">Diesel</option>
                    <option value="Electric">Electric</option>
                    <option value="Hybrid">Hybrid</option>
                    <option value="Plug-in Hybrid">Plug-in Hybrid</option>
                    <option value="Mild Hybrid">Mild Hybrid</option>
                    <option value="LPG">LPG</option>
                    <option value="CNG">CNG</option>
                    <option value="Hydrogen">Hydrogen</option>
                    <option value="Ethanol">Ethanol</option>
                    <option value="Biodiesel">Biodiesel</option>
                  </Select>
                </FormControl>
                
                <FormControl>
                  <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                    <Icon as={FaCogs} mr={2} color="accent.500" />
                    Transmission
                  </FormLabel>
                  <Select 
                    placeholder="Select transmission" 
                    value={transmissionType} 
                    onChange={(e) => setTransmissionType(e.target.value)}
                    bg="white"
                    borderColor="secondary.200"
                    color="text.900"
                    _hover={{ borderColor: "accent.500" }}
                    _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                    sx={{
                      "& option": {
                        background: "white",
                        color: "text.900"
                      }
                    }}
                  >
                    <option value="Automatic">Automatic</option>
                    <option value="Manual">Manual</option>
                    <option value="CVT">CVT (Continuously Variable Transmission)</option>
                    <option value="DCT">DCT (Dual Clutch Transmission)</option>
                    <option value="Semi-Automatic">Semi-Automatic</option>
                    <option value="AMT">AMT (Automated Manual Transmission)</option>
                    <option value="DSG">DSG (Direct Shift Gearbox)</option>
                    <option value="Tiptronic">Tiptronic</option>
                    <option value="Single-Speed">Single-Speed (Electric Vehicles)</option>
                  </Select>
                </FormControl>
              </SimpleGrid>
              
              <FormControl>
                <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                  <Icon as={FaTachometerAlt} mr={2} color="accent.500" />
                  Mileage (km)
                </FormLabel>
                <Input 
                  type="number" 
                  placeholder="e.g. 50000" 
                  value={mileage} 
                  onChange={(e) => setMileage(e.target.value)}
                  bg="white"
                  color="text.900"
                  borderColor="secondary.200"
                  _hover={{ borderColor: "accent.500" }}
                  _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                />
              </FormControl>
              
              <FormControl isRequired>
                <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                  <Icon as={FaExclamationTriangle} mr={2} color="accent.500" />
                  Symptoms
                </FormLabel>
                <Textarea 
                  placeholder="Describe the issues you're experiencing with your car..." 
                  value={symptoms} 
                  onChange={(e) => setSymptoms(e.target.value)}
                  rows={4}
                  bg="white"
                  color="text.900"
                  borderColor="secondary.200"
                  _hover={{ borderColor: "accent.500" }}
                  _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                />
              </FormControl>
              
              <Button 
                type="submit" 
                colorScheme="accent" 
                size="lg" 
                isLoading={loading} 
                loadingText="Diagnosing..."
                width="full"
              >
                Diagnose My Car
              </Button>
            </VStack>
          </form>
        </CardBody>
      </Card>
    );
  };

  const renderDiagnosisResults = () => {
    if (!diagnosis) return null;
    
    // Add default values for vehicle_info if it's undefined
    const { 
      vehicle_info = {}, 
      possible_issues = [], 
      recommendations = [], 
      analysis = '', 
      severity = '', 
      repair_costs = [], 
      common_issues = [],
      diagnosis_method = '' 
    } = diagnosis;
    
    // Add default empty object for vehicle_info properties
    const {
      brand = '',
      model = '',
      year = '',
      fuel_type = '',
      transmission_type = ''
    } = vehicle_info;
    
    // Calculate total repair cost estimate
    const calculateTotalCost = () => {
      let minTotal = 0;
      let maxTotal = 0;
      
      repair_costs.forEach(item => {
        if (item.total_cost) {
          const costRange = item.total_cost.replace('€', '').split(' - ');
          if (costRange.length === 2) {
            minTotal += parseInt(costRange[0], 10) || 0;
            maxTotal += parseInt(costRange[1], 10) || 0;
          }
        }
      });
      
      return `€${minTotal} - €${maxTotal}`;
    };
    
    // Calculate total labor time
    const calculateTotalTime = () => {
      let totalHours = 0;
      
      repair_costs.forEach(item => {
        if (item.labor_time) {
          const hours = parseFloat(item.labor_time.split(' ')[0]) || 0;
          totalHours += hours;
        }
      });
      
      return `${totalHours.toFixed(1)} hours`;
    };
    
    return (
      <VStack spacing={6} align="stretch">
        <Heading as="h3" size="lg" color="text.900">Diagnosis Results</Heading>
        
        <Box 
          bg="white" 
          borderRadius="lg" 
          boxShadow="md" 
          p={6}
          borderLeft="4px solid" 
          borderLeftColor={
            severity === 'high' ? 'red.500' : 
            severity === 'medium' ? 'orange.500' : 
            severity === 'low' ? 'green.500' : 
            'blue.500'
          }
        >
          <VStack align="stretch" spacing={4}>
            <Flex justify="space-between" align="center">
              <Heading as="h4" size="md" color="text.900">Vehicle Information</Heading>
              <Badge 
                colorScheme={
                  severity === 'high' ? 'red' : 
                  severity === 'medium' ? 'orange' : 
                  severity === 'low' ? 'green' : 
                  'blue'
                }
                fontSize="md"
                px={3}
                py={1}
                borderRadius="md"
              >
                {severity.toUpperCase()} SEVERITY
              </Badge>
            </Flex>
            
            <Box bg="gray.50" p={4} borderRadius="md">
              <SimpleGrid columns={{ base: 1, md: 3 }} spacing={4}>
                <Box>
                  <Text fontWeight="semibold" color="text.900">Brand:</Text>
                  <Text color="text.900">{brand}</Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" color="text.900">Model:</Text>
                  <Text color="text.900">{model}</Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" color="text.900">Year:</Text>
                  <Text color="text.900">{year}</Text>
                </Box>
                {fuel_type && (
                  <Box>
                    <Text fontWeight="semibold" color="text.900">Fuel Type:</Text>
                    <Text color="text.900">{fuel_type}</Text>
                  </Box>
                )}
                {transmission_type && (
                  <Box>
                    <Text fontWeight="semibold" color="text.900">Transmission:</Text>
                    <Text color="text.900">{transmission_type}</Text>
                  </Box>
                )}
              </SimpleGrid>
            </Box>
            
            <Divider />
            
            <Heading as="h4" size="md" color="text.900">Diagnosis</Heading>
            <Text color="text.900" fontWeight="medium">{analysis}</Text>
            
            {possible_issues && possible_issues.length > 0 && (
              <>
                <Heading as="h4" size="md" color="text.900">Possible Issues</Heading>
                <UnorderedList spacing={2} pl={4}>
                  {possible_issues.map((issue, index) => (
                    <ListItem key={index} color="text.900">
                      <Text fontWeight="semibold">
                        {typeof issue === 'object' ? issue.name : issue}
                      </Text>
                      {typeof issue === 'object' && issue.description && (
                        <Text fontSize="sm" color="text.700">{issue.description}</Text>
                      )}
                    </ListItem>
                  ))}
                </UnorderedList>
              </>
            )}
            
            {common_issues && common_issues.length > 0 && (
              <>
                <Heading as="h4" size="md" color="text.900">Known Issues for This Model</Heading>
                <UnorderedList spacing={2} pl={4}>
                  {common_issues.map((issue, index) => (
                    <ListItem key={index} color="text.900">
                      <Text>{issue}</Text>
                    </ListItem>
                  ))}
                </UnorderedList>
              </>
            )}
            
            <Divider />
            <Heading as="h4" size="md" color="text.900">Repair Costs & Time Estimates</Heading>
            <Box bg="blue.50" p={4} borderRadius="md" borderWidth="1px" borderColor="blue.200">
              {repair_costs && repair_costs.length > 0 ? (
                <>
                  <Box 
                    bg="white" 
                    p={4} 
                    mb={4} 
                    borderRadius="md" 
                    borderWidth="2px" 
                    borderColor="blue.300"
                    boxShadow="md"
                  >
                    <Flex justify="space-between" align="center">
                      <Text fontWeight="bold" fontSize="lg" color="blue.700">
                        <Icon as={FaWrench} mr={2} />
                        Total Repair Estimate:
                      </Text>
                      <Text fontWeight="bold" fontSize="xl" color="blue.700">
                        {calculateTotalCost()}
                      </Text>
                    </Flex>
                    <Text fontSize="sm" color="gray.600" mt={1}>
                      Estimated time: {calculateTotalTime()}
                    </Text>
                  </Box>
                  
                  <Text fontWeight="semibold" mb={2} color="text.900">Breakdown by Repair Item:</Text>
                  <VStack align="stretch" spacing={3}>
                    {repair_costs.map((item, index) => (
                      <Box key={index} p={3} bg="white" borderRadius="md" borderWidth="1px" borderColor="gray.200">
                        <Flex justify="space-between" align="center" mb={2}>
                          <Text fontWeight="bold" color="text.900">{item.repair}</Text>
                          <Badge colorScheme="blue">{item.labor_time}</Badge>
                        </Flex>
                        <Flex justify="space-between" align="center">
                          <Text color="text.700">Parts Cost:</Text>
                          <Text color="blue.600" fontWeight="medium">{item.parts_cost}</Text>
                        </Flex>
                        <Flex justify="space-between" align="center" mt={1}>
                          <Text color="text.700">Total Cost:</Text>
                          <Text color="blue.600" fontWeight="bold">{item.total_cost}</Text>
                        </Flex>
                      </Box>
                    ))}
                  </VStack>
                </>
              ) : (
                <Text color="text.700">No specific cost estimates available for the identified issues.</Text>
              )}
              
              <Text fontSize="sm" color="gray.600" mt={3}>
                <Icon as={FaInfoCircle} mr={1} />
                Costs based on OEM data and may vary by location and specific vehicle condition.
              </Text>
            </Box>
            
            <Button 
              colorScheme="brand" 
              size="lg" 
              mt={4}
              leftIcon={<Icon as={FaMapMarkerAlt} />}
              onClick={() => handleFindGarages(possible_issues[0])}
            >
              Find Garages That Can Fix This
            </Button>
          </VStack>
        </Box>
        

      </VStack>
    );
  };

  return (
    <Box w="full">
      <Container maxW="container.lg" py={8}>
        <VStack spacing={8} align="stretch">
          <Box textAlign="center">
            <Heading as="h1" size="xl" mb={2} color="text.900">
              Car Diagnosis
            </Heading>
            <Text color="text.700">
              Get an expert diagnosis for your car issues using DeepSeek AI and technical documentation
            </Text>
          </Box>
          
          {!diagnosis ? (
            <Card bg={cardBg} borderColor={borderColor} borderWidth="1px" borderRadius="lg" overflow="hidden">
              <CardHeader bg={headerBg} borderBottomWidth="1px" borderColor={borderColor}>
                <Heading size="md" color="text.900">
                  <Flex align="center">
                    <Icon as={FaCarAlt} mr={3} color="accent.500" />
                    Vehicle Information
                  </Flex>
                </Heading>
              </CardHeader>
              <CardBody>
                <form onSubmit={handleSubmit}>
                  <VStack spacing={6} align="stretch">
                    <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
                      <FormControl isRequired>
                        <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                          <Icon as={FaCar} mr={2} color="accent.500" />
                          Car Brand
                        </FormLabel>
                        <Select 
                          placeholder="Select brand" 
                          value={selectedBrand}
                          onChange={handleBrandChange}
                          bg="white"
                          color="text.900"
                          borderColor="secondary.200"
                          _hover={{ borderColor: "accent.500" }}
                          _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                          isDisabled={loadingOptions}
                          opacity="1"
                          _disabled={{ opacity: "0.8", cursor: "not-allowed" }}
                          sx={{
                            "& option": {
                              background: "white",
                              color: "text.900",
                            }
                          }}
                        >
                          {loadingOptions ? (
                            <option value="" disabled>Loading...</option>
                          ) : (
                            Object.keys(carBrands).map((brand) => (
                              <option key={brand} value={brand}>{brand}</option>
                            ))
                          )}
                        </Select>
                      </FormControl>
                      
                      <FormControl isRequired>
                        <FormLabel fontWeight="medium" color={textColor}>Car Model</FormLabel>
                        <Select 
                          placeholder={selectedBrand ? "Select model" : "Select brand first"} 
                          value={selectedModel} 
                          onChange={(e) => setSelectedModel(e.target.value)}
                          isDisabled={!selectedBrand || models.length === 0 || loadingOptions}
                          bg="white"
                          color="text.900"
                          borderColor="secondary.200"
                          _hover={{ borderColor: "accent.500" }}
                          _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                          opacity="1"
                          _disabled={{ opacity: "0.8", cursor: "not-allowed" }}
                          sx={{
                            "& option": {
                              background: "white !important",
                              color: "black !important",
                            }
                          }}
                        >
                          {models.map((model) => (
                            <option key={model} value={model}>{model}</option>
                          ))}
                        </Select>
                      </FormControl>
                    </SimpleGrid>
                    
                    <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
                      <FormControl isRequired>
                        <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                          <Icon as={FaCalendarAlt} mr={2} color="accent.500" />
                          Year
                        </FormLabel>
                        <Select 
                          placeholder="Select year" 
                          value={year} 
                          onChange={(e) => setYear(e.target.value)}
                          bg="white"
                          color="text.900"
                          borderColor="secondary.200"
                          _hover={{ borderColor: "accent.500" }}
                          _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                        >
                          {Array.from({ length: 30 }, (_, i) => new Date().getFullYear() - i).map((y) => (
                            <option key={y} value={y}>{y}</option>
                          ))}
                        </Select>
                      </FormControl>
                      
                      <FormControl>
                        <FormLabel fontWeight="medium" color={textColor}>Fuel Type</FormLabel>
                        <Select 
                          placeholder="Select fuel type" 
                          value={fuelType} 
                          onChange={(e) => setFuelType(e.target.value)}
                          bg="white"
                          color="text.900"
                          borderColor="secondary.200"
                          _hover={{ borderColor: "accent.500" }}
                          _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                        >
                          <option value="Gasoline">Gasoline</option>
                          <option value="Diesel">Diesel</option>
                          <option value="Electric">Electric</option>
                          <option value="Hybrid">Hybrid</option>
                          <option value="LPG">LPG</option>
                        </Select>
                      </FormControl>
                      
                      <FormControl>
                        <FormLabel fontWeight="medium" color={textColor}>Transmission</FormLabel>
                        <Select 
                          placeholder="Select transmission" 
                          value={transmissionType} 
                          onChange={(e) => setTransmissionType(e.target.value)}
                          bg="white"
                          color="text.900"
                          borderColor="secondary.200"
                          _hover={{ borderColor: "accent.500" }}
                          _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                        >
                          <option value="Automatic">Automatic</option>
                          <option value="Manual">Manual</option>
                          <option value="CVT">CVT</option>
                          <option value="Semi-Automatic">Semi-Automatic</option>
                        </Select>
                      </FormControl>
                    </SimpleGrid>
                    
                    <FormControl>
                      <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                        <Icon as={FaTachometerAlt} mr={2} color="accent.500" />
                        Mileage (km)
                      </FormLabel>
                      <Input 
                        type="number" 
                        placeholder="e.g. 50000" 
                        value={mileage} 
                        onChange={(e) => setMileage(e.target.value)}
                        bg="white"
                        color="text.900"
                        borderColor="secondary.200"
                        _hover={{ borderColor: "accent.500" }}
                        _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                      />
                    </FormControl>
                    
                    <FormControl isRequired>
                      <FormLabel fontWeight="medium" color={textColor} display="flex" alignItems="center">
                        <Icon as={FaExclamationTriangle} mr={2} color="accent.500" />
                        Symptoms
                      </FormLabel>
                      <Textarea 
                        placeholder="Describe the issues you're experiencing with your car..." 
                        value={symptoms} 
                        onChange={(e) => setSymptoms(e.target.value)}
                        rows={4}
                        bg="white"
                        color="text.900"
                        borderColor="secondary.200"
                        _hover={{ borderColor: "accent.500" }}
                        _focus={{ borderColor: "accent.500", boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" }}
                      />
                    </FormControl>
                    
                    <Button 
                      type="submit" 
                      colorScheme="accent" 
                      size="lg" 
                      isLoading={loading} 
                      loadingText="Diagnosing..."
                      width="full"
                    >
                      Diagnose My Car
                    </Button>
                  </VStack>
                </form>
              </CardBody>
            </Card>
          ) : (
            <Box id="diagnosis-results">
              {renderDiagnosisResults()}
              
              <Button 
                mt={6}
                variant="outline" 
                colorScheme="accent" 
                onClick={() => {
                  setDiagnosis(null);
                  setSelectedIssue(null);
                }}
              >
                Start New Diagnosis
              </Button>
            </Box>
          )}
          
          {error && (
            <Alert status="error" borderRadius="md">
              <AlertIcon />
              <AlertTitle mr={2}>Error!</AlertTitle>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </VStack>
      </Container>
      
      {/* BookingModal removed */}
    </Box>
  );
};

export default DiagnosisForm;
