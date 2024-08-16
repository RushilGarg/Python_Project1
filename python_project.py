import datetime
import re
import numpy as np

def parse_iostat_log(file_path, start_time, end_time, device_name):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    start_time = datetime.datetime.strptime(start_time, '%d/%m/%Y %I:%M:%S %p')
    end_time = datetime.datetime.strptime(end_time, '%d/%m/%Y %I:%M:%S %p')

    rtt_values = []
    current_time = None

    for line in lines:
        # Match the timestamp in the iostat log
        time_match = re.match(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [APM]{2})', line.strip())
        if time_match:
            current_time = datetime.datetime.strptime(time_match.group(1), '%d/%m/%Y %I:%M:%S %p')
            continue
        
        if current_time and start_time <= current_time <= end_time:
            if device_name in line:
                data = line.split()
                await_time = float(data[3])  # 'await' is the 4th column
                rtt_values.append(await_time)

    if not rtt_values:
        raise ValueError(f"No data found for device {device_name} in the given time range.")

    # Calculate average, 99th, and 95th percentiles
    avg_rtt = np.mean(rtt_values)
    rtt_99th = np.percentile(rtt_values, 99)
    rtt_95th = np.percentile(rtt_values, 95)

    return avg_rtt, rtt_99th, rtt_95th

def main():
    # Example inputs
    file_path = 'iostat.log'
    start_time = '08/05/2024 02:32:00 PM'
    end_time = '08/05/2024 02:33:59 PM'
    device_name = 'sda'

    avg_rtt, rtt_99th, rtt_95th = parse_iostat_log(file_path, start_time, end_time, device_name)

    print(f"Device: {device_name}")
    print(f"Average RTT: {avg_rtt:.2f} ms")
    print(f"99th Percentile RTT: {rtt_99th:.2f} ms")
    print(f"95th Percentile RTT: {rtt_95th:.2f} ms")

if __name__ == "__main__":
    main()
