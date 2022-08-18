import json

import pandas as pd

from literals import INPUT_FIXTURE, BMI_CATEGORY_HEALTH_RISK_MAP


class BMICalculator():
    bmi_category_health_risk_map = BMI_CATEGORY_HEALTH_RISK_MAP
    height_unit = 'cm' # Can be `m` or `cm`
    weight_unit = 'kg' # Can be `g` or `kg`

    def load_data(self, json_data=INPUT_FIXTURE):
        self.ht_wt_params = json.loads(json_data)
        return self.ht_wt_params

    def _calculate_bmi(self, height, weight, height_unit, weight_unit):
        if height_unit not in ['cm', 'm']:
            raise ValueError("height_unit parameter must be 'cm' or 'm'")
        if weight_unit not in ['g', 'kg']:
            raise ValueError("weight_unit parameter must be 'g' or 'kg'")

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

        # Check if bmi_result param is a Dataframe obj or a list obj
        if isinstance(bmi_result, pd.DataFrame):
            iter_rows = bmi_result.iterrows()
        elif isinstance(bmi_result, list):
            iter_rows = enumerate(bmi_result)
        
        for ix, res in iter_rows:
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

    def get_bmi_result_with_pandas():
        if not self.ht_wt_params:
            raise ValueError(
                'No input data available. Use `load_data` method to add'
                ' height, weight, input data'
            )

    def _convert_cm_to_m(self, value):
        return (value / 100)

    def _convert_g_to_kg(self, value):
        return (value / 1000)
