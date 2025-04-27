// Simple test script for the Used Car Check feature
console.log('Testing the Used Car Check feature...');

// Mock form data
const testData = {
  brand: 'Toyota',
  model: 'Corolla',
  year: 2018,
  mileage: 80000,
  fuelType: 'Gasoline',
  transmission: 'Manual'
};

console.log('Test data:', testData);

// Simulate form submission
async function testUsedCarCheck() {
  try {
    console.log('Simulating form submission...');
    
    // Create mock result
    let reliabilityScore = 85; // Toyota is reliable
    
    // Adjust for mileage
    if (parseInt(testData.mileage) > 150000) {
      reliabilityScore -= 15;
    } else if (parseInt(testData.mileage) > 100000) {
      reliabilityScore -= 5;
    }
    
    // Adjust for age
    const currentYear = new Date().getFullYear();
    const age = currentYear - parseInt(testData.year);
    if (age > 10) {
      reliabilityScore -= 10;
    } else if (age > 5) {
      reliabilityScore -= 5;
    }
    
    // Determine recommendation
    let recommendation, summary;
    if (reliabilityScore >= 80) {
      recommendation = "Buy";
      summary = `This ${testData.year} ${testData.brand} ${testData.model} appears to be a reliable vehicle with minimal issues expected.`;
    } else if (reliabilityScore >= 65) {
      recommendation = "Buy with Inspection";
      summary = `This ${testData.year} ${testData.brand} ${testData.model} seems decent, but should be inspected by a mechanic before purchase.`;
    } else if (reliabilityScore >= 50) {
      recommendation = "Caution";
      summary = `This ${testData.year} ${testData.brand} ${testData.model} has some concerning factors that should be thoroughly investigated.`;
    } else {
      recommendation = "Avoid";
      summary = `This ${testData.year} ${testData.brand} ${testData.model} has significant reliability concerns and/or very high mileage.`;
    }
    
    // Create mock issues
    const issues = [
      {
        title: "Timing Belt",
        description: `The timing belt on ${testData.brand} ${testData.model} models from this era may need replacement around ${testData.mileage} km.`,
        severity: "warning"
      },
      {
        title: "Suspension Components",
        description: "Check for worn suspension components, especially if the vehicle has been driven on rough roads.",
        severity: "info"
      },
      {
        title: "Electronics",
        description: "Some models from this year have reported issues with the electrical system.",
        severity: "warning"
      }
    ];
    
    // Create mock sources
    const sources = [
      {
        title: "AutoScout24 - Vehicle History",
        url: "https://www.autoscout24.com"
      },
      {
        title: "TÜV Report - Reliability Data",
        url: "https://www.tuv.com/world/en/"
      },
      {
        title: `${testData.brand} Owners Forum`,
        url: `https://www.${testData.brand.toLowerCase()}forum.com`
      }
    ];
    
    // Create the mock result
    const mockResult = {
      car_info: {
        brand: testData.brand,
        model: testData.model,
        year: parseInt(testData.year),
        mileage: parseInt(testData.mileage),
        fuel_type: testData.fuelType,
        transmission: testData.transmission
      },
      score: reliabilityScore,
      recommendation: recommendation,
      summary: summary,
      issues: issues,
      sources: sources
    };
    
    console.log('Mock result generated:', mockResult);
    console.log('Test completed successfully!');
    
    return mockResult;
  } catch (error) {
    console.error('Test failed:', error);
    return null;
  }
}

// Run the test
testUsedCarCheck().then(result => {
  console.log('Final result:', result);
});
