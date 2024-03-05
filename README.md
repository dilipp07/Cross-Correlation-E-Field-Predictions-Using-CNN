# Data Simulation for Cross-correlation

# How to run?
### STEPS:

Clone the repository

```bash
https://github.com/dilipp07/Cross-Correlation-E-Field-Predictions-Using-CNN.git
```

Before running the following steps make sure to update this on the following code:

- change the specific file location where you want to store/load the data at the end of each of the .py file 

- change the number in the for loop for as many data as you want (default it was set in as 1001 for 1000 data)

### STEP 01 - Open reference.py for generating reference electric.

# Finally run the following command

```bash
python reference.py
```

### STEP 02 - Open characterised.py for generating pulse to be characterised.

```bash
python characterised.py
```

### STEP 03 - Open cross_correlation.py for generating cross correlation traces without passing through fused silica.

```bash
python cross_correlation.py
```

### STEP 04 - Open cross_correlation_withglass.py for generating cross correlation traces passing through fused silica.

```bash
python cross_correlation_withglass.py
```

### STEP 05 - Open input.py for generating input for the CNN .

```bash
python input.py
```

- Additionally, I have provided the code for generating an optimized model for CNN just play with the parameter for optimization and try to run the .ipynb file in a system having high power GPU
- For a generalised model generate data in 10e6 range and fit in the model.
