import pandas as pd

def wavelength_xlsx_to_array(file): 
    try:
        df = pd.read_excel(file, index_col=0)
    except Exception as e:
        raise ValueError(f'No excel filepassed passed: {e}')
    
    columns = generate_float_range_arr(357.0, 725.5, 0.5)

    df_transposed = df.transpose()
    df_cut = df_transposed[columns]
    data = df_cut.values

    # returning 1D array
    return data.ravel()

def generate_float_range_arr(min, max, step):
    i = min
    arr = []

    while i <= max:
        arr.append(i)
        i += step
    return arr
