import tqdm
import time
import os


# Function to determine the last generated IP and remove incomplete entries
def get_last_generated_ip(filename):
    if not os.path.exists(filename):
        print("There is no an existing file")
        return "0.0.0.0"  # Start from the beginning if the file does not exist

    with open(filename, "rb") as file:
        file.seek(0, os.SEEK_END)  # Move to the end of the file
        position = file.tell()
        print(position)
        while position > 0:
            position -= 1
            file.seek(position)
            if file.read(1) == b"\n":
                break

        file.seek(position)
        last_line = file.readline().decode("utf-8").strip()

    return last_line if last_line else "0.0.0.0"


# Function to generate all possible IP addresses
# Writes to a file every 50,000,000 IPs to avoid excessive RAM usage
def ip_generator():
    total_ips = 256 * 256 * 256 * 256
    batch_size = 50_000_000  # Batch size for writing to file
    ip_list = []

    last_ip = get_last_generated_ip("ip_list.txt")
    start_values = list(map(int, last_ip.split(".")))

    with open("ip_list.txt", "a", encoding="utf-8") as file:
        with tqdm.tqdm(total=total_ips, desc="Generating IPs") as pbar:
            for i in range(start_values[0], 256):
                for j in range(start_values[1] if i == start_values[0] else 0, 256):
                    for k in range(start_values[2] if j == start_values[1] else 0, 256):
                        for m in range(start_values[3] if k == start_values[2] else 0, 256):
                            ip = f"{i}.{j}.{k}.{m}"
                            ip_list.append(ip)
                            if len(ip_list) >= batch_size:
                                file.writelines(f"{ip}\n" for ip in ip_list)
                                ip_list.clear()  # Clear list to free memory
                            pbar.update(1)  # Update progress bar

        if ip_list:  # Write remaining IPs
            file.writelines(f"{ip}\n" for ip in ip_list)
            ip_list.clear()


# Function to filter out private IP addresses from the generated file
# Processes the file line by line to avoid RAM issues
def delete_private_ip():
    print("Filtering private IPs...")
    start_time = time.time()
    private_prefixes = ("192.168.", "172.16.", "10.", "127.")

    with open("ip_list.txt", "r", encoding="utf-8") as infile, open("filtered_ip_list.txt", "w",
                                                                    encoding="utf-8") as outfile:
        with tqdm.tqdm(total=256 * 256 * 256 * 256, desc="Filtering IPs") as pbar:
            for line in infile:
                if not line.startswith(private_prefixes):
                    outfile.write(line)
                pbar.update(1)

    print(f"Private IP filtering completed in {time.time() - start_time:.2f} seconds.")


# Main function to generate and filter the IP list
def generate_ip_list():
    print("Starting IP generation...")
    start_time = time.time()
    #ip_generator()
    print(f"IP generation completed in {time.time() - start_time:.2f} seconds.")

    delete_private_ip()
    print("Process completed successfully.")


generate_ip_list()
