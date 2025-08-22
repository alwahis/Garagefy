import React from 'react';
import { Box, Heading, Text, VStack, Button, useColorModeValue } from '@chakra-ui/react';
import { FaTools } from 'react-icons/fa';

const FixIt = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('gray.800', 'white');
  const cardBg = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <Box p={4} maxW="1200px" mx="auto">
      <VStack spacing={6} align="stretch">
        <Box textAlign="center" py={8}>
          <Heading as="h1" size="2xl" mb={4} color={textColor}>
            Car Body Repair Services
          </Heading>
          <Text fontSize="lg" color="gray.500">
            Professional car body repair services to get your vehicle looking like new
          </Text>
        </Box>

        <Box 
          bg={cardBg} 
          p={6} 
          borderRadius="lg" 
          boxShadow="md"
          border="1px"
          borderColor={borderColor}
        >
          <VStack spacing={6}>
            <Box textAlign="center">
              <Box 
                display="inline-flex" 
                p={4} 
                bg="purple.100" 
                borderRadius="full"
                mb={4}
              >
                <FaTools size={40} color="#805AD5" />
              </Box>
              <Heading as="h2" size="lg" mb={4} color={textColor}>
                Body Repair Services
              </Heading>
              <Text color="gray.500" mb={6}>
                Our expert technicians can handle all types of car body repairs, from minor dents to major collision damage.
              </Text>
            </Box>

            <Box width="100%" mt={8}>
              <Heading as="h3" size="md" mb={4} color={textColor}>
                Services We Offer:
              </Heading>
              <VStack spacing={4} align="stretch">
                {[
                  'Dent Repair & Removal',
                  'Scratch & Paint Repair',
                  'Bumper Repair',
                  'Collision Repair',
                  'Paintless Dent Repair',
                  'Frame Straightening',
                  'Rust Repair',
                  'Full Body Painting'
                ].map((service, index) => (
                  <Box 
                    key={index}
                    p={4}
                    border="1px"
                    borderColor={borderColor}
                    borderRadius="md"
                    _hover={{
                      bg: 'purple.50',
                      borderColor: 'purple.200',
                      transform: 'translateX(4px)',
                      transition: 'all 0.2s'
                    }}
                  >
                    <Text>{service}</Text>
                  </Box>
                ))}
              </VStack>
            </Box>

            <Button 
              colorScheme="purple" 
              size="lg" 
              mt={8}
              onClick={() => window.location.href = 'tel:+1234567890'}
              leftIcon={<FaTools />}
            >
              Call for a Free Estimate
            </Button>
          </VStack>
        </Box>
      </VStack>
    </Box>
  );
};

export default FixIt;
