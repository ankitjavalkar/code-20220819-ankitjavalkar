INPUT_FIXTURE = '[{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },{ "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },{ "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },{ "Gender": "Female", "HeightCm": 166, "WeightKg": 62},{"Gender": "Female", "HeightCm": 150, "WeightKg": 70},{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]'
BMI_CATEGORY_HEALTH_RISK_MAP = {
    'Underweight': {
        'category': 'Underweight',
        'bmi_range_min': 0,
        'bmi_range_max': 18.4,
        'health_risk': 'Malnutrition risk',
    },
    'Normal weight': {
        'category': 'Normal weight',
        'bmi_range_min': 18.5,
        'bmi_range_max': 24.9,
        'health_risk': 'Low risk',
    },
    'Overweight': {
        'category': 'Overweight',
        'bmi_range_min': 25,
        'bmi_range_max': 29.9,
        'health_risk': 'Enhanced risk',
    },
    'Moderately obese': {
        'category': 'Moderately obese',
        'bmi_range_min': 30,
        'bmi_range_max': 34.9,
        'health_risk': 'Medium risk',
    },
    'Severely obese': {
        'category': 'Severely obese',
        'bmi_range_min': 35,
        'bmi_range_max': 39.9,
        'health_risk': 'High risk',
    },
    'Very severely obese': {
        'category': 'Very severely obese',
        'bmi_range_min': 40,
        'bmi_range_max': 999999, # Can also use +inf from math module
        'health_risk': 'Very high risk',
    },
}