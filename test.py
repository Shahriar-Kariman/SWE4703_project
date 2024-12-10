# Given parameters
SOC_initial = 40  # Initial state of charge in kWh
beta = 250  # Number of cycles per year
kappa = 4.6/1000  # Degradation per cycle in kWh
vartheta = 0.5/100  # Annual capacity degradation (2%)
t = 10  # Time in years
# Calculate maximum state of charge after t years
SOC_max = SOC_initial - (beta * kappa + vartheta) * t
print(f"Maximum state of charge after {t} years: {SOC_max:.2f} kWh")