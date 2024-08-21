import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# Function to parse the input data
def parse_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    data = []
    timestamp = None
    
    for line in lines:
        line = line.strip()
        if line:
            if line.startswith('202'):
                timestamp = dt.datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
            else:
                pod_name, cpu_usage, memory_usage = line.split()
                cpu_usage = float(cpu_usage.rstrip('m')) / 1000  # Convert to cores
                memory_usage = float(memory_usage.rstrip('Mi')) / 1024  # Convert to Gi
                data.append([timestamp, pod_name, cpu_usage, memory_usage])
    
    return pd.DataFrame(data, columns=['timestamp', 'pod_name', 'cpu_usage', 'memory_usage'])

# Function to filter data within the time range
def filter_data(df, start_time, end_time):
    return df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

# Function to plot the graphs
def plot_usage(df, component, start_time, end_time):
    # Filter the data for the specific component
    component_data = df[df['pod_name'].str.contains(component)]
    
    plt.figure(figsize=(14, 10))
    
    for node in ['master-n1', 'master-n2', 'master-n3']:
        node_data = component_data[component_data['pod_name'].str.contains(node)]
        plt.plot(node_data['timestamp'], node_data['cpu_usage'], label=f'{component} {node} - CPU (cores)')
        plt.plot(node_data['timestamp'], node_data['memory_usage'], label=f'{component} {node} - Memory (Gi)')
    
    plt.title(f'{component} Resource Usage from {start_time} to {end_time}')
    plt.xlabel('Time')
    plt.ylabel('Usage')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function to run the analysis
def main(file_path, start_time, end_time):
    df = parse_data(file_path)
    filtered_df = filter_data(df, start_time, end_time)
    
    for component in ['etcd-control-plane', 'kube-apiserver', 'kube-controller-manager', 'kube-scheduler']:
        plot_usage(filtered_df, component, start_time, end_time)

# Example usage
file_path = 'path_to_your_file.txt'
start_time = dt.datetime(2024, 8, 12, 21, 9, 47)
end_time = dt.datetime(2024, 8, 12, 21, 9, 58)

main(file_path, start_time, end_time)
