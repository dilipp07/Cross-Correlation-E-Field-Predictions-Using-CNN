import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve
import pickle
import os

def generate_spectrum(num_peaks=np.random.randint(10, 25), lambda_values=None):
    c = 3e8  # Speed of light in meters per second
    lambda_0 = np.random.uniform(600e-9, 900e-9)  # Central wavelength in meters
    gamma_0 = np.random.uniform(150e-9, 220e-9)  # Width parameter in meters

    if lambda_values is None:
        lambda_values = np.linspace(400e-9, 1200e-9, 4096)  # Wavelength values for the x-axis in meters

    spectrum = np.zeros_like(lambda_values)
    for _ in range(num_peaks):
        A = 0.1 + np.random.rand() * 0.9
        delta_lambda_0_i = (-gamma_0 / 4) + (np.random.rand() * gamma_0) / 2
        lambda_0_i = lambda_0 + delta_lambda_0_i
        gamma_lambda_i = (4 * np.random.rand() + 30) * 1e-9  # Width parameter in meters

        gaussian_function = A * np.exp((-(4 * np.log(2)) * (lambda_values - lambda_0_i)**2) / gamma_lambda_i**2)
        spectrum += gaussian_function
    spectrum = spectrum / np.max(spectrum)
    
    center_index = len(lambda_values) // 2
    crop_length = 1600 // 2
    spectrum = spectrum[center_index - crop_length:center_index + crop_length]

    # Rescale the wavelength values accordingly
    lambda_values = lambda_values[center_index - crop_length:center_index + crop_length]

    return spectrum,lambda_values

def generate_smoothed_phases(spectral_phases, random_width,l):
    sigma_nm = random_width 
    sigma_phase = 2 * 3.14 * random_width
    kernel_size = int(30 * sigma_phase)
    gaussian_kernel = np.exp(-0.5 * ((np.arange(-kernel_size, kernel_size + 1) /sigma_phase ) ** 2))
#     gaussian_kernel /= np.sum(gaussian_kernel)

    # Apply circular convolution to the spectral phases
    smoothed_phases = convolve(spectral_phases, gaussian_kernel, mode='same')

    # Remove linear components from smoothed phases
    linear_fit = np.polyfit(spectral_phases, smoothed_phases, 1)
    linear_components = np.polyval(linear_fit, spectral_phases)
    detrended_smoothed_phases = (smoothed_phases - linear_components)
    
    linear_fit = np.polyfit(l, smoothed_phases, 1)
    linear_components = np.polyval(linear_fit, l)
    detrended_smoothed_phases = (smoothed_phases - linear_components)

    return detrended_smoothed_phases


def construct_complex_fields(spectrum, detrended_smoothed_phases, omega):
    phase_multiplier = np.sqrt(spectrum)
    complex_fields = phase_multiplier * np.exp(1j * detrended_smoothed_phases)
    complex_fields=np.concatenate(((-complex_fields)[: :-1],complex_fields),axis=0)
    return complex_fields

def calculate_time_domain_electric_field(complex_fields, omega):
    time_values = np.fft.fftshift(np.fft.fftfreq(len(omega), d=(omega[1] - omega[0])))
    # Trim time_values symmetrically around zero
    time_values = time_values[len(time_values)//2 - 500 : len(time_values)//2 + 500]

    electric_field_time = np.fft.ifftshift(np.fft.ifft(np.fft.ifftshift(complex_fields)))
    # Trim electric_field_time symmetrically around zero
    electric_field_time = electric_field_time[len(electric_field_time)//2 - 500 : len(electric_field_time)//2 + 500]

    return electric_field_time, time_values



def save_array(array, filename, path="my_electric_fields"):
    full_path = os.path.join(path, filename)
    os.makedirs(path, exist_ok=True)

    with open(full_path, 'wb') as file:
        pickle.dump(array, file)

if __name__ == "__main__":
    desired_path = r"C:\Users\dilip\OneDrive\Desktop\MTP\artifacts\ref_E"
    desired_path1=r"C:\Users\dilip\OneDrive\Desktop\MTP\artifacts\ref_spec" # Specify the path where you want to save the files

    for i in range(1,1001):
        # Generate spectrum
        spectrum,l = generate_spectrum()

        # Generate smoothed phases
        spectral_phases = np.random.uniform(-np.pi, np.pi, len(spectrum))  # Generate random phases
        random_width = (3 + np.random.rand()* 52)   # Generate random width for smoothing
        detrended_smoothed_phases = generate_smoothed_phases(spectral_phases, random_width,l)

        # Construct complex fields
        omega = (3e8 / np.linspace(400e-9, 1200e-9, 4096))  # Calculate omega values
        complex_fields = construct_complex_fields(spectrum, detrended_smoothed_phases, omega)

        # Calculate time-domain electric field
        electric_field_time, time_values = calculate_time_domain_electric_field(complex_fields, omega)

        # Save the electric field array
        save_array(electric_field_time, f"ref_electric_field_{i}.pkl", path=desired_path)
        save_array(spectrum, f"ref_spec{i}.pkl", path=desired_path1)