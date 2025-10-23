import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import FixIt from './pages/FixIt';
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
              <Route path="/fix-it" element={<FixIt />} />
            </Routes>
          </Box>
        </Box>
      </ChakraProvider>
    </Router>
  );
}

export default App;
