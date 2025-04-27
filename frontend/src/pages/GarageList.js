import React, { useState, useEffect } from 'react';
import {
  Box,
  VStack,
  Heading,
  Text,
  Container,
  Card,
  CardBody,
  Link,
  Spinner,
  Alert,
  AlertIcon,
  SimpleGrid,
  Icon,
  Flex,
  Button,
  Divider,
  useColorModeValue,
  CardHeader,
  Input,
  InputGroup,
  InputLeftElement,
  Wrap,
  WrapItem,
  Tag,
  Badge,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  useBreakpointValue
} from '@chakra-ui/react';
import { 
  FaMapMarkerAlt, 
  FaPhone, 
  FaClock, 
  FaTools, 
  FaExternalLinkAlt, 
  FaSearch,
  FaStar,
  FaRoute,
  FaPhoneAlt,
  FaDirections,
  FaCalendarCheck,
  FaArrowLeft
} from 'react-icons/fa';
import axios from 'axios';
import config from '../config';
import { useLocation, useNavigate } from 'react-router-dom';
import BookingModal from '../components/BookingModal';

const GarageCard = ({ garage, onBookAppointment }) => {
  const cardBg = 'white';
  const borderColor = 'secondary.200';
  const headerBg = 'secondary.50';
  const textColor = 'text.900';
  const mutedTextColor = 'text.700';
  const isMobile = useBreakpointValue({ base: true, md: false });
  
  return (
    <Card 
      variant="outline" 
      bg={cardBg} 
      borderColor={borderColor}
      shadow="md"
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-5px)', shadow: 'lg' }}
      height="100%"
      cursor="pointer"
      onClick={() => onBookAppointment(garage)}
    >
      <CardHeader 
        bg={headerBg}
        borderBottomWidth="1px" 
        borderColor={borderColor}
        pb={3}
        p={isMobile ? 3 : 5}
      >
        <Heading size="md" noOfLines={1} color="text.900">{garage.name}</Heading>
        {garage.distance && (
          <Flex align="center" mt={2}>
            <Icon as={FaRoute} color="brand.600" mr={1} />
            <Text fontWeight="medium" color="brand.600">
              {garage.distance} km away
            </Text>
          </Flex>
        )}
      </CardHeader>
      <CardBody p={isMobile ? 3 : 5}>
        <VStack align="stretch" spacing={4}>
          <Flex align="flex-start">
            <Box 
              bg="accent.500" 
              p={2} 
              borderRadius="full" 
              display="inline-flex"
              mr={2}
              flexShrink={0}
            >
              <Icon as={FaMapMarkerAlt} color="white" />
            </Box>
            <Text color={textColor} fontSize={isMobile ? "sm" : "md"}>{garage.address}</Text>
          </Flex>
          
          <Flex align="flex-start">
            <Box 
              bg="brand.600" 
              p={2} 
              borderRadius="full" 
              display="inline-flex"
              mr={2}
              flexShrink={0}
            >
              <Icon as={FaPhone} color="white" />
            </Box>
            <Text color={textColor} fontSize={isMobile ? "sm" : "md"}>{garage.phone}</Text>
          </Flex>
          
          <Flex align="flex-start">
            <Box 
              bg="secondary.600" 
              p={2} 
              borderRadius="full" 
              display="inline-flex"
              mr={2}
              flexShrink={0}
            >
              <Icon as={FaClock} color="white" />
            </Box>
            <VStack align="stretch" spacing={0}>
              <Text fontWeight="medium" color={textColor} fontSize={isMobile ? "sm" : "md"}>Opening Hours</Text>
              <Text color={mutedTextColor} fontSize={isMobile ? "xs" : "sm"}>{garage.hours}</Text>
            </VStack>
          </Flex>
          
          <Flex mt={1} justify="space-between" align="center">
            <Flex>
              {Array(5).fill('').map((_, i) => (
                <Icon
                  key={i}
                  as={FaStar}
                  color={i < garage.rating ? "accent.500" : "gray.300"}
                  mr={1}
                />
              ))}
            </Flex>
            <Button 
              rightIcon={<FaCalendarCheck />} 
              colorScheme="brand" 
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                onBookAppointment(garage);
              }}
            >
              Book
            </Button>
          </Flex>
          
          <Wrap spacing={2} mt={2}>
            {garage.services?.map((service, index) => (
              <WrapItem key={index}>
                <Tag size="sm" colorScheme="secondary" borderRadius="full">
                  {service}
                </Tag>
              </WrapItem>
            ))}
          </Wrap>
        </VStack>
      </CardBody>
    </Card>
  );
};

const GarageList = () => {
  const [garages, setGarages] = useState([]);
  const [filteredGarages, setFilteredGarages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedGarage, setSelectedGarage] = useState(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const location = useLocation();
  const navigate = useNavigate();
  
  // Responsive layout adjustments
  const isMobile = useBreakpointValue({ base: true, md: false });
  const containerPadding = useBreakpointValue({ base: 4, md: 8 });
  const headingSize = useBreakpointValue({ base: "lg", md: "xl" });
  
  // Extract any selected issue from the location state
  const selectedIssue = location.state?.issue;
  const vehicleInfo = location.state?.vehicle;

  useEffect(() => {
    const fetchGarages = async () => {
      try {
        const response = await axios.get(`${config.API_BASE_URL}${config.ENDPOINTS.GARAGES}`);
        if (response.data && Array.isArray(response.data)) {
          const garageData = response.data;
          setGarages(garageData);
          setFilteredGarages(garageData);
        } else {
          // If API fails, use mock data
          const mockData = getMockGarages();
          setGarages(mockData);
          setFilteredGarages(mockData);
        }
        setLoading(false);
      } catch (err) {
        console.error('Error fetching garages:', err);
        // Use mock data as fallback
        const mockData = getMockGarages();
        setGarages(mockData);
        setFilteredGarages(mockData);
        setLoading(false);
      }
    };
    
    fetchGarages();
  }, []);
  
  // Mock data function for fallback
  const getMockGarages = () => {
    return [
      {
        id: 1,
        name: "AutoTech Garage",
        address: "123 Main Street, Luxembourg City",
        phone: "+352 123 456 789",
        website: "https://autotech.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-14:00",
        rating: 4,
        distance: 2.3,
        services: ["Engine Repair", "Brake Service", "Oil Change", "Diagnostics"],
        latitude: 49.611622,
        longitude: 6.132263
      },
      {
        id: 2,
        name: "EuroCar Service",
        address: "45 Avenue de la Liberté, Luxembourg",
        phone: "+352 987 654 321",
        website: "https://eurocar.lu",
        hours: "Mon-Fri: 8:30-18:30, Sat: 9:00-15:00",
        rating: 5,
        distance: 3.1,
        services: ["Transmission Repair", "Electrical Systems", "AC Service", "Tire Replacement"],
        latitude: 49.600750,
        longitude: 6.125790
      },
      {
        id: 3,
        name: "Premium Auto Care",
        address: "78 Route d'Esch, Luxembourg",
        phone: "+352 456 789 123",
        website: "https://premiumauto.lu",
        hours: "Mon-Fri: 8:00-19:00, Sat: 10:00-16:00",
        rating: 4,
        distance: 1.7,
        services: ["Luxury Car Service", "Performance Tuning", "Body Work", "Detailing"],
        latitude: 49.590150,
        longitude: 6.122560
      },
      {
        id: 4,
        name: "Garage Moderne",
        address: "12 Rue de Bonnevoie, Luxembourg",
        phone: "+352 321 654 987",
        website: "https://garagemoderne.lu",
        hours: "Mon-Fri: 7:30-18:00, Sat: 8:30-13:00",
        rating: 3,
        distance: 4.2,
        services: ["General Repairs", "Inspection Service", "Battery Replacement", "Wheel Alignment"],
        latitude: 49.605230,
        longitude: 6.129870
      },
      {
        id: 5,
        name: "LuxAuto Service",
        address: "56 Boulevard Royal, Luxembourg",
        phone: "+352 789 123 456",
        website: "https://luxauto.lu",
        hours: "Mon-Fri: 8:00-18:30, Sat: 9:00-14:30",
        rating: 5,
        distance: 2.8,
        services: ["Electric Vehicle Service", "Hybrid Repairs", "Computer Diagnostics", "Suspension Work"],
        latitude: 49.612340,
        longitude: 6.127650
      },
      {
        id: 6,
        name: "City Garage Luxembourg",
        address: "34 Avenue de la Gare, Luxembourg",
        phone: "+352 654 321 987",
        website: "https://citygarage.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-13:00",
        rating: 4,
        distance: 3.5,
        services: ["Full Service", "Quick Oil Change", "Brake Repair", "Engine Diagnostics"],
        latitude: 49.599870,
        longitude: 6.133420
      },
      {
        id: 7,
        name: "Mécanique Express",
        address: "22 Rue de Hollerich, Luxembourg",
        phone: "+352 277 889 123",
        website: "https://mecaniqueexpress.lu",
        hours: "Mon-Fri: 7:00-19:00, Sat: 8:00-16:00",
        rating: 4,
        distance: 2.9,
        services: ["Express Service", "Brake Repair", "Suspension", "Diagnostics"],
        latitude: 49.603450,
        longitude: 6.128760
      },
      {
        id: 8,
        name: "Auto Elite",
        address: "88 Boulevard de la Pétrusse, Luxembourg",
        phone: "+352 445 678 912",
        website: "https://autoelite.lu",
        hours: "Mon-Fri: 8:30-18:00, Sat: 9:00-15:00",
        rating: 5,
        distance: 3.7,
        services: ["Luxury Vehicles", "Performance Tuning", "Custom Work", "Detailing"],
        latitude: 49.608720,
        longitude: 6.126540
      },
      {
        id: 9,
        name: "Garage Central",
        address: "15 Avenue Monterey, Luxembourg",
        phone: "+352 661 234 567",
        website: "https://garagecentral.lu",
        hours: "Mon-Fri: 8:00-18:30, Sat: 9:00-14:00",
        rating: 4,
        distance: 1.5,
        services: ["General Repairs", "Tire Service", "Air Conditioning", "Electrical Systems"],
        latitude: 49.610230,
        longitude: 6.129870
      },
      {
        id: 10,
        name: "Technik Auto Center",
        address: "42 Rue de Beggen, Luxembourg",
        phone: "+352 691 345 678",
        website: "https://technikauto.lu",
        hours: "Mon-Fri: 7:30-18:30, Sat: 8:30-13:30",
        rating: 3,
        distance: 5.1,
        services: ["German Cars Specialist", "Computer Diagnostics", "Engine Repair", "Transmission"],
        latitude: 49.633450,
        longitude: 6.137690
      },
      {
        id: 11,
        name: "Rapid Service Garage",
        address: "33 Route d'Arlon, Strassen",
        phone: "+352 671 234 567",
        website: "https://rapidservice.lu",
        hours: "Mon-Fri: 7:00-20:00, Sat: 8:00-17:00",
        rating: 4,
        distance: 6.2,
        services: ["Quick Service", "Oil Change", "Brake Service", "Battery Replacement"],
        latitude: 49.620780,
        longitude: 6.097650
      },
      {
        id: 12,
        name: "Auto Precision",
        address: "77 Rue de Gasperich, Luxembourg",
        phone: "+352 621 987 654",
        website: "https://autoprecision.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-13:00",
        rating: 5,
        distance: 4.8,
        services: ["Precision Tuning", "Performance Upgrades", "Custom Exhaust", "ECU Programming"],
        latitude: 49.589760,
        longitude: 6.123450
      },
      {
        id: 13,
        name: "Garage Excellence",
        address: "12 Rue Edward Steichen, Luxembourg",
        phone: "+352 661 876 543",
        website: "https://excellence-garage.lu",
        hours: "Mon-Fri: 8:30-18:30, Sat: 9:00-15:00",
        rating: 5,
        distance: 7.3,
        services: ["Luxury Cars", "Premium Service", "Detailing", "Custom Modifications"],
        latitude: 49.629870,
        longitude: 6.159760
      },
      {
        id: 14,
        name: "Eco Garage",
        address: "55 Rue de Cessange, Luxembourg",
        phone: "+352 691 234 987",
        website: "https://ecogarage.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-14:00",
        rating: 4,
        distance: 3.9,
        services: ["Hybrid Specialist", "Electric Vehicle Service", "Eco-Friendly Repairs", "Battery Service"],
        latitude: 49.596540,
        longitude: 6.119870
      },
      {
        id: 15,
        name: "Classic Car Workshop",
        address: "28 Route de Longwy, Bertrange",
        phone: "+352 621 345 678",
        website: "https://classiccarworkshop.lu",
        hours: "Mon-Fri: 9:00-17:00, Sat: By appointment",
        rating: 5,
        distance: 8.2,
        services: ["Classic Car Restoration", "Vintage Repairs", "Custom Parts", "Collector Vehicles"],
        latitude: 49.611230,
        longitude: 6.089760
      },
      {
        id: 16,
        name: "Moto & Auto Service",
        address: "67 Route de Thionville, Luxembourg",
        phone: "+352 671 876 543",
        website: "https://motoauto.lu",
        hours: "Mon-Fri: 8:00-18:30, Sat: 9:00-16:00",
        rating: 4,
        distance: 5.7,
        services: ["Motorcycle Repair", "Car Service", "Tire Mounting", "Performance Tuning"],
        latitude: 49.587650,
        longitude: 6.142340
      },
      {
        id: 17,
        name: "Total Car Care",
        address: "19 Rue de Neudorf, Luxembourg",
        phone: "+352 661 432 987",
        website: "https://totalcarcare.lu",
        hours: "Mon-Fri: 7:30-19:00, Sat: 8:30-16:00",
        rating: 4,
        distance: 4.3,
        services: ["Complete Service", "Body Work", "Paint Jobs", "Interior Repair"],
        latitude: 49.617890,
        longitude: 6.149870
      },
      {
        id: 18,
        name: "AutoSport Garage",
        address: "44 Route d'Esch, Luxembourg",
        phone: "+352 691 765 432",
        website: "https://autosport.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-15:00",
        rating: 5,
        distance: 2.6,
        services: ["Sports Cars", "Performance Upgrades", "Race Preparation", "Custom Tuning"],
        latitude: 49.596540,
        longitude: 6.127650
      },
      {
        id: 19,
        name: "Family Auto Service",
        address: "87 Rue de Strasbourg, Luxembourg",
        phone: "+352 621 654 321",
        website: "https://familyauto.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-13:00",
        rating: 4,
        distance: 3.2,
        services: ["Family Cars", "Minivan Service", "Child Seat Installation", "Safety Checks"],
        latitude: 49.601230,
        longitude: 6.133450
      },
      {
        id: 20,
        name: "Quick Fix Garage",
        address: "31 Rue du Fort Neipperg, Luxembourg",
        phone: "+352 661 987 123",
        website: "https://quickfix.lu",
        hours: "Mon-Fri: 7:00-20:00, Sat-Sun: 9:00-16:00",
        rating: 3,
        distance: 1.9,
        services: ["Express Repairs", "Mobile Service", "Roadside Assistance", "Quick Diagnostics"],
        latitude: 49.607650,
        longitude: 6.134560
      },
      {
        id: 21,
        name: "German Auto Specialists",
        address: "63 Boulevard Konrad Adenauer, Luxembourg",
        phone: "+352 691 234 567",
        website: "https://germanauto.lu",
        hours: "Mon-Fri: 8:00-18:30, Sat: 9:00-14:00",
        rating: 5,
        distance: 6.8,
        services: ["BMW Specialist", "Mercedes Service", "Audi Repair", "VW Diagnostics"],
        latitude: 49.637890,
        longitude: 6.147650
      },
      {
        id: 22,
        name: "Electric Vehicle Center",
        address: "22 Avenue John F. Kennedy, Luxembourg",
        phone: "+352 671 345 987",
        website: "https://evcenter.lu",
        hours: "Mon-Fri: 8:30-18:00, Sat: 9:30-15:00",
        rating: 5,
        distance: 5.3,
        services: ["EV Charging", "Tesla Service", "Battery Diagnostics", "Electric Conversions"],
        latitude: 49.619870,
        longitude: 6.167890
      },
      {
        id: 23,
        name: "Budget Auto Repair",
        address: "41 Rue de Bouillon, Luxembourg",
        phone: "+352 621 876 123",
        website: "https://budgetauto.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-14:00",
        rating: 3,
        distance: 4.1,
        services: ["Affordable Repairs", "Used Parts", "Basic Service", "Budget Friendly"],
        latitude: 49.593450,
        longitude: 6.129870
      },
      {
        id: 24,
        name: "Truck & Van Service",
        address: "78 Rue de la Déportation, Hollerich",
        phone: "+352 661 432 876",
        website: "https://truckvanservice.lu",
        hours: "Mon-Fri: 7:00-19:00, Sat: 8:00-15:00",
        rating: 4,
        distance: 7.6,
        services: ["Commercial Vehicles", "Van Repair", "Truck Service", "Fleet Maintenance"],
        latitude: 49.601230,
        longitude: 6.117890
      },
      {
        id: 25,
        name: "Exclusive Auto Garage",
        address: "15 Boulevard Grande-Duchesse Charlotte, Luxembourg",
        phone: "+352 691 765 987",
        website: "https://exclusiveauto.lu",
        hours: "Mon-Fri: 9:00-18:00, Sat: By appointment",
        rating: 5,
        distance: 2.4,
        services: ["Exotic Cars", "Premium Detailing", "Concierge Service", "Climate Controlled Storage"],
        latitude: 49.615670,
        longitude: 6.127890
      },
      {
        id: 26,
        name: "AutoGlass & Body Shop",
        address: "53 Route de Diekirch, Walferdange",
        phone: "+352 621 543 876",
        website: "https://autoglassbody.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-13:00",
        rating: 4,
        distance: 9.2,
        services: ["Windshield Replacement", "Body Repair", "Paint Jobs", "Dent Removal"],
        latitude: 49.659870,
        longitude: 6.137650
      }
    ];
  };

  // Filter garages based on search term
  useEffect(() => {
    if (!searchTerm.trim()) {
      setFilteredGarages(garages);
      return;
    }
    
    const term = searchTerm.toLowerCase();
    const filtered = garages.filter(garage => 
      garage.name.toLowerCase().includes(term) ||
      garage.address.toLowerCase().includes(term) ||
      garage.services.some(service => service.toLowerCase().includes(term))
    );
    
    setFilteredGarages(filtered);
  }, [searchTerm, garages]);
  
  const handleBookAppointment = (garage) => {
    setSelectedGarage(garage);
    onOpen();
  };
  
  const handleBackToDiagnosis = () => {
    navigate(-1);
  };

  if (loading) {
    return (
      <Flex justify="center" align="center" minH="calc(100vh - 72px)" direction="column">
        <Spinner size={isMobile ? "lg" : "xl"} color="accent.500" thickness="4px" mb={4} />
        <Text color="text.900" fontSize={isMobile ? "md" : "lg"}>Finding garages near you...</Text>
      </Flex>
    );
  }

  // Define theme color variables
  const cardBg = 'white';
  const borderColor = 'secondary.200';
  const textColor = 'text.900';
  const mutedTextColor = 'text.700';

  return (
    <Container maxW="container.xl" py={containerPadding} px={containerPadding}>
      <VStack spacing={8} align="stretch">
        <Box 
          p={isMobile ? 4 : 6} 
          borderRadius="lg" 
          boxShadow="md"
          bg="white"
          color="text.900"
        >
          <VStack spacing={4} align="stretch">
            <Flex 
              justifyContent="space-between" 
              alignItems="center"
              direction={isMobile ? "column" : "row"}
              gap={isMobile ? 3 : 0}
            >
              <Heading 
                size={headingSize} 
                color={textColor}
                textAlign={isMobile ? "center" : "left"}
              >
                {selectedIssue 
                  ? `Garages for ${selectedIssue.name}` 
                  : 'Find Garages Near You'}
              </Heading>
              
              {selectedIssue && (
                <Button 
                  leftIcon={<Icon as={FaArrowLeft} />} 
                  onClick={handleBackToDiagnosis}
                  colorScheme="brand"
                  variant="outline"
                  size={isMobile ? "sm" : "md"}
                  width={isMobile ? "full" : "auto"}
                >
                  Back to Diagnosis
                </Button>
              )}
            </Flex>
            
            {vehicleInfo && (
              <Flex align="center">
                <Badge colorScheme="accent" fontSize="md" px={2} py={1}>
                  {vehicleInfo.year} {vehicleInfo.brand} {vehicleInfo.model}
                </Badge>
              </Flex>
            )}
            
            <Text 
              fontSize={isMobile ? "md" : "lg"} 
              color={textColor}
              textAlign={isMobile ? "center" : "left"}
              mt={2}
            >
              {selectedIssue 
                ? `Find the best auto repair shops that can fix ${selectedIssue.name}` 
                : 'Find the best auto repair shops in your area'}
            </Text>
          </VStack>
        </Box>

        <InputGroup 
          size={isMobile ? "md" : "lg"} 
          mx="auto" 
          maxW="container.md"
          mt={4}
        >
          <InputLeftElement pointerEvents="none">
            <Icon as={FaSearch} color="accent.500" />
          </InputLeftElement>
          <Input 
            placeholder="Search by garage name, service, or location..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            bg="white"
            borderWidth="2px"
            borderColor="gray.300"
            _focus={{ 
              borderColor: "accent.500", 
              boxShadow: "0 0 0 1px var(--chakra-colors-accent-500)" 
            }}
          />
        </InputGroup>

        {error && (
          <Alert status="warning" borderRadius="md">
            <AlertIcon />
            {error}
          </Alert>
        )}

        {filteredGarages.length === 0 ? (
          <Alert status="info" borderRadius="md">
            <AlertIcon />
            No garages found matching your search criteria.
          </Alert>
        ) : (
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={isMobile ? 4 : 6}>
            {filteredGarages.map((garage) => (
              <GarageCard 
                key={garage.id} 
                garage={garage} 
                onBookAppointment={handleBookAppointment}
              />
            ))}
          </SimpleGrid>
        )}
      </VStack>
      
      {/* Booking Modal */}
      {selectedGarage && (
        <Modal 
          isOpen={isOpen} 
          onClose={onClose} 
          size={isMobile ? "full" : "xl"}
          motionPreset={isMobile ? "slideInBottom" : "scale"}
        >
          <ModalOverlay />
          <ModalContent borderRadius={isMobile ? 0 : "md"}>
            <ModalHeader fontSize={isMobile ? "lg" : "xl"}>Book Appointment at {selectedGarage.name}</ModalHeader>
            <ModalCloseButton />
            <ModalBody pb={6}>
              <BookingModal 
                garage={selectedGarage} 
                issue={selectedIssue}
                vehicle={vehicleInfo}
                onClose={onClose}
              />
            </ModalBody>
          </ModalContent>
        </Modal>
      )}
    </Container>
  );
};

export default GarageList;
