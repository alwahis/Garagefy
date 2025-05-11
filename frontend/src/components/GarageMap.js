import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Box, Text, VStack, Badge, Flex, Icon, Link, Button, Alert, AlertIcon, Spinner, Center } from '@chakra-ui/react';
import { FaPhone, FaExternalLinkAlt, FaEuroSign } from 'react-icons/fa';
import L from 'leaflet';

// Fix for default marker icons in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;

// Define marker icon paths
const ICON_URL = 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png';
const ICON_RETINA_URL = 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png';
const SHADOW_URL = 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png';

// Set up default icon configuration
L.Icon.Default.mergeOptions({
  iconUrl: ICON_URL,
  iconRetinaUrl: ICON_RETINA_URL,
  shadowUrl: SHADOW_URL,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
  shadowAnchor: [12, 41]
});

// Create default icon
const DefaultIcon = new L.Icon({
  iconUrl: ICON_URL,
  iconRetinaUrl: ICON_RETINA_URL,
  shadowUrl: SHADOW_URL,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
  shadowAnchor: [12, 41]
});

// Simple function to determine price range category
const getPriceRangeCategory = (repairPrices) => {
  if (!repairPrices || repairPrices.length === 0) return 'medium';
  
  const prices = repairPrices.map(item => {
    if (typeof item.average_price === 'number') return item.average_price;
    if (typeof item.average_price === 'string') {
      const numericValue = parseFloat(item.average_price.replace(/[^0-9.]/g, ''));
      return isNaN(numericValue) ? 0 : numericValue;
    }
    return 0;
  });
  
  const avgPrice = prices.reduce((sum, price) => sum + price, 0) / prices.length;
  
  if (avgPrice > 300) return 'high';
  if (avgPrice > 150) return 'medium';
  return 'low';
};

// Extremely simplified GarageMap component
const GarageMap = ({ garages, onSelectGarage }) => {
  // Default center on Luxembourg City
  const defaultCenter = [49.611622, 6.132263];
  
  // Calculate valid garages and their positions
  const validGarages = garages?.filter(garage => 
    garage && 
    garage.latitude && 
    garage.longitude && 
    !isNaN(parseFloat(garage.latitude)) && 
    !isNaN(parseFloat(garage.longitude))
  ) || [];
  
  // Calculate center from first valid garage or use default
  let mapCenter = defaultCenter;
  if (validGarages.length > 0) {
    const firstGarage = validGarages[0];
    const lat = parseFloat(firstGarage.latitude);
    const lng = parseFloat(firstGarage.longitude);
    if (!isNaN(lat) && !isNaN(lng)) {
      mapCenter = [lat, lng];
    }
  }
  
  // Simple inline styles to ensure map is visible
  const mapContainerStyle = {
    height: '600px',
    width: '100%',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    position: 'relative'
  };
  
  const mapStyle = {
    height: '100%',
    width: '100%'
  };
  
  return (
    <div style={mapContainerStyle} className="garage-map-container">
      <MapContainer 
        center={mapCenter}
        zoom={13} 
        style={mapStyle}
        attributionControl={true}
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {validGarages.map((garage) => {
          const lat = parseFloat(garage.latitude);
          const lng = parseFloat(garage.longitude);
          const markerKey = garage.id || `garage-${garage.name}-${lat}-${lng}`;
          
          return (
            <Marker 
              key={markerKey}
              position={[lat, lng]}
              icon={DefaultIcon}
            >
              <Popup>
                <VStack align="start" spacing={2} p={1}>
                  <Text fontWeight="bold" fontSize="md">{garage.name}</Text>
                  <Text fontSize="sm">{garage.address}</Text>
                  
                  {garage.repair_prices && garage.repair_prices.length > 0 ? (
                    <Box width="100%">
                      <Text fontWeight="semibold" fontSize="sm" mb={1}>
                        <Flex align="center">
                          <Icon as={FaEuroSign} mr={1} color="green.500" />
                          Repair Prices:
                        </Flex>
                      </Text>
                      {garage.repair_prices.slice(0, 3).map((item, idx) => (
                        <Flex key={idx} justify="space-between" fontSize="xs" mb={1}>
                          <Text>{item.service}</Text>
                          <Badge colorScheme={
                            item.average_price > 300 ? "red" : 
                            item.average_price > 150 ? "yellow" : "green"
                          }>
                            {typeof item.average_price === 'number' 
                              ? `€${item.average_price}` 
                              : item.average_price}
                          </Badge>
                        </Flex>
                      ))}
                    </Box>
                  ) : (
                    <Text fontSize="xs" color="gray.500">No price information available</Text>
                  )}
                  
                  <Flex justify="space-between" width="100%" mt={2}>
                    {garage.phone && (
                      <Link href={`tel:${garage.phone}`} isExternal fontSize="sm">
                        <Flex align="center">
                          <Icon as={FaPhone} mr={1} color="blue.500" />
                          Call
                        </Flex>
                      </Link>
                    )}
                    
                    {garage.website && (
                      <Link href={garage.website} isExternal fontSize="sm">
                        <Flex align="center">
                          <Icon as={FaExternalLinkAlt} mr={1} color="blue.500" />
                          Website
                        </Flex>
                      </Link>
                    )}
                    
                    <Button 
                      size="xs" 
                      colorScheme="blue" 
                      onClick={() => onSelectGarage(garage)}
                    >
                      Details
                    </Button>
                  </Flex>
                </VStack>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default GarageMap;
