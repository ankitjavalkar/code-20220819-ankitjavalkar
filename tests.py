from unittest import TestCase
import pandas as pd

from bmicalc import BMICalculator

class TestBMICalculator(TestCase):
    def setUp(self):
        self.my_bmi_obj = BMICalculator()

    def test_calculate_bmi_result_in_m_and_kg(self):
        ht_in_m = 2
        wt_in_kg = 4
        ht_unit = 'm'
        wt_unit = 'kg'
        expected_bmi_val = 1

        bmi_val = self.my_bmi_obj._calculate_bmi(
            height=ht_in_m,
            weight=wt_in_kg,
            height_unit=ht_unit,
            weight_unit=wt_unit,
        )
        self.assertEqual(bmi_val, 1)

    def test_calculate_bmi_result_in_cm_and_g(self):
        ht_in_cm = 200
        wt_in_g = 4000
        ht_unit = 'cm'
        wt_unit = 'g'
        expected_bmi_val = 1

        bmi_val = self.my_bmi_obj._calculate_bmi(
            height=ht_in_cm,
            weight=wt_in_g,
            height_unit=ht_unit,
            weight_unit=wt_unit,
        )
        self.assertEqual(bmi_val, 1)

    def test_calculate_bmi_value_error(self):
        ht_in_m = 2
        wt_in_kg = 4
        invalid_ht_unit = 'random_str'
        valid_wt_unit = 'kg'

        self.assertRaises(
            ValueError,
            self.my_bmi_obj._calculate_bmi,
            ht_in_m,
            wt_in_kg,
            invalid_ht_unit,
            valid_wt_unit,
        )

        valid_ht_unit = 'm'
        invalid_wt_unit = 'random_str'

        self.assertRaises(
            ValueError,
            self.my_bmi_obj._calculate_bmi,
            ht_in_m,
            wt_in_kg,
            valid_ht_unit,
            invalid_wt_unit,
        )

    def test_get_bmi_cat_and_health_risk(self):
        underweight_bmi = 5
        normal_weight_bmi = 22
        overweight_bmi = 27
        mod_obese_bmi = 32
        sev_obese_bmi = 37
        very_sev_obese_bmi = 43

        self.assertEqual(
            self.my_bmi_obj._get_bmi_cat_and_health_risk(underweight_bmi),
            {
                'category': 'Underweight',
                'bmi_range_min': 0,
                'bmi_range_max': 18.4,
                'health_risk': 'Malnutrition risk',
            },
        )
        self.assertEqual(
            self.my_bmi_obj._get_bmi_cat_and_health_risk(normal_weight_bmi),
            {
                'category': 'Normal weight',
                'bmi_range_min': 18.5,
                'bmi_range_max': 24.9,
                'health_risk': 'Low risk',
            },
        )
        self.assertEqual(
            self.my_bmi_obj._get_bmi_cat_and_health_risk(overweight_bmi),
            {
                'category': 'Overweight',
                'bmi_range_min': 25,
                'bmi_range_max': 29.9,
                'health_risk': 'Enhanced risk',
            },
        )
        self.assertEqual(
            self.my_bmi_obj._get_bmi_cat_and_health_risk(mod_obese_bmi),
            {
                'category': 'Moderately obese',
                'bmi_range_min': 30,
                'bmi_range_max': 34.9,
                'health_risk': 'Medium risk',
            },
        )
        self.assertEqual(
            self.my_bmi_obj._get_bmi_cat_and_health_risk(sev_obese_bmi),
            {
                'category': 'Severely obese',
                'bmi_range_min': 35,
                'bmi_range_max': 39.9,
                'health_risk': 'High risk',
            },
        )
        self.assertEqual(
            self.my_bmi_obj._get_bmi_cat_and_health_risk(very_sev_obese_bmi),
            {
                'category': 'Very severely obese',
                'bmi_range_min': 40,
                'bmi_range_max': 999999,
                'health_risk': 'Very high risk',
            },
        )

    def test_get_category_count(self):
        self.my_bmi_obj.load_data(json_data='[{"Gender": "Male", "HeightCm": 171, "WeightKg": 100 }]')
        sample_bmi_res = self.my_bmi_obj.get_bmi_result()
        self.assertEqual(
            self.my_bmi_obj._get_category_count(sample_bmi_res),
            {'Moderately obese': 1},
        )


class TestBMICalculatorWithPandas(TestCase):
    def setUp(self):
        self.my_bmi_obj = BMICalculator()
        self.fixture = '[{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },{ "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },{ "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },{ "Gender": "Female", "HeightCm": 166, "WeightKg": 62},{"Gender": "Female", "HeightCm": 150, "WeightKg": 70},{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]'
        self.input_df = pd.read_json(self.fixture)

    def test_load_data_with_pandas(self):
        self.assertTrue(
            self.input_df.equals(
                self.my_bmi_obj.load_data_with_pandas(
                    json_data=self.fixture,
                ),
            )
        )
        self.assertTrue(
            self.input_df.equals(
                self.my_bmi_obj.ht_wt_params
            )
        )

    def test_get_bmi_result_with_pandas(self):
        expected_bmi_dict = {
            'Gender': {
                0: 'Male',
                1: 'Male',
                2: 'Male',
                3: 'Female',
                4: 'Female',
                5: 'Female'
            },
            'HeightCm': {0: 171, 1: 161, 2: 180, 3: 166, 4: 150, 5: 167},
            'WeightKg': {0: 96, 1: 85, 2: 77, 3: 62, 4: 70, 5: 82},
            'Bmi': {
                0: 32.83061454806607,
                1: 32.79194475521777,
                2: 23.76543209876543,
                3: 22.49963710262738,
                4: 31.11111111111111,
                5: 29.402273297715947
            },
            'BmiCategory': {
                0: 'Moderately obese',
                1: 'Moderately obese',
                2: 'Normal weight',
                3: 'Normal weight',
                4: 'Moderately obese',
                5: 'Overweight'
            },
            'HealthRisk': {
                0: 'Medium risk',
                1: 'Medium risk',
                2: 'Low risk',
                3: 'Low risk',
                4: 'Medium risk',
                5: 'Enhanced risk'
            }
        }
        expected_bmi_result = pd.DataFrame()
        expected_bmi_result = expected_bmi_result.from_dict(
            expected_bmi_dict
        )
        self.my_bmi_obj.load_data_with_pandas()
        bmi_res = self.my_bmi_obj.get_bmi_result_with_pandas()

        self.assertTrue(
            expected_bmi_result.equals(
                bmi_res
            )
        )
        self.assertTrue(
            expected_bmi_result.equals(
                self.my_bmi_obj.bmi_result
            )
        )

    def test_display_category_count_with_pandas(self):
        expected_agg_data_dict = {
            'Moderately obese': 3,
            'Normal weight': 2,
            'Overweight': 1
        }
        expected_agg_data = pd.Series(expected_agg_data_dict)
        self.my_bmi_obj.load_data_with_pandas()
        self.my_bmi_obj.get_bmi_result_with_pandas()
        aggregated_data = self.my_bmi_obj.display_category_count_with_pandas()

        self.assertTrue(
            expected_agg_data.equals(
                aggregated_data
            )
        )
