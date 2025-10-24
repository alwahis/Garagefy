import React from 'react';
import { 
  Box, 
  Container, 
  Heading, 
  VStack, 
  Text, 
  Button,
  Icon,
  Badge,
  Image,
  SimpleGrid,
  HStack,
  Flex,
  Avatar
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { FaCamera, FaCheckCircle, FaArrowRight, FaWrench, FaCar } from 'react-icons/fa';
import { MdDirectionsCar, MdBuild, MdLocalCarWash } from 'react-icons/md';
import { BsFillCarFrontFill } from 'react-icons/bs';

const Home = () => {
  const navigate = useNavigate();

  return (
    <Box 
      bg="linear-gradient(180deg, #1a1a1a 0%, #2d2d2d 100%)"
      minH="100vh"
      position="relative"
      overflow="hidden"
    >
      {/* App-like Header with gradient */}
      <Box
        bg="linear-gradient(135deg, #FF6B00 0%, #FF8C00 100%)"
        pt={8}
        pb={20}
        position="relative"
        boxShadow="0 4px 20px rgba(255,107,0,0.3)"
      >
        {/* Garage/Workshop Pattern Overlay */}
        <Box
          position="absolute"
          top="0"
          left="0"
          right="0"
          bottom="0"
          opacity="0.1"
          backgroundImage="repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,.1) 10px, rgba(255,255,255,.1) 20px)"
        />
        
        <Container maxW="container.md" position="relative" zIndex={1}>
          <VStack spacing={4} align="center">
            {/* Logo with garage icon */}
            <HStack spacing={3}>
              <Icon as={MdBuild} boxSize={10} color="white" />
              <Heading 
                fontSize="4xl"
                fontWeight="black"
                color="white"
                letterSpacing="tight"
              >
                Garagefy
              </Heading>
            </HStack>
            
            <Badge
              fontSize="sm"
              px={4}
              py={1}
              borderRadius="full"
              bg="rgba(255,255,255,0.2)"
              color="white"
              textTransform="uppercase"
              fontWeight="bold"
              backdropFilter="blur(10px)"
            >
              🔧 Body Shop Network
            </Badge>

            <Text 
              fontSize="2xl" 
              color="white" 
              fontWeight="bold"
              textAlign="center"
              textShadow="0 2px 10px rgba(0,0,0,0.3)"
            >
              Car Body Damage?
            </Text>
            
            <Text 
              fontSize="lg" 
              color="whiteAlpha.900" 
              textAlign="center"
            >
              Connect with Luxembourg's best body shops instantly
            </Text>
          </VStack>
        </Container>
      </Box>

      {/* Main Content Card - App-like floating card */}
      <Container maxW="container.md" mt={-16} position="relative" zIndex={2} px={4}>
        <VStack spacing={6}>
          
          {/* Main Action Card */}
          <Box
            w="100%"
            bg="white"
            borderRadius="3xl"
            p={8}
            boxShadow="0 20px 60px rgba(0,0,0,0.3)"
            border="1px solid"
            borderColor="gray.100"
          >
            <VStack spacing={6}>
              {/* Car damage types with icons */}
              <SimpleGrid columns={3} spacing={4} w="100%">
                <VStack spacing={2}>
                  <Box
                    bg="orange.50"
                    borderRadius="2xl"
                    p={4}
                    border="2px solid"
                    borderColor="orange.200"
                  >
                    <Icon as={BsFillCarFrontFill} boxSize={8} color="orange.500" />
                  </Box>
                  <Text fontSize="sm" fontWeight="bold" color="gray.700" textAlign="center">
                    Dents
                  </Text>
                </VStack>
                
                <VStack spacing={2}>
                  <Box
                    bg="orange.50"
                    borderRadius="2xl"
                    p={4}
                    border="2px solid"
                    borderColor="orange.200"
                  >
                    <Icon as={MdLocalCarWash} boxSize={8} color="orange.500" />
                  </Box>
                  <Text fontSize="sm" fontWeight="bold" color="gray.700" textAlign="center">
                    Scratches
                  </Text>
                </VStack>
                
                <VStack spacing={2}>
                  <Box
                    bg="orange.50"
                    borderRadius="2xl"
                    p={4}
                    border="2px solid"
                    borderColor="orange.200"
                  >
                    <Icon as={FaWrench} boxSize={8} color="orange.500" />
                  </Box>
                  <Text fontSize="sm" fontWeight="bold" color="gray.700" textAlign="center">
                    Collision
                  </Text>
                </VStack>
              </SimpleGrid>

              {/* Value proposition */}
              <Box
                w="100%"
                bg="gradient-to-r from-orange-50 to-yellow-50"
                borderRadius="2xl"
                p={6}
                border="2px solid"
                borderColor="orange.200"
              >
                <VStack spacing={3}>
                  <Text fontSize="3xl" fontWeight="black" color="orange.600">
                    Save up to 70%
                  </Text>
                  <Text fontSize="md" color="gray.700" textAlign="center">
                    Compare quotes from all body shops in Luxembourg
                  </Text>
                </VStack>
              </Box>

              {/* MEGA CTA Button - App-style */}
              <Button
                size="lg"
                w="100%"
                h="70px"
                fontSize="xl"
                fontWeight="black"
                bg="linear-gradient(135deg, #FF6B00 0%, #FF8C00 100%)"
                color="white"
                borderRadius="2xl"
                boxShadow="0 10px 30px rgba(255,107,0,0.4)"
                _hover={{
                  transform: "translateY(-2px)",
                  boxShadow: "0 15px 40px rgba(255,107,0,0.5)",
                }}
                _active={{
                  transform: "translateY(0px)"
                }}
                transition="all 0.2s"
                onClick={() => navigate('/fix-it')}
                rightIcon={<Icon as={FaArrowRight} boxSize={6} />}
                leftIcon={<Icon as={FaCamera} boxSize={6} />}
              >
                GET QUOTES NOW
              </Button>

              <HStack spacing={3} justify="center">
                <HStack spacing={1}>
                  <Icon as={FaCheckCircle} color="green.500" boxSize={4} />
                  <Text fontSize="sm" color="gray.600" fontWeight="semibold">Free</Text>
                </HStack>
                <Text color="gray.400">•</Text>
                <HStack spacing={1}>
                  <Icon as={FaCheckCircle} color="green.500" boxSize={4} />
                  <Text fontSize="sm" color="gray.600" fontWeight="semibold">2 Days</Text>
                </HStack>
                <Text color="gray.400">•</Text>
                <HStack spacing={1}>
                  <Icon as={FaCheckCircle} color="green.500" boxSize={4} />
                  <Text fontSize="sm" color="gray.600" fontWeight="semibold">No Obligation</Text>
                </HStack>
              </HStack>
            </VStack>
          </Box>

          {/* How it works - App-style steps */}
          <Box
            w="100%"
            bg="white"
            borderRadius="3xl"
            p={8}
            boxShadow="0 10px 30px rgba(0,0,0,0.1)"
          >
            <Heading
              fontSize="2xl"
              color="gray.800"
              textAlign="center"
              mb={6}
              fontWeight="black"
            >
              How It Works
            </Heading>

            <VStack spacing={6} align="stretch">
              {/* Step 1 */}
              <HStack spacing={4} align="start">
                <Box
                  bg="orange.500"
                  borderRadius="full"
                  w="50px"
                  h="50px"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                  flexShrink={0}
                  boxShadow="0 4px 15px rgba(255,107,0,0.3)"
                >
                  <Text fontSize="xl" fontWeight="black" color="white">1</Text>
                </Box>
                <VStack align="start" spacing={1} flex={1}>
                  <HStack spacing={2}>
                    <Icon as={FaCamera} color="orange.500" boxSize={5} />
                    <Text fontSize="lg" fontWeight="bold" color="gray.800">
                      Take Photos
                    </Text>
                  </HStack>
                  <Text fontSize="md" color="gray.600">
                    Snap pictures of your car damage with your phone
                  </Text>
                </VStack>
              </HStack>

              {/* Connector line */}
              <Box w="2px" h="30px" bg="gray.200" ml="24px" />

              {/* Step 2 */}
              <HStack spacing={4} align="start">
                <Box
                  bg="orange.500"
                  borderRadius="full"
                  w="50px"
                  h="50px"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                  flexShrink={0}
                  boxShadow="0 4px 15px rgba(255,107,0,0.3)"
                >
                  <Text fontSize="xl" fontWeight="black" color="white">2</Text>
                </Box>
                <VStack align="start" spacing={1} flex={1}>
                  <HStack spacing={2}>
                    <Icon as={MdBuild} color="orange.500" boxSize={5} />
                    <Text fontSize="lg" fontWeight="bold" color="gray.800">
                      We Contact Body Shops
                    </Text>
                  </HStack>
                  <Text fontSize="md" color="gray.600">
                    Your request goes to every certified body shop in Luxembourg
                  </Text>
                </VStack>
              </HStack>

              {/* Connector line */}
              <Box w="2px" h="30px" bg="gray.200" ml="24px" />

              {/* Step 3 */}
              <HStack spacing={4} align="start">
                <Box
                  bg="orange.500"
                  borderRadius="full"
                  w="50px"
                  h="50px"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                  flexShrink={0}
                  boxShadow="0 4px 15px rgba(255,107,0,0.3)"
                >
                  <Text fontSize="xl" fontWeight="black" color="white">3</Text>
                </Box>
                <VStack align="start" spacing={1} flex={1}>
                  <HStack spacing={2}>
                    <Icon as={FaCheckCircle} color="orange.500" boxSize={5} />
                    <Text fontSize="lg" fontWeight="bold" color="gray.800">
                      Compare & Choose
                    </Text>
                  </HStack>
                  <Text fontSize="md" color="gray.600">
                    Get quotes in 2 days, pick the best price and service
                  </Text>
                </VStack>
              </HStack>
            </VStack>
          </Box>

          {/* Garage Network Badge */}
          <Box
            w="100%"
            bg="linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)"
            borderRadius="2xl"
            p={6}
            boxShadow="0 10px 30px rgba(0,0,0,0.3)"
          >
            <VStack spacing={3}>
              <HStack spacing={2}>
                <Icon as={MdBuild} color="orange.500" boxSize={6} />
                <Text fontSize="lg" fontWeight="bold" color="white">
                  Certified Body Shop Network
                </Text>
              </HStack>
              <Text fontSize="sm" color="gray.400" textAlign="center">
                All garages verified • Professional service • Best prices
              </Text>
            </VStack>
          </Box>

          {/* Bottom CTA */}
          <Button
            size="lg"
            w="100%"
            h="65px"
            fontSize="xl"
            fontWeight="black"
            bg="linear-gradient(135deg, #FF6B00 0%, #FF8C00 100%)"
            color="white"
            borderRadius="2xl"
            boxShadow="0 10px 30px rgba(255,107,0,0.4)"
            _hover={{
              transform: "translateY(-2px)",
              boxShadow: "0 15px 40px rgba(255,107,0,0.5)",
            }}
            transition="all 0.2s"
            onClick={() => navigate('/fix-it')}
            rightIcon={<Icon as={FaArrowRight} boxSize={5} />}
            mb={8}
          >
            START NOW - IT'S FREE
          </Button>

        </VStack>
      </Container>
    </Box>
  );
};

export default Home;
