import pickle
import matplotlib.pyplot as plt
import numpy as np

def load_data(file_path):
  
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def reshape_data(data, shape):
    
   
    return data.reshape(shape)

def stack_data(matrices, axis):
    
  
    return np.stack(matrices, axis=axis)

def transpose_data(data, axes):
  
    return np.transpose(data, axes)

def save_data(data, filename):
  
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def process_and_save_data(i):
  
    charspec = load_data(f'C:\\Users\\dilip\\OneDrive\\Desktop\\MTP\\artifacts\\char_spec\\char_spec{i}.pkl')
    refspec = load_data(f'C:\\Users\\dilip\\OneDrive\\Desktop\\MTP\\artifacts\\ref_spec\\ref_spec{i}.pkl')
    IXG = load_data(f'C:\\Users\\dilip\\OneDrive\\Desktop\\MTP\\artifacts\\cross-correlation_G\\cross-correlation_Glass{i}.pkl')
    IXWG = load_data(f'C:\\Users\\dilip\\OneDrive\\Desktop\\MTP\\artifacts\\cross-correlation_WG\\cross-correlation_WG{i}.pkl')

    matrix3 = reshape_data(charspec, (40, 40))
    matrix1 = reshape_data(refspec, (40, 40))
    matrix4 = reshape_data(IXG, (40, 40))
    matrix2 = reshape_data(IXWG, (40, 40))

    stacked_data = stack_data((matrix1, matrix2, matrix3, matrix4), axis=-1)
    stacked_data = transpose_data(stacked_data, (1, 0, 2))

    save_data(stacked_data, f"C:\\Users\\dilip\\OneDrive\\Desktop\\MTP\\input\\input{i}.pkl")

def main():
  
    for i in range(1, 1001):
        process_and_save_data(i)

if __name__ == "__main__":
    
    main()