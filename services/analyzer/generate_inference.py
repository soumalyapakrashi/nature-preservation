import pandas as pd
import matplotlib.pyplot as plt

def infer(input_data: dict):
    df = pd.DataFrame.from_dict(input_data)
    df.sort_values("ds", inplace = True, ignore_index = True)
    
    plt.plot(df["ds"], df["y"])
    plt.show()