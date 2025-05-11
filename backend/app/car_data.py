"""
Car data module containing supported car brands and models
"""

CAR_DATA = {
    # German Brands
    'BMW': {
        'models': ['1 Series', '2 Series', '3 Series', '4 Series', '5 Series', '6 Series', '7 Series', '8 Series', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'Z4', 'i3', 'i4', 'i7', 'i8', 'iX', 'iX3', 'M2', 'M3', 'M4', 'M5', 'M8'],
        'manual': 'BMW Factory Service Manual'
    },
    'Mercedes-Benz': {
        'models': ['A-Class', 'B-Class', 'C-Class', 'CLA', 'CLS', 'E-Class', 'EQA', 'EQB', 'EQC', 'EQE', 'EQS', 'G-Class', 'GLA', 'GLB', 'GLC', 'GLE', 'GLS', 'S-Class', 'SL', 'SLC', 'AMG GT', 'Maybach S-Class', 'V-Class', 'Vito'],
        'manual': 'Mercedes-Benz Workshop Information System'
    },
    'Volkswagen': {
        'models': ['Arteon', 'Atlas', 'Caddy', 'California', 'Golf', 'Golf GTI', 'Golf R', 'ID.3', 'ID.4', 'ID.5', 'ID.Buzz', 'Jetta', 'Passat', 'Polo', 'Sharan', 'T-Cross', 'T-Roc', 'Taigo', 'Tiguan', 'Touareg', 'Touran', 'Transporter', 'Up!'],
        'manual': 'Volkswagen Service Manual'
    },
    'Audi': {
        'models': ['A1', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'e-tron', 'e-tron GT', 'Q2', 'Q3', 'Q4 e-tron', 'Q5', 'Q7', 'Q8', 'R8', 'RS3', 'RS4', 'RS5', 'RS6', 'RS7', 'RS Q3', 'RS Q8', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'TT', 'TTS'],
        'manual': 'Audi Service Manual'
    },
    'Porsche': {
        'models': ['718 Boxster', '718 Cayman', '911', 'Cayenne', 'Macan', 'Panamera', 'Taycan'],
        'manual': 'Porsche Technical Information System'
    },
    'Opel': {
        'models': ['Astra', 'Corsa', 'Crossland', 'Grandland', 'Insignia', 'Mokka', 'Combo', 'Vivaro', 'Zafira'],
        'manual': 'Opel Technical Information System'
    },
    
    # Japanese Brands
    'Toyota': {
        'models': ['Auris', 'Avensis', 'Aygo', 'C-HR', 'Camry', 'Corolla', 'GR Supra', 'GR Yaris', 'Highlander', 'Hilux', 'Land Cruiser', 'Mirai', 'Prius', 'Proace', 'RAV4', 'Supra', 'Yaris', 'Yaris Cross'],
        'manual': 'Toyota Technical Information System'
    },
    'Honda': {
        'models': ['Accord', 'Civic', 'CR-V', 'e', 'e:Ny1', 'HR-V', 'Jazz', 'NSX', 'Insight', 'Odyssey', 'Pilot', 'Ridgeline'],
        'manual': 'Honda Service Express'
    },
    'Mazda': {
        'models': ['2', '3', '6', 'CX-3', 'CX-30', 'CX-5', 'CX-60', 'CX-9', 'MX-5', 'MX-30'],
        'manual': 'Mazda Workshop Manual'
    },
    'Nissan': {
        'models': ['350Z', '370Z', 'Ariya', 'GT-R', 'Juke', 'Leaf', 'Micra', 'Navara', 'Note', 'Qashqai', 'X-Trail'],
        'manual': 'Nissan Electronic Service Manual'
    },
    'Subaru': {
        'models': ['BRZ', 'Crosstrek', 'Forester', 'Impreza', 'Legacy', 'Outback', 'WRX', 'WRX STI'],
        'manual': 'Subaru Technical Information System'
    },
    'Mitsubishi': {
        'models': ['ASX', 'Eclipse Cross', 'L200', 'Outlander', 'Space Star'],
        'manual': 'Mitsubishi Service Information'
    },
    'Lexus': {
        'models': ['CT', 'ES', 'IS', 'LC', 'LS', 'NX', 'RX', 'UX'],
        'manual': 'Lexus Technical Information System'
    },
    'Suzuki': {
        'models': ['Across', 'Ignis', 'Jimny', 'S-Cross', 'Swift', 'Swace', 'Vitara'],
        'manual': 'Suzuki Service Manual'
    },
    
    # French Brands
    'Renault': {
        'models': ['Arkana', 'Austral', 'Captur', 'Clio', 'Espace', 'Kadjar', 'Kangoo', 'Megane', 'Scenic', 'Trafic', 'Twingo', 'Zoe'],
        'manual': 'Renault Service Documentation'
    },
    'Peugeot': {
        'models': ['108', '208', '2008', '308', '3008', '408', '508', '5008', 'Rifter', 'Traveller'],
        'manual': 'Peugeot Service Documentation'
    },
    'Citroën': {
        'models': ['Berlingo', 'C1', 'C3', 'C3 Aircross', 'C4', 'C4 Cactus', 'C5 Aircross', 'C5 X', 'SpaceTourer'],
        'manual': 'Citroën Service Documentation'
    },
    'DS': {
        'models': ['DS 3', 'DS 3 Crossback', 'DS 4', 'DS 7 Crossback', 'DS 9'],
        'manual': 'DS Service Documentation'
    },
    'Alpine': {
        'models': ['A110'],
        'manual': 'Alpine Service Documentation'
    },
    
    # Italian Brands
    'Fiat': {
        'models': ['500', '500X', 'Doblo', 'Panda', 'Tipo'],
        'manual': 'Fiat eLearn'
    },
    'Alfa Romeo': {
        'models': ['Giulia', 'Giulietta', 'Stelvio', 'Tonale', '4C', '8C', 'Brera', 'Spider'],
        'manual': 'Alfa Romeo Service Information'
    },
    'Ferrari': {
        'models': ['296 GTB', '296 GTS', '812', 'F8', 'Roma', 'SF90', 'Portofino', 'Purosangue', 'LaFerrari', '488', 'California', 'GTC4Lusso'],
        'manual': 'Ferrari Technical Documentation'
    },
    'Lamborghini': {
        'models': ['Aventador', 'Huracan', 'Urus', 'Revuelto', 'Sian', 'Countach', 'Gallardo', 'Murcielago'],
        'manual': 'Lamborghini Technical Documentation'
    },
    'Maserati': {
        'models': ['Ghibli', 'Grecale', 'Levante', 'MC20', 'Quattroporte', 'GranTurismo', 'GranCabrio'],
        'manual': 'Maserati Technical Documentation'
    },
    'Pagani': {
        'models': ['Huayra', 'Zonda', 'Utopia'],
        'manual': 'Pagani Technical Documentation'
    },
    
    # British Brands
    'Land Rover': {
        'models': ['Defender', 'Discovery', 'Discovery Sport', 'Range Rover', 'Range Rover Evoque', 'Range Rover Sport', 'Range Rover Velar', 'Range Rover SV'],
        'manual': 'Land Rover Technical Information'
    },
    'Jaguar': {
        'models': ['E-Pace', 'F-Pace', 'F-Type', 'I-Pace', 'XE', 'XF', 'XJ', 'XK', 'S-Type', 'X-Type'],
        'manual': 'Jaguar Technical Information'
    },
    'MINI': {
        'models': ['Clubman', 'Convertible', 'Countryman', 'Electric', 'Hatch', 'John Cooper Works', 'Paceman', 'Roadster', 'Coupe'],
        'manual': 'MINI Technical Information'
    },
    'Bentley': {
        'models': ['Bentayga', 'Continental GT', 'Flying Spur', 'Mulsanne', 'Bacalar', 'Batur', 'Arnage', 'Brooklands', 'Azure'],
        'manual': 'Bentley Technical Information'
    },
    'Aston Martin': {
        'models': ['DB11', 'DBS', 'DBX', 'Vantage', 'Valkyrie', 'Vanquish', 'Rapide', 'One-77', 'Vulcan', 'DB9', 'DB12'],
        'manual': 'Aston Martin Workshop Information'
    },
    'Rolls-Royce': {
        'models': ['Cullinan', 'Dawn', 'Ghost', 'Phantom', 'Wraith', 'Spectre', 'Silver Shadow', 'Silver Seraph', 'Corniche'],
        'manual': 'Rolls-Royce Technical Information'
    },
    'McLaren': {
        'models': ['720S', '765LT', 'Artura', 'GT', 'Elva', 'Senna', 'Speedtail', 'P1', '570S', '650S', '675LT'],
        'manual': 'McLaren Technical Information'
    },
    'Lotus': {
        'models': ['Emira', 'Evija', 'Eletre', 'Elise', 'Exige', 'Evora', 'Esprit'],
        'manual': 'Lotus Service Information'
    },
    'Morgan': {
        'models': ['Plus Four', 'Plus Six', '3 Wheeler', 'Aero 8', 'Roadster'],
        'manual': 'Morgan Workshop Manual'
    },
    'Caterham': {
        'models': ['Seven 270', 'Seven 310', 'Seven 360', 'Seven 420', 'Seven 620', 'CSR'],
        'manual': 'Caterham Technical Information'
    },
    
    # Swedish Brands
    'Volvo': {
        'models': ['C40', 'S60', 'S90', 'V60', 'V90', 'XC40', 'XC60', 'XC90', 'EX30', 'EX90', 'C30', 'V40', 'V50', 'S40', 'XC70'],
        'manual': 'Volvo VIDA'
    },
    'Koenigsegg': {
        'models': ['Jesko', 'Gemera', 'Regera', 'CC8S', 'CCR', 'CCX', 'Agera', 'One:1'],
        'manual': 'Koenigsegg Technical Documentation'
    },
    
    # Spanish Brands
    'SEAT': {
        'models': ['Arona', 'Ateca', 'Ibiza', 'Leon', 'Tarraco', 'Mii', 'Alhambra'],
        'manual': 'SEAT Workshop Information'
    },
    'Cupra': {
        'models': ['Formentor', 'Born', 'Ateca', 'Leon', 'Tavascan', 'Terramar'],
        'manual': 'Cupra Technical Information'
    },
    
    # Czech Brands
    'Skoda': {
        'models': ['Citigo', 'Fabia', 'Kamiq', 'Karoq', 'Kodiaq', 'Octavia', 'Rapid', 'Scala', 'Superb', 'Enyaq'],
        'manual': 'Skoda Workshop Manual'
    },
    
    # Korean Brands
    'Hyundai': {
        'models': ['Bayon', 'i10', 'i20', 'i30', 'IONIQ', 'IONIQ 5', 'IONIQ 6', 'Kona', 'Santa Fe', 'Tucson', 'Accent', 'Elantra', 'Sonata', 'Palisade', 'Veloster', 'Genesis', 'Nexo', 'Venue'],
        'manual': 'Hyundai Technical Information'
    },
    'Kia': {
        'models': ['Ceed', 'EV6', 'Niro', 'Picanto', 'ProCeed', 'Rio', 'Sorento', 'Sportage', 'Stinger', 'Stonic', 'XCeed', 'Optima', 'Forte', 'Soul', 'Telluride', 'Carnival', 'Seltos', 'EV9', 'Cadenza', 'K5', 'K9'],
        'manual': 'Kia Technical Information'
    },
    'Genesis': {
        'models': ['G70', 'G80', 'G90', 'GV60', 'GV70', 'GV80', 'X Convertible', 'X Speedium Coupe'],
        'manual': 'Genesis Technical Information'
    },
    'SsangYong': {
        'models': ['Korando', 'Musso', 'Rexton', 'Tivoli', 'Torres'],
        'manual': 'SsangYong Service Information'
    },
    
    # American Brands
    'Ford': {
        'models': ['Bronco', 'EcoSport', 'Edge', 'Explorer', 'Fiesta', 'Focus', 'Galaxy', 'Kuga', 'Mondeo', 'Mustang', 'Mustang Mach-E', 'Puma', 'Ranger', 'S-Max', 'Transit'],
        'manual': 'Ford Workshop Manual'
    },
    'Chevrolet': {
        'models': ['Blazer', 'Bolt', 'Camaro', 'Corvette', 'Equinox', 'Silverado', 'Suburban', 'Tahoe', 'Trailblazer', 'Traverse'],
        'manual': 'GM Service Information'
    },
    'Jeep': {
        'models': ['Avenger', 'Cherokee', 'Compass', 'Gladiator', 'Grand Cherokee', 'Renegade', 'Wrangler'],
        'manual': 'Jeep Service Information'
    },
    'Tesla': {
        'models': ['Model 3', 'Model S', 'Model X', 'Model Y', 'Cybertruck'],
        'manual': 'Tesla Service Information'
    },
    'Cadillac': {
        'models': ['CT4', 'CT5', 'Escalade', 'XT4', 'XT5', 'XT6'],
        'manual': 'GM Service Information'
    },
    
    # Chinese Brands
    'MG': {
        'models': ['3', '4', '5', 'HS', 'ZS', 'ZS EV', 'Marvel R', 'MG5 Electric', 'Cyberster', 'MG6', 'MG7', 'RX5'],
        'manual': 'MG Service Information'
    },
    'BYD': {
        'models': ['Atto 3', 'Han', 'Tang', 'Seal', 'Dolphin', 'Yuan Plus', 'Song', 'Qin', 'e6', 'Destroyer 05', 'Yangwang U8', 'Yangwang U9'],
        'manual': 'BYD Service Information'
    },
    'Polestar': {
        'models': ['1', '2', '3', '4', '5', '6'],
        'manual': 'Polestar Service Information'
    },
    'NIO': {
        'models': ['ET5', 'ET7', 'ES6', 'ES7', 'ES8', 'EC6', 'EC7', 'EL6', 'EL7'],
        'manual': 'NIO Service Information'
    },
    'Xpeng': {
        'models': ['P5', 'P7', 'G3', 'G9', 'G6'],
        'manual': 'Xpeng Service Information'
    },
    'Geely': {
        'models': ['Coolray', 'Azkarra', 'Okavango', 'Emgrand', 'Geometry A', 'Geometry C', 'Xingyue', 'Boyue'],
        'manual': 'Geely Service Information'
    },
    'Great Wall': {
        'models': ['Haval H6', 'Haval Jolion', 'Haval H9', 'Tank 300', 'Tank 500', 'Ora Cat', 'Ora Good Cat', 'Wey Coffee 01', 'Wey Mocha'],
        'manual': 'Great Wall Service Information'
    },
    'Li Auto': {
        'models': ['L7', 'L8', 'L9', 'One'],
        'manual': 'Li Auto Service Information'
    },
    'Lynk & Co': {
        'models': ['01', '02', '03', '05', '06', '09'],
        'manual': 'Lynk & Co Service Information'
    },
    
    # Indian Brands
    'Tata': {
        'models': ['Nexon', 'Harrier', 'Safari', 'Tiago', 'Tigor', 'Altroz', 'Punch', 'Curvv'],
        'manual': 'Tata Service Information'
    },
    'Mahindra': {
        'models': ['XUV700', 'XUV300', 'Thar', 'Scorpio', 'Bolero', 'XUV400', 'BE', 'XEV'],
        'manual': 'Mahindra Service Information'
    },
    'Maruti Suzuki': {
        'models': ['Swift', 'Baleno', 'Brezza', 'Ertiga', 'Dzire', 'Wagon R', 'Alto', 'Celerio', 'Ciaz', 'Jimny'],
        'manual': 'Maruti Suzuki Service Information'
    },
    
    # Vietnamese Brands
    'VinFast': {
        'models': ['VF 3', 'VF 5', 'VF 6', 'VF 7', 'VF 8', 'VF 9', 'VF e34', 'President', 'Lux A2.0', 'Lux SA2.0'],
        'manual': 'VinFast Service Information'
    }
}
