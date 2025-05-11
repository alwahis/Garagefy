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
  useBreakpointValue,
  ButtonGroup,
  Tooltip,
  Switch,
  FormControl,
  FormLabel
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
  FaArrowLeft,
  FaList,
  FaMap,
  FaEuroSign
} from 'react-icons/fa';
import axios from 'axios';
import config from '../config';
import { useLocation, useNavigate } from 'react-router-dom';
import BookingModal from '../components/BookingModal';
import GarageMap from '../components/GarageMap';

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
            >
              <Icon as={FaMapMarkerAlt} color="white" />
            </Box>
            <Box>
              <Text fontWeight="medium" color={textColor}>
                Address
              </Text>
              <Text color={mutedTextColor} fontSize="sm">
                {garage.address}
              </Text>
            </Box>
          </Flex>
          
          <Flex align="flex-start">
            <Box 
              bg="accent.500" 
              p={2} 
              borderRadius="full" 
              display="inline-flex"
              mr={2}
            >
              <Icon as={FaPhoneAlt} color="white" />
            </Box>
            <Box>
              <Text fontWeight="medium" color={textColor}>
                Contact
              </Text>
              <Text color={mutedTextColor} fontSize="sm">
                {garage.phone}
              </Text>
            </Box>
          </Flex>
          
          <Flex align="flex-start">
            <Box 
              bg="accent.500" 
              p={2} 
              borderRadius="full" 
              display="inline-flex"
              mr={2}
            >
              <Icon as={FaClock} color="white" />
            </Box>
            <Box>
              <Text fontWeight="medium" color={textColor}>
                Hours
              </Text>
              <Text color={mutedTextColor} fontSize="sm" noOfLines={2}>
                {garage.hours}
              </Text>
            </Box>
          </Flex>
          
          <Flex align="flex-start">
            <Box 
              bg="accent.500" 
              p={2} 
              borderRadius="full" 
              display="inline-flex"
              mr={2}
            >
              <Icon as={FaStar} color="white" />
            </Box>
            <Box>
              <Text fontWeight="medium" color={textColor}>
                Rating
              </Text>
              <Flex>
                {Array(5).fill('').map((_, i) => (
                  <Icon
                    key={i}
                    as={FaStar}
                    color={i < garage.rating ? 'yellow.400' : 'gray.300'}
                    mr={1}
                  />
                ))}
              </Flex>
            </Box>
          </Flex>
          

          
          <Divider />
          
          <Box>
            <Text fontWeight="medium" color={textColor} mb={2}>
              Services
            </Text>
            <Wrap spacing={2}>
              {garage.services?.map((service, index) => (
                <WrapItem key={index}>
                  <Tag size="sm" colorScheme="brand" variant="subtle">
                    {service}
                  </Tag>
                </WrapItem>
              ))}
            </Wrap>
          </Box>
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
  const [viewMode, setViewMode] = useState('map'); // Changed default to 'map' instead of 'list'
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
        longitude: 6.132263,
        repair_prices: [
          { service: "Oil Change", average_price: 85 },
          { service: "Brake Pad Replacement", average_price: 220 },
          { service: "Timing Belt Replacement", average_price: 450 },
          { service: "Air Filter Replacement", average_price: 45 },
          { service: "Battery Replacement", average_price: 150 }
        ]
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
        longitude: 6.125790,
        repair_prices: [
          { service: "Transmission Fluid Change", average_price: 180 },
          { service: "AC Recharge", average_price: 120 },
          { service: "Tire Replacement (4 tires)", average_price: 520 },
          { service: "Alternator Replacement", average_price: 380 },
          { service: "Starter Motor Replacement", average_price: 350 }
        ]
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
        longitude: 6.122560,
        repair_prices: [
          { service: "Full Service (Luxury)", average_price: 450 },
          { service: "Performance Tuning", average_price: 750 },
          { service: "Body Work (per panel)", average_price: 580 },
          { service: "Full Detailing", average_price: 320 },
          { service: "Wheel Alignment", average_price: 180 }
        ]
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
        longitude: 6.129870,
        repair_prices: [
          { service: "General Inspection", average_price: 95 },
          { service: "Battery Replacement", average_price: 140 },
          { service: "Wheel Alignment", average_price: 120 },
          { service: "Brake Fluid Flush", average_price: 85 },
          { service: "Coolant Flush", average_price: 90 }
        ]
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
        longitude: 6.127650,
        repair_prices: [
          { service: "EV Battery Check", average_price: 120 },
          { service: "Hybrid System Diagnosis", average_price: 180 },
          { service: "Computer Diagnostics", average_price: 95 },
          { service: "Suspension Repair", average_price: 420 },
          { service: "Software Update", average_price: 150 }
        ]
      },
      {
        id: 6,
        name: "City Garage Luxembourg",
        address: "34 Avenue de la Gare, Luxembourg",
        phone: "+352 654 321 987",
        website: "https://citygarage.lu",
        hours: "Mon-Fri: 8:00-17:30, Sat: 9:00-13:00",
        rating: 4,
        distance: 3.5,
        services: ["Engine Diagnostics", "Transmission Repair", "Brake Service", "Suspension Work"],
        latitude: 49.599870,
        longitude: 6.133450,
        repair_prices: [
          { service: "Engine Diagnostics", average_price: 120 },
          { service: "Transmission Repair", average_price: 650 },
          { service: "Brake Service", average_price: 180 },
          { service: "Suspension Work", average_price: 350 }
        ]
      },
      {
        id: 7,
        name: "Atelier Muller",
        address: "23 Rue de Wiltz, Ettelbruck",
        phone: "+352 812 345 678",
        website: "https://ateliermuller.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-13:00",
        rating: 4,
        distance: 25.3,
        services: ["Classic Car Restoration", "Engine Rebuilding", "Custom Fabrication", "Vintage Parts Sourcing"],
        latitude: 49.847382,
        longitude: 6.106292,
        repair_prices: [
          { service: "Classic Car Service", average_price: 280 },
          { service: "Engine Rebuild (starting)", average_price: 2500 },
          { service: "Custom Fabrication (hourly)", average_price: 85 }
        ]
      },
      {
        id: 8,
        name: "Garage Schmit",
        address: "45 Route de Longwy, Rodange",
        phone: "+352 621 987 654",
        website: "https://garageschmit.lu",
        hours: "Mon-Fri: 7:30-18:30, Sat: 8:00-12:00",
        rating: 5,
        distance: 22.7,
        services: ["Diesel Specialist", "Truck Repairs", "Commercial Vehicle Service", "Fleet Maintenance"],
        latitude: 49.545872,
        longitude: 5.842095,
        repair_prices: [
          { service: "Diesel Engine Service", average_price: 220 },
          { service: "Commercial Vehicle Inspection", average_price: 150 },
          { service: "Fleet Maintenance Contract (monthly)", average_price: 350 }
        ]
      },
      {
        id: 9,
        name: "Atelier Hoffmann",
        address: "12 Rue de la Libération, Diekirch",
        phone: "+352 691 234 567",
        website: "https://atelierhoffmann.lu",
        hours: "Mon-Fri: 8:30-17:30, Sat: 9:00-12:00",
        rating: 4,
        distance: 27.9,
        services: ["Motorcycle Repairs", "Scooter Service", "ATV Maintenance", "Performance Upgrades"],
        latitude: 49.868332,
        longitude: 6.158889,
        repair_prices: [
          { service: "Motorcycle Service", average_price: 120 },
          { service: "Scooter Tune-up", average_price: 80 },
          { service: "ATV Maintenance", average_price: 150 }
        ]
      },
      {
        id: 10,
        name: "Garage Weber & Fils",
        address: "78 Avenue de la Faïencerie, Luxembourg",
        phone: "+352 661 876 543",
        website: "https://weberfils.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 8:30-14:00",
        rating: 5,
        distance: 3.2,
        services: ["Family-Owned Since 1965", "Multi-Brand Specialist", "Classic Car Maintenance", "Pre-Purchase Inspection"],
        latitude: 49.628075,
        longitude: 6.114988,
        repair_prices: [
          { service: "Multi-Point Inspection", average_price: 75 },
          { service: "Pre-Purchase Inspection", average_price: 180 },
          { service: "Classic Car Maintenance", average_price: 250 }
        ]
      },
      {
        id: 11,
        name: "Garage Elsen",
        address: "34 Rue de Mersch, Mamer",
        phone: "+352 671 432 876",
        website: "https://garageelsen.lu",
        hours: "Mon-Fri: 7:00-19:00, Sat: 8:00-16:00",
        rating: 4,
        distance: 9.7,
        services: ["24/7 Roadside Assistance", "Towing Service", "Jump Starts", "Tire Changes"],
        latitude: 49.626389,
        longitude: 6.023611,
        repair_prices: [
          { service: "Roadside Assistance (basic)", average_price: 85 },
          { service: "Towing (up to 20km)", average_price: 120 },
          { service: "Tire Change (per tire)", average_price: 35 }
        ]
      },
      {
        id: 12,
        name: "Atelier Kieffer",
        address: "56 Rue de la Gare, Dudelange",
        phone: "+352 621 765 432",
        website: "https://kieffer-garage.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-13:00",
        rating: 3,
        distance: 15.6,
        services: ["Bodywork Specialist", "Paint Jobs", "Dent Removal", "Collision Repair"],
        latitude: 49.477778,
        longitude: 6.087778,
        repair_prices: [
          { service: "Dent Removal (small)", average_price: 120 },
          { service: "Paint Job (per panel)", average_price: 350 },
          { service: "Collision Repair (starting)", average_price: 450 }
        ]
      },
      {
        id: 13,
        name: "Garage Thill",
        address: "23 Route d'Arlon, Strassen",
        phone: "+352 691 543 876",
        website: "https://garagethill.lu",
        hours: "Mon-Fri: 8:30-18:30, Sat: 8:30-12:30",
        rating: 5,
        distance: 5.8,
        services: ["German Car Specialist", "BMW Service", "Mercedes Maintenance", "Audi & VW Repairs"],
        latitude: 49.619444,
        longitude: 6.073056,
        repair_prices: [
          { service: "German Car Full Service", average_price: 320 },
          { service: "Diagnostic Scan", average_price: 90 },
          { service: "Timing Belt Replacement (German cars)", average_price: 650 }
        ]
      },
      {
        id: 14,
        name: "Garage Clement",
        address: "89 Rue de Belvaux, Esch-sur-Alzette",
        phone: "+352 621 234 987",
        website: "https://garageclement.lu",
        hours: "Mon-Fri: 7:30-18:00, Sat: 8:00-12:00",
        rating: 4,
        distance: 17.3,
        services: ["French Car Specialist", "Peugeot Service", "Renault Maintenance", "Citroën Repairs"],
        latitude: 49.495833,
        longitude: 5.981111,
        repair_prices: [
          { service: "French Car Service", average_price: 210 },
          { service: "Timing Belt (French cars)", average_price: 480 },
          { service: "Clutch Replacement", average_price: 650 }
        ]
      },
      {
        id: 15,
        name: "Garage Schintgen",
        address: "12 Rue de Remich, Grevenmacher",
        phone: "+352 661 876 234",
        website: "https://schintgen-auto.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 8:00-13:00",
        rating: 5,
        distance: 24.1,
        services: ["Tire Specialist", "Wheel Alignment", "Balancing", "Seasonal Tire Storage"],
        latitude: 49.680833,
        longitude: 6.440278,
        repair_prices: [
          { service: "Tire Change (set of 4)", average_price: 60 },
          { service: "Wheel Alignment", average_price: 95 },
          { service: "Seasonal Tire Storage (6 months)", average_price: 80 }
        ]
      },
      {
        id: 16,
        name: "Atelier Reding",
        address: "45 Rue Principale, Mersch",
        phone: "+352 621 432 765",
        website: "https://reding-garage.lu",
        hours: "Mon-Fri: 8:00-17:30, Sat: 8:30-12:00",
        rating: 4,
        distance: 19.5,
        services: ["Agricultural Equipment", "Tractor Repair", "Farm Machinery", "Heavy Equipment Service"],
        latitude: 49.748611,
        longitude: 6.106389,
        repair_prices: [
          { service: "Tractor Service", average_price: 280 },
          { service: "Farm Equipment Repair (hourly)", average_price: 75 },
          { service: "Heavy Machinery Diagnostics", average_price: 150 }
        ]
      },
      {
        id: 17,
        name: "Garage Lorang",
        address: "67 Rue de Differdange, Petange",
        phone: "+352 621 987 123",
        website: "https://garage-lorang.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 8:00-12:00",
        rating: 4,
        distance: 20.8,
        services: ["Italian Car Specialist", "Fiat Service", "Alfa Romeo Repairs", "Ferrari & Maserati Maintenance"],
        latitude: 49.558333,
        longitude: 5.880556,
        repair_prices: [
          { service: "Italian Car Service", average_price: 290 },
          { service: "Sports Car Maintenance", average_price: 450 },
          { service: "Timing Belt (Italian cars)", average_price: 580 }
        ]
      },
      {
        id: 18,
        name: "Atelier Kremer",
        address: "34 Rue de la Moselle, Remich",
        phone: "+352 661 345 987",
        website: "https://kremer-auto.lu",
        hours: "Mon-Fri: 8:30-17:30, Sat: 9:00-13:00",
        rating: 5,
        distance: 22.4,
        services: ["Air Conditioning Specialist", "Climate Control Systems", "Heating Systems", "Refrigerant Service"],
        latitude: 49.545278,
        longitude: 6.366111,
        repair_prices: [
          { service: "AC Recharge & Service", average_price: 120 },
          { service: "Climate Control Diagnosis", average_price: 90 },
          { service: "Heating System Repair", average_price: 250 }
        ]
      },
      {
        id: 19,
        name: "Garage Biver",
        address: "12 Route de Thionville, Hesperange",
        phone: "+352 621 456 789",
        website: "https://biver-garage.lu",
        hours: "Mon-Fri: 7:30-18:30, Sat: 8:00-14:00",
        rating: 4,
        distance: 6.3,
        services: ["Electrical Systems Specialist", "Battery Service", "Alternator Repair", "Starter Motor Replacement"],
        latitude: 49.578889,
        longitude: 6.156667,
        repair_prices: [
          { service: "Electrical Diagnostics", average_price: 85 },
          { service: "Battery Replacement", average_price: 150 },
          { service: "Alternator Replacement", average_price: 320 }
        ]
      },
      {
        id: 20,
        name: "Garage Felten",
        address: "56 Rue de Clervaux, Wiltz",
        phone: "+352 691 876 345",
        website: "https://felten-garage.lu",
        hours: "Mon-Fri: 8:00-17:00, Sat: 8:30-12:30",
        rating: 4,
        distance: 40.2,
        services: ["4x4 Specialist", "Off-Road Modifications", "Suspension Lifts", "Winch Installation"],
        latitude: 49.965556,
        longitude: 5.933333,
        repair_prices: [
          { service: "4x4 Service", average_price: 250 },
          { service: "Suspension Lift Kit", average_price: 1200 },
          { service: "Winch Installation", average_price: 650 }
        ]
      },
      {
        id: 21,
        name: "Garage Theis",
        address: "23 Rue de Mondorf, Ellange",
        phone: "+352 621 234 567",
        website: "https://theis-auto.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 9:00-12:00",
        rating: 5,
        distance: 18.7,
        services: ["Hybrid Vehicle Specialist", "Toyota Hybrid Service", "Battery System Diagnostics", "EV Charging Solutions"],
        latitude: 49.517778,
        longitude: 6.283333,
        repair_prices: [
          { service: "Hybrid System Check", average_price: 120 },
          { service: "Battery Pack Diagnostics", average_price: 180 },
          { service: "EV Charger Installation", average_price: 750 }
        ]
      },
      {
        id: 22,
        name: "Atelier Goedert",
        address: "78 Rue Principale, Junglinster",
        phone: "+352 661 432 198",
        website: "https://goedert-garage.lu",
        hours: "Mon-Fri: 8:30-18:00, Sat: 8:30-13:00",
        rating: 4,
        distance: 17.5,
        services: ["Brake Specialist", "ABS Systems", "Hydraulic Systems", "Performance Brakes"],
        latitude: 49.718056,
        longitude: 6.223889,
        repair_prices: [
          { service: "Complete Brake Service", average_price: 240 },
          { service: "ABS Module Repair", average_price: 350 },
          { service: "Performance Brake Upgrade", average_price: 850 }
        ]
      },
      {
        id: 23,
        name: "Garage Mayer",
        address: "45 Rue de la Gare, Bettembourg",
        phone: "+352 621 765 098",
        website: "https://mayer-auto.lu",
        hours: "Mon-Fri: 7:30-18:30, Sat: 8:00-13:00",
        rating: 3,
        distance: 12.9,
        services: ["Exhaust Specialist", "Catalytic Converter Replacement", "Custom Exhaust Systems", "Emissions Testing"],
        latitude: 49.518611,
        longitude: 6.103056,
        repair_prices: [
          { service: "Exhaust Repair", average_price: 180 },
          { service: "Catalytic Converter Replacement", average_price: 650 },
          { service: "Custom Exhaust Fabrication", average_price: 850 }
        ]
      },
      {
        id: 24,
        name: "Garage Braun",
        address: "12 Route d'Echternach, Consdorf",
        phone: "+352 691 543 210",
        website: "https://braun-garage.lu",
        hours: "Mon-Fri: 8:00-17:30, Sat: 9:00-12:00",
        rating: 5,
        distance: 25.6,
        services: ["Suspension Specialist", "Shock Absorber Replacement", "Lowering Springs", "Performance Suspension"],
        latitude: 49.778889,
        longitude: 6.338889,
        repair_prices: [
          { service: "Shock Absorber Replacement (pair)", average_price: 280 },
          { service: "Lowering Spring Installation", average_price: 350 },
          { service: "Complete Suspension Overhaul", average_price: 950 }
        ]
      },
      {
        id: 25,
        name: "Atelier Faber",
        address: "67 Rue de Bastogne, Redange",
        phone: "+352 621 876 543",
        website: "https://faber-garage.lu",
        hours: "Mon-Fri: 8:00-18:00, Sat: 8:00-12:00",
        rating: 4,
        distance: 27.3,
        services: ["Transmission Specialist", "Manual Gearbox Repair", "Automatic Transmission Service", "Clutch Replacement"],
        latitude: 49.765556,
        longitude: 5.889444,
        repair_prices: [
          { service: "Transmission Fluid Change", average_price: 150 },
          { service: "Clutch Replacement", average_price: 750 },
          { service: "Gearbox Rebuild", average_price: 1800 }
        ]
      },
      {
        id: 26,
        name: "Garage Weis",
        address: "34 Rue Principale, Berdorf",
        phone: "+352 661 234 876",
        website: "https://weis-auto.lu",
        hours: "Mon-Fri: 8:30-17:30, Sat: 9:00-13:00",
        rating: 5,
        distance: 29.8,
        services: ["Engine Specialist", "Turbocharger Repair", "Engine Rebuilding", "Performance Tuning"],
        latitude: 49.818611,
        longitude: 6.353056,
        repair_prices: [
          { service: "Engine Diagnostics", average_price: 120 },
          { service: "Turbocharger Replacement", average_price: 950 },
          { service: "Engine Rebuild", average_price: 3500 }
        ]
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
              
              {/* View toggle buttons */}
              <ButtonGroup size="md" isAttached variant="outline">
                <Button
                  leftIcon={<Icon as={FaList} />}
                  colorScheme={viewMode === 'list' ? 'brand' : 'gray'}
                  onClick={() => setViewMode('list')}
                >
                  List
                </Button>
                <Button
                  leftIcon={<Icon as={FaMap} />}
                  colorScheme={viewMode === 'map' ? 'brand' : 'gray'}
                  onClick={() => setViewMode('map')}
                >
                  Map
                </Button>
              </ButtonGroup>
              
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

        {error ? (
          <Alert status="error" borderRadius="md">
            <AlertIcon />
            {error}
          </Alert>
        ) : filteredGarages.length === 0 ? (
          <Alert status="info" borderRadius="md">
            <AlertIcon />
            No garages found matching your search criteria.
          </Alert>
        ) : viewMode === 'list' ? (
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6} mt={6}>
            {filteredGarages.map((garage) => (
              <GarageCard 
                key={garage.id} 
                garage={garage} 
                onBookAppointment={handleBookAppointment} 
              />
            ))}
          </SimpleGrid>
        ) : (
          <Box mt={6}>
            <GarageMap 
              garages={filteredGarages} 
              onSelectGarage={handleBookAppointment} 
            />
            <Text fontSize="sm" color="gray.500" mt={2} textAlign="center">
              Marker colors indicate repair price ranges: 
              <Badge colorScheme="green" mx={1}>Affordable</Badge>
              <Badge colorScheme="yellow" mx={1}>Moderate</Badge>
              <Badge colorScheme="red" mx={1}>Expensive</Badge>
            </Text>
          </Box>
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
                vehicleInfo={vehicleInfo} 
                issue={selectedIssue} 
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
