import pickle
import matplotlib.pyplot as plt
import numpy as np

def load_electric_fields(i):
    
    with open(r"C:\\Users\\dilip\\OneDrive\\Desktop\\MTP\\artifacts\\char_E\\char_electric_field_{}.pkl".format(i), 'rb') as file1:
        
        E_t_c = pickle.load(file1)
    with open(r"C:\\Users\\dilip\\OneDrive\\Desktop\\MTP\\artifacts\\ref_E\\ref_electric_field_{}.pkl".format(i), 'rb') as file2:
        E_t_r = pickle.load(file2)
    return E_t_c, E_t_r

def load_time_values():
    

    with open(r'C:\Users\dilip\OneDrive\Desktop\MTP\artifacts\time_values.pkl', 'rb') as file3:
        time_values = pickle.load(file3)
    return time_values



def calculate_cross_correlation_intensities(tau_values, E_t_c, E_t_r, time_values):
    
   
    cross_correlation_intensities = np.zeros(len(tau_values))
    for j in range(len(tau_values)):
        tau = tau_values[j]
        shifted_electric_field = np.roll(E_t_c, int(-tau / (time_values[1] - time_values[0])))
        intensity = np.trapz((np.real(E_t_r) + np.real(shifted_electric_field))**4, time_values)
        cross_correlation_intensities[j] = intensity
    return cross_correlation_intensities


def normalize_intensities(intensities):
  
    normalized_intensities = np.divide(intensities, np.max(np.abs(intensities)))
    return normalized_intensities

def save_normalized_intensities(normalized_intensities, filename):

    with open(filename, 'wb') as file:
        pickle.dump(normalized_intensities, file)

def main():

    for i in range(1, 1001):
        E_t_c, E_t_r = load_electric_fields(i)
        time_values = load_time_values()
        tau_values = np.linspace(-75, 75, 1600) * 10**-14
        cross_correlation_intensities = calculate_cross_correlation_intensities(tau_values, E_t_c, E_t_r, time_values)
        normalized_intensities = normalize_intensities(cross_correlation_intensities)
        filename = f"C:\\Users\\dilip\\OneDrive\\Desktop\\MTP\\artifacts\\cross-correlation_WG\\cross-correlation_WG{i}.pkl"
        save_normalized_intensities(normalized_intensities, filename)

if __name__ == "__main__":
    main()