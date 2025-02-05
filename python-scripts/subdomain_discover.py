import requests
import tqdm


# Function which take the domain and return the subdomains
def subdomain_brutforce_dictionnary(domain):
    with open("../Subdomains/subdomain_list.txt", "r", encoding="utf-8") as file:
        subdomains = file.readlines()
    with tqdm.tqdm(total=len(subdomains), desc="Bruteforcing subdomains") as pbar:
        for i in range(len(subdomains)):
            url_subdomain = f"http://{subdomains[i].strip()}.{domain}"
            try:
                response = requests.get(url_subdomain)
                if response.status_code == 200:
                    # print(f"subdomain found: {subdomains[i].strip()}.{domain}")
                    with open("results/subdomains.txt", "a", encoding="utf-8") as file:
                        file.write(f"{subdomains[i].strip()}.{domain}\n")
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.MissingSchema:
                pass
            except requests.exceptions.InvalidURL:
                pass
            except requests.exceptions.InvalidSchema:
                pass
            except requests.exceptions.InvalidHeader:
                pass
            pbar.update(1)
    return True
