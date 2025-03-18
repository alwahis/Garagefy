import React from 'react';
import { Box, Flex, Button, Text } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';

const Navigation = () => {
  return (
    <Box as="nav" bg="white" boxShadow="sm" py={4}>
      <Flex maxW="container.xl" mx="auto" px={4} justify="space-between" align="center">
        <RouterLink to="/">
          <Text fontSize="2xl" fontWeight="bold" color="blue.500">
            Garagefy
          </Text>
        </RouterLink>
        <Flex gap={4}>
          <Button as={RouterLink} to="/diagnose" colorScheme="blue" variant="link">
            Diagnose Problem
          </Button>
          <Button as={RouterLink} to="/garages" colorScheme="blue" variant="link">
            Find Garage
          </Button>
        </Flex>
      </Flex>
    </Box>
  );
};

export default Navigation;
