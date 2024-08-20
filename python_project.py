import datetime
import re
import numpy as np

def parse_iostat_log(file_path, start_time, end_time, device_name):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Convert start and end times to datetime objects
    start_time = datetime.datetime.strptime(start_time, '%d/%m/%Y %I:%M:%S %p')
    end_time = datetime.datetime.strptime(end_time, '%d/%m/%Y %I:%M:%S %p')

    rtt_values = []
    current_time = None

    for line in lines:
        line = line.strip()
        
        # Match the timestamp in the iostat
        time_match = re.match(r'(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}:\d{2} [APM]{2})', line)
        if time_match:
            date_part = time_match.group(1)
            time_part = time_match.group(2)
            current_time = datetime.datetime.strptime(f'{date_part} {time_part}', '%d/%m/%Y %I:%M:%S %p')
            print(f"Current time found: {current_time}")  # Debug: print the current timestamp found
            continue
        
        if current_time and start_time <= current_time <= end_time:
            if device_name in line:
                data = line.split(',')
                print(f"Line matching device '{device_name}': {line}")  # Debug: print matching line
                print(f"Parsed data: {data}")  # Debug: print the split line data
                await_time = float(data[4].strip())  # Assuming 'await' is the 5th column (index 4)
                rtt_values.append(await_time)
    
    print(f"RTT values collected: {rtt_values}")  # Debug: print all collected RTT values

    if not rtt_values:
        raise ValueError(f"No data found for device {device_name} in the given time range.")

    # Calculate average, 99th, and 95th percentiles
    avg_rtt = np.mean(rtt_values)
    rtt_99th = np.percentile(rtt_values, 99)
    rtt_95th = np.percentile(rtt_values, 95)

    return avg_rtt, rtt_99th, rtt_95th

def main():
    file_path = 'C:/Users/rushi_khc/OneDrive/Desktop/test.csv'
    start_time = '08/05/2024 02:32:00 PM'
    end_time = '08/05/2024 02:33:59 PM'
    device_name = 'sda'  # Example device name

    avg_rtt, rtt_99th, rtt_95th = parse_iostat_log(file_path, start_time, end_time, device_name)

    print(f"Device: {device_name}")
    print(f"Average RTT: {avg_rtt:.2f} ms")
    print(f"99th Percentile RTT: {rtt_99th:.2f} ms")
    print(f"95th Percentile RTT: {rtt_95th:.2f} ms")

if __name__ == "__main__":
    main()
