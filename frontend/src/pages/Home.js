import React from 'react';
import { 
  Box, 
  Container, 
  Heading, 
  VStack, 
  Text, 
  SimpleGrid, 
  useBreakpointValue, 
  Icon
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import { FaTools, FaCar, FaCarCrash } from 'react-icons/fa';

const BigButton = ({ icon, title, description, onClick, bgColor, hoverBgColor }) => {
  const buttonSize = useBreakpointValue({ base: "100%", md: "400px" });
  const iconSize = useBreakpointValue({ base: 12, md: 16 });
  const headingSize = useBreakpointValue({ base: "xl", md: "2xl" });
  const descSize = useBreakpointValue({ base: "sm", md: "md" });
  
  return (
    <Box
      as="button"
      width={buttonSize}
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      py={8}
      px={6}
      borderRadius="xl"
      bg={bgColor}
      color="black" // Changed to black
      _hover={{ bg: hoverBgColor, transform: 'translateY(-5px)', boxShadow: '0 10px 20px rgba(0,0,0,0.3)' }}
      _active={{ bg: hoverBgColor }}
      transition="all 0.3s ease"
      boxShadow="0 5px 15px rgba(0,0,0,0.3)"
      onClick={onClick}
      border="1px solid rgba(255,255,255,0.1)"
      backgroundImage="linear-gradient(180deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%)"
      role="button"
      tabIndex={0}
      aria-label={title}
    >
      <Icon as={icon} boxSize={iconSize} mb={4} color="black" /> {/* Changed to black */}
      <Heading size={headingSize} mb={4} letterSpacing="tight" textAlign="center" color="black">{title}</Heading> {/* Changed to black */}
      <Text 
        textAlign="center" 
        fontSize={descSize} 
        opacity="0.9" 
        px={4} 
        lineHeight="1.6"
        maxW="100%"
        color="black" // Changed to black
      >
        {description}
      </Text>
    </Box>
  );
};

const Home = () => {
  const navigate = useNavigate();
  const containerPadding = useBreakpointValue({ base: 4, md: 8 });
  const spacing = useBreakpointValue({ base: 8, md: 16 });
  const headingSize = useBreakpointValue({ base: "xl", md: "2xl" });
  const textSize = useBreakpointValue({ base: "md", md: "lg" });

  return (
    <Box 
      bgGradient="linear(to-b, #1A365D, #2A4365, #2C5282)" 
      minH="calc(100vh - 72px)"
    >
      <Container maxW="container.xl" py={{ base: 10, md: 20 }} px={containerPadding}>
        <VStack spacing={spacing} align="center">
          <VStack spacing={4} textAlign="center" mb={{ base: 8, md: 12 }}>
            <Heading 
              as="h1" 
              size={headingSize}
              fontWeight="bold"
              lineHeight="shorter"
              color="white"
              letterSpacing="wide"
              textShadow="0 2px 4px rgba(0,0,0,0.3)"
            >
              GARAGEFY
            </Heading>
            <Text fontSize={textSize} color="whiteAlpha.900" maxW="800px" fontWeight="medium">
              Your trusted car assistant
            </Text>
          </VStack>

          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={spacing} width="100%" justifyItems="center">
            <BigButton
              icon={FaCar}
              title="Car Diagnosis"
              description="Get instant diagnosis for your car issues"
              bgColor="#2C5282" /* Darker blue for better contrast */
              hoverBgColor="#1A365D"
              onClick={() => navigate('/diagnose-car')}
            />
            <BigButton
              icon={FaCarCrash}
              title="Fix It"
              description="Find professional help for car body repairs and dents"
              bgColor="#9F7AEA" /* Purple color for Fix It button */
              hoverBgColor="#805AD5"
              onClick={() => navigate('/fix-it')}
            />
            <BigButton
              icon={FaTools}
              title="Used Car Check"
              description="Verify a used car's history and condition before you buy"
              bgColor="#276749" /* Darker green for better contrast */
              hoverBgColor="#1C4532"
              onClick={() => navigate('/used-car-check')}
            />
          </SimpleGrid>

          {/* Professional bottom section */}
          <Box 
            bg="rgba(255, 255, 255, 0.1)" 
            p={{ base: 6, md: 8 }} 
            borderRadius="xl" 
            boxShadow="0 5px 15px rgba(0,0,0,0.2)" 
            mt={{ base: 8, md: 12 }}
            textAlign="center"
            maxW="800px"
            border="1px solid rgba(255,255,255,0.15)"
            backdropFilter="blur(10px)"
          >
            <Heading size="md" mb={4} color="white" letterSpacing="wide" textShadow="0 1px 2px rgba(0,0,0,0.3)">
              PROFESSIONAL • RELIABLE • FAST
            </Heading>
            <Text fontSize={textSize} color="whiteAlpha.900" mb={6} fontWeight="medium">
              Select a service above to get started with your car needs
            </Text>
          </Box>
        </VStack>
      </Container>
    </Box>
  );
};
export default Home;
