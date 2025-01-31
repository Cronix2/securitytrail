import tqdm
import time


# Function to generate all possible IP addresses
# Writes to a file every 50,000,000 IPs to avoid excessive RAM usage
def ip_generator():
    total_ips = 256 * 256 * 256 * 256
    batch_size = 50_000_000  # Batch size for writing to file
    ip_list = []
    with open("ip_list.txt", "w", encoding="utf-8") as file:
        with tqdm.tqdm(total=total_ips, desc="Generating IPs") as pbar:
            for i in range(256):
                for j in range(256):
                    for k in range(256):
                        for m in range(256):
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
# Writes the filtered IPs to a new file
def delete_private_ip():
    print("Filtering private IPs...")
    start_time = time.time()
    private_prefixes = ("192.168.", "172.16.", "10.", "127.")

    with open("ip_list.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open("filtered_ip_list.txt", "w", encoding="utf-8") as file:
        with tqdm.tqdm(total=len(lines), desc="Filtering private IPs") as pbar:
            for line in lines:
                if not line.startswith(private_prefixes):
                    file.write(line)
                pbar.update(1)

    print(f"Private IP filtering completed in {time.time() - start_time:.2f} seconds.")


# Main function to generate and filter the IP list
def generate_ip_list():
    print("Starting IP generation...")
    start_time = time.time()
    ip_generator()
    print(f"IP generation completed in {time.time() - start_time:.2f} seconds.")

    delete_private_ip()
    print("Process completed successfully.")


generate_ip_list()
