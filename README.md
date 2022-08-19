# BMI Calculator

This module calculates the Body Mass Index for a given input containing height and weight data. It also aggregates the data and displays the count of rows belonging to different categories based on their BMI.

### Task Objectives

1. Calculate the BMI for given data (More instructions given below)
2. Count the number of overweight people

	Based on the input data provided in the task, here is the categorical breakup:

	Number of Moderately obese people = 3
	Number of Normal weight people = 2
	Number of Overweight people = 1

	The total number of exactly "Overweight" people is 1
	The total number of "Overweight" or higher BMI is 4 (Overweight + Moderately obese)

### How To

You can use the library as follows:

1. Clone this repository

```
git clone 
```

2. Switch to the directory containing the `bmicalc.py` file

```
cd ~/bmi_calculator
```

3. Install requirements (this will install `pandas`) if you would prefer to use this module with pandas as the data processing engine (Recommended for very large input datasets) - it is not a mandatory dependency.

```
pip install pandas
```

4. In the Python / IPython shell, run the following;

```
from bmicalc import BMICalculator
bmi = BMICalculator()
```

#### Without Pandas

5a. Load the input data. Use the `json_data` argument to provide a json string as input or a json file as input. The module uses the default data available in the `input_fixture.json` file as input if no argument is provided.

```
bmi.load_data() # To load the default data

# bmi.load_data(json_data='{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 }') # To load user provided custom json string

# bmi.load_data(json_data='/path/to/myfile.json') # To load data from user provided json file
```

6a. Calculate the BMI and generate the BMI data

```
bmi.get_bmi_result()
```

7a. Calculate aggregation of number of rows in each category by running;

```
bmi.display_category_count()
```

#### With Pandas

When loading and working with large datasets, using the pandas backend is a better idea for performance.

5b. Load the input data.

```
bmi.load_data_with_pandas() # To load the default data

# bmi.load_data_with_pandas(json_data='{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 }') # To load user provided custom json string

# bmi.load_data_with_pandas(json_data='/path/to/myfile.json') # To load data from user provided json file
```

6b. Calculate the BMI and generate the BMI data

```
bmi.get_bmi_result_with_pandas()
```

7a. Calculate aggregation of number of rows in each category by running;

```
bmi.display_category_count_with_pandas()
```

Note that here the data is in the form of a pandas Dataframe.

### Tests

The tests have been written using the `unittest` module. They are located in the `tests.py` file. You can run the tests using;

```
python -m unittest discover
```

### Footnotes and Possible Improvements
* We can always add more tests and cover more corner cases, like floating point corner cases
* We can add Travis CI/Github Actions or other CI-CD to automatically run tests
* We can add code coverage stats to check and make sure that the tests cover maximum code
* We have not truncated the floating number results to retain data.
* This module can be enhanced by building CLI clients with argparse module or even web app API using Flask
* The pandas workflow can be integrated into the mainstream workflow instead of the current implementation of using completely different methods (current design was executed due to time constraints)
