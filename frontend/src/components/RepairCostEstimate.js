import React from 'react';
import {
  Box,
  Heading,
  Text,
  VStack,
  HStack,
  Icon,
  Badge,
  Button,
  useColorModeValue,
  Divider
} from '@chakra-ui/react';
import { FaBolt, FaEuroSign, FaChartBar } from 'react-icons/fa';

const RepairCostEstimate = ({ costEstimate, onBack }) => {
  const bgColor = useColorModeValue('white', 'darkBg.800');
  const borderColor = useColorModeValue('gray.200', 'darkBg.600');
  const headingBgColor = useColorModeValue('blue.500', 'brand.500');
  const textColor = useColorModeValue('gray.800', 'white');
  const secondaryTextColor = useColorModeValue('gray.600', 'gray.300');

  if (!costEstimate) {
    return (
      <Box textAlign="center" p={5}>
        <Text>No cost estimate available</Text>
        <Button mt={4} onClick={onBack}>Back to Diagnosis</Button>
      </Box>
    );
  }

  // Parse the probability distribution from string if needed
  let probabilities = costEstimate.probability_distribution || [];
  if (typeof probabilities === 'string') {
    try {
      probabilities = JSON.parse(probabilities);
    } catch (e) {
      console.error('Failed to parse probability distribution', e);
      probabilities = [];
    }
  }

  return (
    <Box 
      bg={bgColor} 
      borderWidth="1px" 
      borderColor={borderColor} 
      borderRadius="xl"
      overflow="hidden"
      boxShadow="xl"
      mt={6}
      mb={6}
      maxW="800px"
      mx="auto"
    >
      <Box bg={headingBgColor} p={6}>
        <HStack spacing={3}>
          <Icon as={FaEuroSign} w={6} h={6} color="white" />
          <Heading size="md" color="white">Repair Cost Estimate (Luxembourg)</Heading>
        </HStack>
      </Box>

      <Box p={6}>
        <VStack spacing={6} align="stretch">
          <Box>
            <Heading size="md" mb={4} color={textColor}>
              Estimated Cost Range: {costEstimate.min_cost}-{costEstimate.max_cost} {costEstimate.currency}
            </Heading>
            
            <Divider my={4} />
            
            <Text fontWeight="bold" mb={3} color={textColor}>Cost Breakdown (with probabilities):</Text>
            <VStack align="stretch" spacing={3}>
              {probabilities.map((prob, index) => {
                const [probability, range] = prob;
                const percentage = Math.round(probability * 100);
                const [min, max] = range.split('-');
                
                // Calculate width for the probability bar
                const barWidth = `${percentage}%`;
                
                return (
                  <Box key={index}>
                    <HStack mb={1}>
                      <Text fontWeight="bold" color={textColor}>{percentage}% chance:</Text>
                      <Text color={textColor}>{range} {costEstimate.currency}</Text>
                    </HStack>
                    <Box 
                      w="100%" 
                      h="12px" 
                      bg="gray.100" 
                      borderRadius="full" 
                      overflow="hidden"
                    >
                      <Box 
                        w={barWidth} 
                        h="100%" 
                        bg="blue.500" 
                        borderRadius="full"
                      />
                    </Box>
                  </Box>
                );
              })}
            </VStack>
            
            <Divider my={4} />
            
            <Box mt={4} p={3} bg="blue.50" borderRadius="md" borderWidth="1px" borderColor="blue.200">
              <HStack>
                <Icon as={FaChartBar} color="blue.500" />
                <Text fontWeight="bold" color="blue.700">Adjustment Factors:</Text>
              </HStack>
              <Text color="gray.700" mt={2}>
                • Brand Factor: {costEstimate.multipliers?.brand || 1.0}x
              </Text>
              <Text color="gray.700">
                • Age Factor: {costEstimate.multipliers?.age || 1.0}x
              </Text>
              <Text color="gray.700">
                • Total Multiplier: {costEstimate.multipliers?.total || 1.0}x
              </Text>
            </Box>
          </Box>
          
          <Button 
            onClick={onBack} 
            colorScheme="brand" 
            size="lg" 
            leftIcon={<Icon as={FaBolt} />}
          >
            Back to Diagnosis
          </Button>
        </VStack>
      </Box>
    </Box>
  );
};

export default RepairCostEstimate;
