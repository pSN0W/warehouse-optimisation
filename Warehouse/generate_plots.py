import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./cost_data.csv')

def generate_plot(
    col,
    color,
    title
):
    curr = df.groupby(by = col).apply(lambda x:x["cost"].min())
    fig = plt.figure(figsize=(12,9))
    plt.plot(curr.index.values, curr.values, color=color, marker='x')
    plt.title(title)
    plt.xlabel(col)
    plt.ylabel("cost")
    plt.show()
    
generate_plot("lane_depth",'r',"Cost minimsation with lane depth")
generate_plot("rack_level",'g',"Cost minimsation with number of level in rack")
generate_plot("aspect_ratio",'b',"Cost minimsation with aspect ratio")
