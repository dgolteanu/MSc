import numpy as np
import os

def calculate_sparsity(array):
    """Calculate the sparsity of a NumPy array."""
    total_elements = array.size
    zero_elements = total_elements - np.count_nonzero(array)
    sparsity = zero_elements / total_elements
    return sparsity

def process_npy_files(folder_path):
    """Process all .npy files in the specified folder and calculate sparsity statistics."""
    sparsities = []

    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.startswith('cgr'):
            file_path = os.path.join(folder_path, file_name)
            array = np.load(file_path)
            sparsity = calculate_sparsity(array)
            sparsities.append(sparsity)

    # Calculate mean and standard deviation of sparsities
    mean_sparsity = np.mean(sparsities)
    std_sparsity = np.std(sparsities)

    return sparsities, mean_sparsity, std_sparsity

def main():
    folder_path = input("Enter the path to the folder containing .npy files: ").strip()
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    sparsities, mean_sparsity, std_sparsity = process_npy_files(folder_path)

    print(f"Sparsities: {sparsities}")
    print(f"Mean Sparsity: {mean_sparsity:.2%}")
    print(f"Standard Deviation of Sparsity: {std_sparsity:.2%}")

if __name__ == "__main__":
    main()
