import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  Heading, 
  Text, 
  VStack, 
  Button, 
  Input,
  Textarea,
  FormControl,
  FormLabel,
  useColorModeValue,
  useToast,
  InputGroup,
  InputLeftElement,
  Icon,
  Flex,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  SimpleGrid,
  Image,
  Select,
  Checkbox,
  FormErrorMessage
} from '@chakra-ui/react';
import { FaUser, FaEnvelope, FaPhone, FaCar, FaImage, FaTimes } from 'react-icons/fa';
import axios from 'axios';
import config from '../config';
import { useLanguage } from '../i18n/LanguageContext';

const FixIt = () => {
  const { t } = useLanguage();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    carBrand: '',
    vin: '',
    plateNumber: '',
    notes: '',
    images: [],
    consent: false
  });
  
  const [previewImages, setPreviewImages] = useState([]);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [selectedImage, setSelectedImage] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [apiStatus, setApiStatus] = useState('unknown');
  const isSubmittingRef = useRef(false);
  const requestIdRef = useRef('');
  const toast = useToast();
  
  const textColor = useColorModeValue('gray.800', 'white');
  const cardBg = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');
  
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const clearForm = () => {
    setFormData({
      name: '',
      email: '',
      phone: '',
      carBrand: '',
      vin: '',
      plateNumber: '',
      notes: '',
      images: [],
      consent: false
    });
    setPreviewImages([]);
  };
  
  const carBrands = [
    'Audi', 'BMW', 'Mercedes-Benz', 'Volkswagen', 'Opel', 'Ford', 'Peugeot',
    'Renault', 'Citroën', 'Fiat', 'Toyota', 'Honda', 'Nissan', 'Mazda',
    'Hyundai', 'Kia', 'Volvo', 'SEAT', 'Skoda', 'Dacia', 'Tesla', 'Other'
  ];
  
  const validateVIN = (vin) => {
    // VIN must be 17 alphanumeric characters, excluding I, O, Q
    const vinRegex = /^[A-HJ-NPR-Z0-9]{17}$/;
    return vinRegex.test(vin.toUpperCase());
  };
  
  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    
    // Check total image count (max 5)
    if (formData.images.length + files.length > 5) {
      toast({
        title: 'Too many images',
        description: 'You can upload a maximum of 5 images',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }
    
    files.forEach(file => {
      // Check file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        toast({
          title: 'File too large',
          description: `${file.name} is larger than 10MB`,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
        return;
      }
      
      // Check file type (JPEG/PNG/WebP)
      if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
        toast({
          title: 'Invalid file type',
          description: `${file.name} is not a JPEG, PNG, or WebP image`,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
        return;
      }
      
      const reader = new FileReader();
      reader.onload = () => {
        if (reader.readyState === 2) {
          setPreviewImages(prev => [...prev, reader.result]);
          setFormData(prev => ({
            ...prev,
            images: [...prev.images, file]
          }));
        }
      };
      reader.readAsDataURL(file);
    });
  };
  
  const removeImage = (index) => {
    setPreviewImages(prev => prev.filter((_, i) => i !== index));
    setFormData(prev => ({
      ...prev,
      images: prev.images.filter((_, i) => i !== index)
    }));
  };

  const validateForm = () => {
    const errors = [];
    
    if (!formData.name.trim()) {
      errors.push('Full name is required');
    }
    
    if (!formData.email.trim()) {
      errors.push('Email is required');
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.push('Email is invalid');
    }
    
    if (!formData.carBrand) {
      errors.push('Car brand is required');
    }
    
    if (!formData.vin.trim()) {
      errors.push('VIN is required');
    } else if (!validateVIN(formData.vin)) {
      errors.push('VIN must be 17 alphanumeric characters (excluding I, O, Q)');
    }
    
    if (!formData.plateNumber.trim()) {
      errors.push('License plate number is required');
    }
    
    if (formData.images.length === 0) {
      errors.push('At least 1 damage photo is required');
    }
    
    if (!formData.consent) {
      errors.push('You must consent to data processing');
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    console.log('Form submission started');
    
    // Prevent default form submission
    if (e && typeof e.preventDefault === 'function') {
      e.preventDefault();
      e.stopPropagation();
    } else {
      console.warn('Event object missing preventDefault method');
    }
    
    // Prevent double submission
    if (isSubmittingRef.current) {
      console.warn('Prevented duplicate submission');
      return;
    }
    
    // Set submitting state early
    isSubmittingRef.current = true;
    setIsSubmitting(true);
    
    try {
      // Validate form
      console.log('Validating form...');
      const errors = validateForm();
      if (errors.length > 0) {
        console.warn('Form validation errors:', errors);
        
        // Show a single toast with all errors
        toast({
          title: 'Please complete all required fields',
          description: (
            <Box>
              {errors.map((error, idx) => (
                <Text key={idx} mb={1}>• {error}</Text>
              ))}
            </Box>
          ),
          status: 'error',
          duration: 7000,
          isClosable: true,
          position: 'top',
        });
        
        isSubmittingRef.current = false;
        setIsSubmitting(false);
        return;
      }
      
      console.log('Form validation passed');
      
      // Generate a unique request ID for this submission
      requestIdRef.current = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      console.log('Generated request ID:', requestIdRef.current);
      
      // Prepare form data
      const formDataToSend = new FormData();
      formDataToSend.append('name', formData.name);
      formDataToSend.append('email', formData.email);
      formDataToSend.append('phone', formData.phone || '');
      formDataToSend.append('carBrand', formData.carBrand);
      formDataToSend.append('vin', formData.vin.toUpperCase());
      formDataToSend.append('licensePlate', formData.plateNumber);
      formDataToSend.append('notes', formData.notes || '');
      formDataToSend.append('requestId', requestIdRef.current);

      // Add images if any
      formData.images.forEach((image, index) => {
        formDataToSend.append(`images`, image);
      });

      console.log('Sending form data:', {
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        vin: formData.vin,
        plateNumber: formData.plateNumber,
        notes: formData.notes,
        imagesCount: formData.images.length
      });
      
      console.log('About to POST to:', `${config.API_BASE_URL}${config.ENDPOINTS.SERVICE_REQUESTS}`);
      
      // Send the request to our backend API
      const response = await axios({
        method: 'post',
        url: `${config.API_BASE_URL}${config.ENDPOINTS.SERVICE_REQUESTS}`,
        data: formDataToSend,
        timeout: 30000, // 30 second timeout
        headers: {
          'X-Request-ID': requestIdRef.current,
          'Accept': 'application/json'
          // Let the browser set the Content-Type header with the correct boundary
        }
      });
      
      console.log('Server response:', response.data);
      
      // Show success message
      toast({
        title: 'Success!',
        description: 'Your service request has been submitted successfully.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      
      // Clear the form
      clearForm();
    } catch (error) {
      console.error('Error submitting form:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        config: error.config ? {
          url: error.config.url,
          method: error.config.method,
          headers: error.config.headers
        } : null
      });
      
      // Show error toast
      let errorMessage = 'Failed to submit form. Please try again.';
      
      if (error.response) {
        errorMessage = error.response.data?.detail || 
                      error.response.data?.message || 
                      `Server responded with status ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'No response from server. Please check your connection.';
      }
      
      toast({
        title: 'Error',
        description: errorMessage,
        status: 'error',
        duration: 10000,
        isClosable: true,
        position: 'top-right'
      });
    } finally {
      // Reset the submission state
      isSubmittingRef.current = false;
      setIsSubmitting(false);
    }
  };

  // Test log to check if component is rendering
  console.log('FixIt component rendered');

  // Ping API on mount to show connectivity status
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const url = `${config.API_BASE_URL}/health`;
        console.log('Pinging API health:', url);
        const res = await fetch(url, { credentials: 'include' });
        setApiStatus(res.ok ? 'online' : 'error');
      } catch (e) {
        console.warn('API health check failed', e);
        setApiStatus('offline');
      }
    };
    checkHealth();
  }, []);
  
  return (
    <Box bg="#FFD700" minH="100vh" p={4} position="relative" overflow="hidden">
      {/* Background Car Body Shop Imagery - Subtle Shadows */}
      <Box
        position="absolute"
        top="10%"
        left="2%"
        fontSize="8xl"
        opacity="0.04"
        transform="rotate(-20deg)"
        display={{ base: "none", lg: "block" }}
        pointerEvents="none"
      >
        🚗💥
      </Box>
      <Box
        position="absolute"
        top="30%"
        right="5%"
        fontSize="7xl"
        opacity="0.05"
        transform="rotate(15deg)"
        display={{ base: "none", lg: "block" }}
        pointerEvents="none"
      >
        🔧
      </Box>
      <Box
        position="absolute"
        bottom="25%"
        left="3%"
        fontSize="9xl"
        opacity="0.03"
        transform="rotate(10deg)"
        display={{ base: "none", lg: "block" }}
        pointerEvents="none"
      >
        🚙
      </Box>
      <Box
        position="absolute"
        bottom="15%"
        right="8%"
        fontSize="6xl"
        opacity="0.04"
        transform="rotate(-12deg)"
        display={{ base: "none", lg: "block" }}
        pointerEvents="none"
      >
        🛠️
      </Box>
      <Box
        position="absolute"
        top="60%"
        left="50%"
        fontSize="10xl"
        opacity="0.02"
        transform="translateX(-50%) rotate(-5deg)"
        display={{ base: "none", xl: "block" }}
        pointerEvents="none"
      >
        🚗
      </Box>
      
      <Box maxW="900px" mx="auto" position="relative" zIndex={1}>
        <VStack 
          spacing={8} 
          align="stretch"
        >
          {/* Main Form */}
          <Box 
            bg="white" 
            p={{ base: 6, md: 10 }} 
            borderRadius="2xl" 
            boxShadow="0 20px 60px rgba(0,0,0,0.15)"
            border="3px solid"
            borderColor="#0078D4"
            position="relative"
          >
            {/* Subtle wrench/tool shadow behind form */}
            <Box
              position="absolute"
              bottom="-30px"
              left="50%"
              transform="translateX(-50%)"
              fontSize="12xl"
              opacity="0.02"
              display={{ base: "none", md: "block" }}
              pointerEvents="none"
              zIndex={0}
            >
              🔧
            </Box>
          <VStack spacing={6} as="form" onSubmit={handleSubmit} noValidate position="relative" zIndex={1}>
              <FormControl isRequired>
                <FormLabel>{t('fixItName')}</FormLabel>
                <InputGroup>
                  <InputLeftElement pointerEvents="none">
                    <Icon as={FaUser} color="gray.400" />
                  </InputLeftElement>
                  <Input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder={t('fixItNamePlaceholder')}
                    pl={10}
                  />
                </InputGroup>
              </FormControl>

              <FormControl isRequired>
                <FormLabel>{t('fixItEmail')}</FormLabel>
                <InputGroup>
                  <InputLeftElement pointerEvents="none">
                    <Icon as={FaEnvelope} color="gray.400" />
                  </InputLeftElement>
                  <Input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder={t('fixItEmailPlaceholder')}
                    pl={10}
                  />
                </InputGroup>
              </FormControl>

              <FormControl>
                <FormLabel>{t('fixItPhone')}</FormLabel>
                <InputGroup>
                  <InputLeftElement pointerEvents="none">
                    <Icon as={FaPhone} color="gray.400" />
                  </InputLeftElement>
                  <Input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    placeholder={t('fixItPhonePlaceholder')}
                    pl={10}
                  />
                </InputGroup>
              </FormControl>

              <FormControl isRequired>
                <FormLabel>License Plate Number</FormLabel>
                <InputGroup>
                  <InputLeftElement pointerEvents="none">
                    <Icon as={FaCar} color="gray.400" />
                  </InputLeftElement>
                  <Input
                    type="text"
                    name="plateNumber"
                    value={formData.plateNumber}
                    onChange={handleChange}
                    placeholder="e.g., AB123CD"
                    pl={10}
                    maxLength="15"
                  />
                </InputGroup>
              </FormControl>

              <FormControl isRequired>
                <FormLabel>{t('fixItCarBrand')}</FormLabel>
                <Select
                  name="carBrand"
                  value={formData.carBrand}
                  onChange={handleChange}
                  placeholder={t('fixItCarBrandPlaceholder')}
                >
                  {carBrands.map(brand => (
                    <option key={brand} value={brand}>{brand}</option>
                  ))}
                </Select>
              </FormControl>

              <FormControl isRequired isInvalid={formData.vin && !validateVIN(formData.vin)}>
                <FormLabel>{t('fixItVin')}</FormLabel>
                <InputGroup>
                  <InputLeftElement pointerEvents="none">
                    <Icon as={FaCar} color="gray.400" />
                  </InputLeftElement>
                  <Input
                    type="text"
                    name="vin"
                    value={formData.vin}
                    onChange={handleChange}
                    placeholder={t('fixItVinPlaceholder')}
                    pl={10}
                    maxLength={17}
                    textTransform="uppercase"
                  />
                </InputGroup>
                <FormErrorMessage>
                  VIN must be 17 alphanumeric characters (excluding I, O, Q)
                </FormErrorMessage>
              </FormControl>

              <FormControl isRequired>
                <FormLabel>{t('fixItPhotos')}</FormLabel>
                <Text fontSize="sm" color="gray.600" mb={2}>{t('fixItPhotosDesc')}</Text>
                <Input
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  multiple
                  onChange={handleImageUpload}
                  display="none"
                  id="image-upload"
                />
                <Button
                  as="label"
                  htmlFor="image-upload"
                  leftIcon={<FaImage />}
                  variant="outline"
                  cursor="pointer"
                  w="100%"
                  isDisabled={formData.images.length >= 5}
                >
                  {formData.images.length === 0 ? t('fixItPhotos') : `Choose More Images (${formData.images.length}/5)`}
                </Button>
                {previewImages.length > 0 && (
                  <SimpleGrid columns={[2, 3, 4]} spacing={4} mt={4}>
                    {previewImages.map((src, index) => (
                      <Box key={index} position="relative">
                        <Image
                          src={src}
                          alt={`Preview ${index + 1}`}
                          borderRadius="md"
                          boxSize="100px"
                          objectFit="cover"
                          cursor="pointer"
                          onClick={() => {
                            setSelectedImage(src);
                            onOpen();
                          }}
                        />
                        <Icon
                          as={FaTimes}
                          position="absolute"
                          top={1}
                          right={1}
                          color="white"
                          bg="red.500"
                          borderRadius="full"
                          p={1}
                          boxSize={5}
                          cursor="pointer"
                          _hover={{ bg: 'red.600' }}
                          onClick={(e) => {
                            e.stopPropagation();
                            removeImage(index);
                          }}
                        />
                      </Box>
                    ))}
                  </SimpleGrid>
                )}
              </FormControl>

              <FormControl>
                <FormLabel>{t('fixItNotes')}</FormLabel>
                <Textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleChange}
                  placeholder={t('fixItNotesPlaceholder')}
                  rows={4}
                />
              </FormControl>

              <FormControl isRequired>
                <Box 
                  p={6} 
                  bg="yellow.100" 
                  borderRadius="lg" 
                  border="3px solid" 
                  borderColor="#0078D4"
                  boxShadow="0 4px 12px rgba(30,136,229,0.2)"
                >
                  <Flex align="flex-start" gap={3}>
                    <Box flexShrink={0} mt={1}>
                      <Checkbox
                        name="consent"
                        isChecked={formData.consent}
                        onChange={(e) => setFormData(prev => ({ ...prev, consent: e.target.checked }))}
                        size="lg"
                        colorScheme="blue"
                        borderColor="#0078D4"
                        iconColor="white"
                      />
                    </Box>
                    <Box flex={1}>
                      <Text fontWeight="black" color="#1A202C" fontSize="lg">
                        <Text as="span" color="red.500" fontSize="xl" mr={1}>*</Text>
                        {t('fixItConsentRequired')}: {t('fixItConsent')}
                      </Text>
                    </Box>
                  </Flex>
                </Box>
              </FormControl>

              <Button 
                type="submit" 
                bg="#0078D4"
                color="white"
                size="lg" 
                width="full"
                mt={6}
                py={8}
                fontSize={{ base: "xl", md: "2xl" }}
                fontWeight="black"
                borderRadius="full"
                isLoading={isSubmitting}
                loadingText={t('fixItSubmitting')}
                _hover={{ 
                  bg: "#1565C0",
                  transform: "translateY(-2px)",
                  boxShadow: "0 12px 30px rgba(30,136,229,0.5)"
                }}
                _active={{ bg: "#0D47A1" }}
                transition="all 0.3s ease"
                boxShadow="0 8px 25px rgba(30,136,229,0.4)"
              >
                {t('fixItSubmit')} →
              </Button>
              
              {/* Trust Badge */}
              <Box textAlign="center" mt={6}>
                <Text fontSize="sm" color="gray.600">
                  🔒 Your information is secure and will only be shared with certified body shops
                </Text>
              </Box>
          </VStack>
          </Box>

          {/* Image Preview Modal */}
          <Modal isOpen={isOpen} onClose={onClose} size="xl">
            <ModalOverlay />
            <ModalContent>
              <ModalHeader>{t('fixItPhotos')}</ModalHeader>
              <ModalCloseButton />
              <ModalBody p={4} display="flex" justifyContent="center">
                <Image 
                  src={selectedImage} 
                  alt="Full size preview" 
                  maxH="70vh"
                  objectFit="contain"
                />
              </ModalBody>
            </ModalContent>
          </Modal>

          {/* Bottom CTA Section */}
          <Box 
            bg="#0078D4" 
            p={{ base: 8, md: 12 }} 
            borderRadius="2xl"
            textAlign="center"
            boxShadow="0 20px 60px rgba(30,136,229,0.4)"
          >
            <Heading size="xl" color="white" mb={4}>
              Why Choose Garagefy for Body Repairs?
            </Heading>
            <Text fontSize="lg" color="whiteAlpha.900" mb={6} maxW="700px" mx="auto">
              We connect you with multiple certified body shops in Luxembourg for dents, scratches, and collision repairs - ensuring you get the best price for quality work. No more overpaying!
            </Text>
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
              <VStack>
                <Text fontSize="3xl">🎯</Text>
                <Text fontWeight="bold" color="white">Compare Prices</Text>
                <Text fontSize="sm" color="whiteAlpha.800">Get multiple quotes to compare</Text>
              </VStack>
              <VStack>
                <Text fontSize="3xl">⭐</Text>
                <Text fontWeight="bold" color="white">Quality Guaranteed</Text>
                <Text fontSize="sm" color="whiteAlpha.800">All shops are certified</Text>
              </VStack>
              <VStack>
                <Text fontSize="3xl">💵</Text>
                <Text fontWeight="bold" color="white">Save Money</Text>
                <Text fontSize="sm" color="whiteAlpha.800">Up to 70% savings</Text>
              </VStack>
            </SimpleGrid>
          </Box>
        </VStack>
      </Box>
    </Box>
  );
};

export default FixIt;
