import json
import os

import pandas as pd

from literals import INPUT_FIXTURE, BMI_CATEGORY_HEALTH_RISK_MAP


class BMICalculator():
    bmi_category_health_risk_map = BMI_CATEGORY_HEALTH_RISK_MAP
    height_unit = 'cm' # Can be `m` or `cm`
    weight_unit = 'kg' # Can be `g` or `kg`

    def load_data(self, json_data=INPUT_FIXTURE):
        if os.path.isfile(json_data) and json_data.endswith('.json'):
            with open(json_data, 'r') as jf:
                json_str = jf.read()
        else:
            json_str = json_data
        self.ht_wt_params = json.loads(json_str)
        return self.ht_wt_params

    def _calculate_bmi(self, height, weight, height_unit, weight_unit):
        if height_unit not in ['cm', 'm']:
            raise ValueError("height_unit parameter must be 'cm' or 'm'")
        if weight_unit not in ['g', 'kg']:
            raise ValueError("weight_unit parameter must be 'g' or 'kg'")
        if not height or not weight or height == 0:
            raise ValueError("Height and Weight cannot be 0 or Null")

        if height_unit == 'cm':
            height = self._convert_cm_to_m(height)
        if weight_unit == 'g':
            weight = self._convert_g_to_kg(weight)


        bmi_value = weight / (height ** 2)
        return bmi_value

    def _get_bmi_cat_and_health_risk(self, bmi_value):
        for ref in self.bmi_category_health_risk_map.values():
            if ref.get('bmi_range_min') <= bmi_value <= ref.get('bmi_range_max'):
                return ref
        return None

    def get_bmi_result(self):
        if not self.ht_wt_params:
            raise ValueError(
                'No input data available. Use `load_data` method to add'
                ' height, weight, input data'
            )
        self.bmi_result = []
        for ix, row in enumerate(self.ht_wt_params):
            res = {}
            ht = row.get('HeightCm')
            wt = row.get('WeightKg')
            if not ht and wt:
                # Can use Logging here
                print('WARNING: Input data row {} contains'
                    ' blank or invalid height/weight values'
                    'height: {} | weight : {}'.format(ix, ht, wt)
                )
                continue
            
            bmi_value = self._calculate_bmi(
                ht, wt,
                height_unit=self.height_unit,
                weight_unit=self.weight_unit
            )
            bmi_cat_and_health_risk_label = self._get_bmi_cat_and_health_risk(bmi_value)
            res['Bmi'] = bmi_value
            res['BmiCategory'] = bmi_cat_and_health_risk_label.get('category')
            res['HealthRisk'] = bmi_cat_and_health_risk_label.get('health_risk')            
            res.update(row)
            self.bmi_result.append(res)
        return self.bmi_result

    def _get_category_count(self, bmi_result):
        cat_count = {}
        
        for res in bmi_result:
            cnt = cat_count.setdefault(res.get('BmiCategory'), 0)
            cnt = cnt + 1
            cat_count[res.get('BmiCategory')] = cnt
        return cat_count

    def display_category_count(self):
        cat_count = self._get_category_count(self.bmi_result)
        for k, v in cat_count.items():
            print('Number of {} people = {}'.format(k, v))

    def load_data_with_pandas(self, json_data=INPUT_FIXTURE):
        self.ht_wt_params = pd.read_json(json_data)
        return self.ht_wt_params

    def get_bmi_result_with_pandas(self):
        if self.ht_wt_params is None:
            raise ValueError(
                'No input data available. Use `load_data_with_pandas` method to add'
                ' height, weight, input data'
            )
        self.bmi_result = self.ht_wt_params.copy(deep=True)

        # Calc and create a Bmi column in the Dataframe
        self.bmi_result['Bmi'] = self.bmi_result.apply(
            lambda row: self._calculate_bmi(
                row['HeightCm'],
                row['WeightKg'],
                height_unit=self.height_unit,
                weight_unit=self.weight_unit,
            ),
            axis=1,
        )

        # Find and add `BmiCategory` and `HealthRisk` to new columns in Dataframe
        self.bmi_result[['BmiCategory', 'HealthRisk']] = self.bmi_result.apply(
            lambda row: self._get_multiple_key_vals(
                self._get_bmi_cat_and_health_risk(
                    row['Bmi'],
                ),
                keys=['category', 'health_risk']
            ),
            result_type='expand',
            axis=1,
        )
        return self.bmi_result

    def display_category_count_with_pandas(self):
        return self.bmi_result.groupby('BmiCategory')['BmiCategory'].count()

    def _get_multiple_key_vals(self, x, keys):
        return [x.get(k) for k in keys]

    def _convert_cm_to_m(self, value):
        return (value / 100)

    def _convert_g_to_kg(self, value):
        return (value / 1000)
