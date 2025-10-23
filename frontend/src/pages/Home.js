import React from 'react';
import { 
  Box, 
  Container, 
  Heading, 
  VStack, 
  Text, 
  Button,
  Stack,
  useBreakpointValue, 
  Icon,
  Badge,
  Image,
  Flex
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { FaClock, FaEuroSign, FaArrowRight, FaMapMarkerAlt, FaCheckCircle } from 'react-icons/fa';
import { MdVerified } from 'react-icons/md';

const Home = () => {
  const navigate = useNavigate();
  const isMobile = useBreakpointValue({ base: true, md: false });
  const headingSize = useBreakpointValue({ base: "3xl", md: "5xl", lg: "6xl" });
  const subheadingSize = useBreakpointValue({ base: "lg", md: "xl", lg: "2xl" });
  const textSize = useBreakpointValue({ base: "md", md: "lg" });
  const badgeSize = useBreakpointValue({ base: "lg", md: "xl" });

  return (
    <Box 
      bg="#FFD700" 
      minH="100vh"
      position="relative"
      overflow="hidden"
    >
      {/* Decorative Elements - Car Body Damage Shadows */}
      <Box
        position="absolute"
        top="-10%"
        right="-5%"
        width="400px"
        height="400px"
        borderRadius="full"
        bg="#0078D4"
        opacity="0.1"
        display={{ base: "none", md: "block" }}
      />
      <Box
        position="absolute"
        bottom="-10%"
        left="-5%"
        width="500px"
        height="500px"
        borderRadius="full"
        bg="#0078D4"
        opacity="0.1"
        display={{ base: "none", md: "block" }}
      />
      
      {/* Car Silhouettes with Dents/Damage Icons */}
      <Box
        position="absolute"
        top="15%"
        left="5%"
        fontSize="8xl"
        opacity="0.05"
        transform="rotate(-15deg)"
        display={{ base: "none", lg: "block" }}
      >
        🚗💥
      </Box>
      <Box
        position="absolute"
        bottom="20%"
        right="8%"
        fontSize="8xl"
        opacity="0.05"
        transform="rotate(15deg)"
        display={{ base: "none", lg: "block" }}
      >
        🔧🚙
      </Box>
      <Box
        position="absolute"
        top="50%"
        right="3%"
        fontSize="6xl"
        opacity="0.04"
        transform="rotate(-10deg)"
        display={{ base: "none", lg: "block" }}
      >
        🛠️
      </Box>

      <Container maxW="container.xl" py={{ base: 8, md: 16 }} position="relative" zIndex={1}>
        <VStack spacing={{ base: 12, md: 20 }} align="center">
          {/* Hero Section */}
          <VStack spacing={6} textAlign="center" w="100%" pt={{ base: 8, md: 12 }}>
            {/* Logo */}
            <Box mb={4}>
              <Image 
                src="/garagefy-logo.svg"
                alt="Garagefy - Body Shop Quote Comparison Platform"
                maxW={{ base: "200px", md: "300px", lg: "350px" }}
                w="100%"
                h="auto"
                mx="auto"
                mb={4}
              />
              <Text fontSize={{ base: "md", md: "lg" }} color="#1A202C" fontWeight="semibold" mt={2}>
                Body Shop Quote Comparison Platform
              </Text>
            </Box>

            {/* Main Headline */}
            <Heading 
              as="h1" 
              fontSize={headingSize}
              fontWeight="black"
              lineHeight="1.1"
              color="#1A202C"
              maxW="1000px"
            >
              Car Body Damage? Find the Best Body Shop.
              <Text as="span" color="#0078D4" display="block">
                Save Up to 70%!
              </Text>
            </Heading>

            {/* Save Badge */}
            <Badge 
              fontSize={badgeSize}
              px={8}
              py={3}
              borderRadius="full"
              bg="#0078D4"
              color="white"
              textTransform="uppercase"
              fontWeight="black"
              boxShadow="0 8px 20px rgba(30,136,229,0.4)"
              transform={isMobile ? "scale(1)" : "scale(1.1)"}
            >
              💰 Save up to 70% on Body Damage Repairs
            </Badge>

            {/* Subheadline */}
            <Text 
              fontSize={subheadingSize} 
              color="#1A202C" 
              maxW="800px" 
              fontWeight="semibold"
              lineHeight="1.4"
            >
              Dents, scratches, collision damage? Compare quotes from certified body shops in Luxembourg
            </Text>
          </VStack>

          {/* Featured: Get Quote from All Garages Section */}
          <Box
            w="100%"
            maxW="1100px"
            bg="linear-gradient(135deg, #0078D4 0%, #1565C0 100%)"
            p={{ base: 8, md: 12 }}
            borderRadius="3xl"
            boxShadow="0 20px 60px rgba(30,136,229,0.5)"
            position="relative"
            overflow="hidden"
            border="4px solid"
            borderColor="white"
          >
            {/* Animated Background Pattern */}
            <Box
              position="absolute"
              top="-50%"
              right="-20%"
              width="500px"
              height="500px"
              borderRadius="full"
              bg="whiteAlpha.100"
              display={{ base: "none", md: "block" }}
            />
            <Box
              position="absolute"
              bottom="-30%"
              left="-10%"
              width="400px"
              height="400px"
              borderRadius="full"
              bg="whiteAlpha.100"
              display={{ base: "none", md: "block" }}
            />
            
            <VStack spacing={6} position="relative" zIndex={1}>
              {/* Eye-catching Badge */}
              <Badge
                fontSize={{ base: "sm", md: "md" }}
                px={6}
                py={2}
                borderRadius="full"
                bg="#FFD700"
                color="#1A202C"
                textTransform="uppercase"
                fontWeight="black"
                boxShadow="0 4px 15px rgba(255,215,0,0.4)"
              >
                ⚡ One-Click Solution
              </Badge>

              {/* Main Heading */}
              <Heading
                fontSize={{ base: "2xl", md: "4xl", lg: "5xl" }}
                color="white"
                textAlign="center"
                fontWeight="black"
                lineHeight="1.2"
              >
                Get Quotes from{' '}
                <Text as="span" color="#FFD700">
                  ALL Garages
                </Text>
                {' '}in Luxembourg
              </Heading>

              {/* Subheading with Location Icon */}
              <Flex
                align="center"
                justify="center"
                gap={3}
                flexWrap="wrap"
              >
                <Icon as={FaMapMarkerAlt} color="#FFD700" boxSize={6} />
                <Text
                  fontSize={{ base: "lg", md: "xl" }}
                  color="whiteAlpha.900"
                  fontWeight="semibold"
                  textAlign="center"
                >
                  Luxembourg City • Esch-sur-Alzette • Differdange • Dudelange & More
                </Text>
              </Flex>

              {/* Feature Pills */}
              <Stack
                direction={{ base: "column", sm: "row" }}
                spacing={4}
                justify="center"
                flexWrap="wrap"
              >
                <Flex
                  align="center"
                  bg="whiteAlpha.200"
                  px={6}
                  py={3}
                  borderRadius="full"
                  gap={2}
                >
                  <Icon as={FaCheckCircle} color="#FFD700" />
                  <Text color="white" fontWeight="semibold" fontSize={{ base: "sm", md: "md" }}>
                    All Certified Body Shops
                  </Text>
                </Flex>
                <Flex
                  align="center"
                  bg="whiteAlpha.200"
                  px={6}
                  py={3}
                  borderRadius="full"
                  gap={2}
                >
                  <Icon as={FaClock} color="#FFD700" />
                  <Text color="white" fontWeight="semibold" fontSize={{ base: "sm", md: "md" }}>
                    2 Business Days Response
                  </Text>
                </Flex>
                <Flex
                  align="center"
                  bg="whiteAlpha.200"
                  px={6}
                  py={3}
                  borderRadius="full"
                  gap={2}
                >
                  <Icon as={FaEuroSign} color="#FFD700" />
                  <Text color="white" fontWeight="semibold" fontSize={{ base: "sm", md: "md" }}>
                    100% Free Service
                  </Text>
                </Flex>
              </Stack>

              {/* Large CTA Button */}
              <Button
                size="lg"
                fontSize={{ base: "xl", md: "2xl" }}
                px={{ base: 12, md: 20 }}
                py={{ base: 8, md: 12 }}
                h="auto"
                bg="#FFD700"
                color="#1A202C"
                _hover={{
                  bg: "#FFC700",
                  transform: "scale(1.08) translateY(-4px)",
                  boxShadow: "0 15px 40px rgba(255,215,0,0.6)"
                }}
                _active={{ bg: "#FFB700", transform: "scale(1.05)" }}
                transition="all 0.3s ease"
                boxShadow="0 10px 30px rgba(255,215,0,0.5)"
                borderRadius="full"
                fontWeight="black"
                onClick={() => navigate('/fix-it')}
                rightIcon={<FaArrowRight />}
                mt={4}
              >
                Get All Quotes in One Click 🚀
              </Button>

              {/* Trust Indicator */}
              <Text
                fontSize={{ base: "sm", md: "md" }}
                color="whiteAlpha.800"
                textAlign="center"
                fontStyle="italic"
              >
                ✨ Join 500+ satisfied customers who saved thousands on body repairs
              </Text>
            </VStack>
          </Box>

          {/* Benefits Grid */}
          <Stack
            direction={{ base: "column", md: "row" }}
            spacing={8}
            w="100%"
            maxW="1200px"
            mt={8}
            position="relative"
          >
            {/* Subtle car repair background */}
            <Box
              position="absolute"
              left="-50px"
              top="50%"
              transform="translateY(-50%)"
              fontSize="9xl"
              opacity="0.03"
              display={{ base: "none", xl: "block" }}
              pointerEvents="none"
            >
              🚗
            </Box>
            {/* Benefit Card 1 */}
            <Box
              flex={1}
              bg="white"
              p={{ base: 6, md: 8 }}
              borderRadius="2xl"
              boxShadow="0 10px 30px rgba(0,0,0,0.1)"
              textAlign="center"
              border="3px solid"
              borderColor="#0078D4"
              _hover={{ 
                transform: "translateY(-8px)",
                boxShadow: "0 15px 40px rgba(30,136,229,0.3)"
              }}
              transition="all 0.3s ease"
            >
              <Icon as={FaEuroSign} boxSize={{ base: 12, md: 16 }} color="#0078D4" mb={4} />
              <Heading size="lg" mb={3} color="#1A202C">
                Huge Savings
              </Heading>
              <Text fontSize={textSize} color="gray.600" lineHeight="1.6">
                Save up to 70% on dents, scratches & collision repairs by comparing quotes from multiple body shops
              </Text>
            </Box>

            {/* Benefit Card 2 */}
            <Box
              flex={1}
              bg="white"
              p={{ base: 6, md: 8 }}
              borderRadius="2xl"
              boxShadow="0 10px 30px rgba(0,0,0,0.1)"
              textAlign="center"
              border="3px solid"
              borderColor="#0078D4"
              _hover={{ 
                transform: "translateY(-8px)",
                boxShadow: "0 15px 40px rgba(30,136,229,0.3)"
              }}
              transition="all 0.3s ease"
            >
              <Icon as={FaClock} boxSize={{ base: 12, md: 16 }} color="#0078D4" mb={4} />
              <Heading size="lg" mb={3} color="#1A202C">
                Fast & Easy
              </Heading>
              <Text fontSize={textSize} color="gray.600" lineHeight="1.6">
                Submit one request and receive multiple quotes within 2 business days. No more calling around!
              </Text>
            </Box>

            {/* Benefit Card 3 */}
            <Box
              flex={1}
              bg="white"
              p={{ base: 6, md: 8 }}
              borderRadius="2xl"
              boxShadow="0 10px 30px rgba(0,0,0,0.1)"
              textAlign="center"
              border="3px solid"
              borderColor="#0078D4"
              _hover={{ 
                transform: "translateY(-8px)",
                boxShadow: "0 15px 40px rgba(30,136,229,0.3)"
              }}
              transition="all 0.3s ease"
            >
              <Icon as={MdVerified} boxSize={{ base: 12, md: 16 }} color="#0078D4" mb={4} />
              <Heading size="lg" mb={3} color="#1A202C">
                Trusted Shops
              </Heading>
              <Text fontSize={textSize} color="gray.600" lineHeight="1.6">
                All body shops are certified and verified professionals in Luxembourg
              </Text>
            </Box>
          </Stack>

          {/* How It Works Section */}
          <Box 
            w="100%" 
            maxW="1000px" 
            bg="white" 
            p={{ base: 8, md: 12 }} 
            borderRadius="3xl"
            boxShadow="0 15px 50px rgba(0,0,0,0.15)"
            mt={8}
            position="relative"
          >
            {/* Subtle car being repaired shadow */}
            <Box
              position="absolute"
              top="50%"
              right="-80px"
              transform="translateY(-50%)"
              fontSize="10xl"
              opacity="0.025"
              display={{ base: "none", xl: "block" }}
              pointerEvents="none"
            >
              🚗🔧
            </Box>
            <Heading 
              size="2xl" 
              textAlign="center" 
              mb={10}
              color="#1A202C"
            >
              How It Works
            </Heading>
            
            <VStack spacing={6} align="stretch">
              {/* Step 1 */}
              <Flex 
                align="center" 
                bg="#FFF9E6" 
                p={6} 
                borderRadius="xl"
                border="2px solid"
                borderColor="#FFD700"
              >
                <Box 
                  bg="#0078D4" 
                  color="white" 
                  borderRadius="full" 
                  w="50px" 
                  h="50px" 
                  display="flex" 
                  alignItems="center" 
                  justifyContent="center" 
                  fontWeight="black" 
                  fontSize="2xl"
                  flexShrink={0}
                  mr={6}
                >
                  1
                </Box>
                <Box flex={1}>
                  <Heading size="md" mb={2} color="#1A202C">
                    Submit Your Request
                  </Heading>
                  <Text fontSize="md" color="gray.700">
                    Tell us about your car's body damage (dents, scratches, collision). Upload photos for accurate quotes.
                  </Text>
                </Box>
              </Flex>

              {/* Step 2 */}
              <Flex 
                align="center" 
                bg="#FFF9E6" 
                p={6} 
                borderRadius="xl"
                border="2px solid"
                borderColor="#FFD700"
              >
                <Box 
                  bg="#0078D4" 
                  color="white" 
                  borderRadius="full" 
                  w="50px" 
                  h="50px" 
                  display="flex" 
                  alignItems="center" 
                  justifyContent="center" 
                  fontWeight="black" 
                  fontSize="2xl"
                  flexShrink={0}
                  mr={6}
                >
                  2
                </Box>
                <Box flex={1}>
                  <Heading size="md" mb={2} color="#1A202C">
                    Receive Multiple Quotes
                  </Heading>
                  <Text fontSize="md" color="gray.700">
                    Certified body shops review your request and send you competitive quotes.
                  </Text>
                </Box>
              </Flex>

              {/* Step 3 */}
              <Flex 
                align="center" 
                bg="#FFF9E6" 
                p={6} 
                borderRadius="xl"
                border="2px solid"
                borderColor="#FFD700"
              >
                <Box 
                  bg="#0078D4" 
                  color="white" 
                  borderRadius="full" 
                  w="50px" 
                  h="50px" 
                  display="flex" 
                  alignItems="center" 
                  justifyContent="center" 
                  fontWeight="black" 
                  fontSize="2xl"
                  flexShrink={0}
                  mr={6}
                >
                  3
                </Box>
                <Box flex={1}>
                  <Heading size="md" mb={2} color="#1A202C">
                    Choose & Save
                  </Heading>
                  <Text fontSize="md" color="gray.700">
                    Compare quotes and choose the best deal. Save up to 70% on your body damage repair!
                  </Text>
                </Box>
              </Flex>
            </VStack>
          </Box>

          {/* Final CTA Section */}
          <Box 
            w="100%"
            maxW="1000px"
            bg="#0078D4"
            p={{ base: 10, md: 16 }}
            borderRadius="3xl"
            textAlign="center"
            boxShadow="0 20px 60px rgba(30,136,229,0.4)"
            mt={8}
          >
            <Heading 
              size="2xl" 
              color="white" 
              mb={6}
            >
              Ready to Save Money on Body Damage Repairs?
            </Heading>
            <Text 
              fontSize="xl" 
              color="whiteAlpha.900" 
              mb={8}
              maxW="700px"
              mx="auto"
            >
              Join hundreds of satisfied customers who saved thousands on their car body repairs (dents, scratches, collision)
            </Text>
            <Button
              size="lg"
              fontSize="xl"
              px={12}
              py={8}
              h="auto"
              bg="#FFD700"
              color="#1A202C"
              _hover={{ 
                bg: "#FFC700", 
                transform: "scale(1.05)"
              }}
              _active={{ bg: "#FFB700" }}
              transition="all 0.3s ease"
              boxShadow="0 8px 25px rgba(0,0,0,0.2)"
              borderRadius="full"
              fontWeight="black"
              onClick={() => navigate('/fix-it')}
              rightIcon={<FaArrowRight />}
            >
              Get Your Free Quotes Now
            </Button>
          </Box>
        </VStack>
      </Container>
    </Box>
  );
};
export default Home;
