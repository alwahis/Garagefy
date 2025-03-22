import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import DiagnosisForm from './components/DiagnosisForm';
import GarageList from './pages/GarageList';
import UsedCarCheck from './pages/UsedCarCheck';
import Navbar from './components/Navbar';
import { Box } from '@chakra-ui/react';
import theme from './theme';

function App() {
  return (
    <Router>
      <ChakraProvider theme={theme}>
        <Box minH="100vh" display="flex" flexDirection="column" bg="white">
          <Navbar />
          <Box flex="1" pb={16}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/diagnosis" element={<DiagnosisForm />} />
              <Route path="/diagnose-car" element={<DiagnosisForm />} />
              <Route path="/garages" element={<GarageList />} />
              <Route path="/find-garage" element={<GarageList />} />
              <Route path="/used-car-check" element={<UsedCarCheck />} />
            </Routes>
          </Box>
        </Box>
      </ChakraProvider>
    </Router>
  );
}

export default App;
