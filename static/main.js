// Navigation Functions
function showHome() {
    hideAllSections();
    document.getElementById('homeScreen').classList.add('active');
}

function showDiagnosis() {
    hideAllSections();
    document.getElementById('diagnosisSection').classList.add('active');
    loadCarBrands();
}

function showGarage() {
    hideAllSections();
    document.getElementById('garageSection').classList.add('active');
}

function hideAllSections() {
    const sections = ['homeScreen', 'diagnosisSection', 'garageSection'];
    sections.forEach(section => {
        document.getElementById(section)?.classList.remove('active');
    });
}

// Car selection handling
async function loadCarBrands() {
    try {
        const response = await fetch('/api/brands');
        const brands = await response.json();
        const brandSelect = document.getElementById('carBrand');
        brandSelect.innerHTML = '<option value="">Select Brand</option>';
        brands.forEach(brand => {
            brandSelect.innerHTML += `<option value="${brand}">${brand}</option>`;
        });
    } catch (error) {
        console.error('Error loading car brands:', error);
    }
}

async function loadCarModels(brand) {
    try {
        const response = await fetch(`/api/models/${brand}`);
        const models = await response.json();
        const modelSelect = document.getElementById('carModel');
        modelSelect.innerHTML = '<option value="">Select Model</option>';
        models.forEach(model => {
            modelSelect.innerHTML += `<option value="${model}">${model}</option>`;
        });
        modelSelect.disabled = false;
    } catch (error) {
        console.error('Error loading car models:', error);
    }
}

async function loadCarYears(brand, model) {
    try {
        const response = await fetch(`/api/years/${brand}/${model}`);
        const years = await response.json();
        const yearSelect = document.getElementById('carYear');
        yearSelect.innerHTML = '<option value="">Select Year</option>';
        years.forEach(year => {
            yearSelect.innerHTML += `<option value="${year}">${year}</option>`;
        });
        yearSelect.disabled = false;
    } catch (error) {
        console.error('Error loading car years:', error);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Car selection event listeners
    const brandSelect = document.getElementById('carBrand');
    const modelSelect = document.getElementById('carModel');
    const yearSelect = document.getElementById('carYear');

    brandSelect?.addEventListener('change', (e) => {
        const brand = e.target.value;
        if (brand) {
            loadCarModels(brand);
        } else {
            modelSelect.innerHTML = '<option value="">Select Model</option>';
            modelSelect.disabled = true;
            yearSelect.innerHTML = '<option value="">Select Year</option>';
            yearSelect.disabled = true;
        }
    });

    modelSelect?.addEventListener('change', (e) => {
        const model = e.target.value;
        const brand = brandSelect.value;
        if (model && brand) {
            loadCarYears(brand, model);
        } else {
            yearSelect.innerHTML = '<option value="">Select Year</option>';
            yearSelect.disabled = true;
        }
    });

    // Diagnosis form submission
    const diagnoseForm = document.getElementById('diagnoseForm');
    diagnoseForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const symptoms = document.getElementById('symptoms').value;
        const carBrand = brandSelect.value;
        const carModel = modelSelect.value;
        const carYear = yearSelect.value;

        if (!symptoms || !carBrand || !carModel || !carYear) {
            alert('Please fill in all fields');
            return;
        }

        try {
            showLoading('Diagnosing your car...');
            const response = await fetch('/api/diagnose', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    symptoms,
                    car_brand: carBrand,
                    car_model: carModel,
                    year: parseInt(carYear)
                })
            });

            const result = await response.json();
            hideLoading();

            if (result.error) {
                alert('Error: ' + result.error);
            } else {
                const diagnosisResult = document.getElementById('diagnosisResult');
                diagnosisResult.innerHTML = `
                    <div class="mt-8 p-6 bg-white rounded-lg shadow-lg">
                        <h3 class="text-xl font-semibold mb-4">Diagnosis Result</h3>
                        <p class="text-gray-700">${result.diagnosis}</p>
                        ${result.recommendations ? `
                            <h4 class="text-lg font-semibold mt-4 mb-2">Recommendations:</h4>
                            <ul class="list-disc pl-5">
                                ${result.recommendations.map(rec => `<li class="text-gray-700">${rec}</li>`).join('')}
                            </ul>
                        ` : ''}
                    </div>
                `;
                diagnosisResult.scrollIntoView({ behavior: 'smooth' });
            }
        } catch (error) {
            hideLoading();
            console.error('Error diagnosing car:', error);
            alert('An error occurred while diagnosing your car. Please try again.');
        }
    });
});

// Loading overlay functions
function showLoading(message = 'Loading...') {
    const loading = document.getElementById('loading');
    const loadingMessage = document.getElementById('loadingMessage');
    if (loadingMessage) loadingMessage.textContent = message;
    loading?.classList.remove('hidden');
}

function hideLoading() {
    const loading = document.getElementById('loading');
    loading?.classList.add('hidden');
}
