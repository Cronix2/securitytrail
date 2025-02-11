<p align="center">
    <img src="https://cdn-icons-png.flaticon.com/512/6295/6295417.png" align="center" width="30%">
</p>

<p align="center">
    <h1 align="center">SECURITYTRAIL.GIT</h1>
</p>

<p align="center">
    <em><code>❯ Subdomain enumeration and monitoring tool</code></em>
</p>

<p align="center">
    <img src="https://img.shields.io/github/license/Cronix2/securitytrail.git?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
    <img src="https://img.shields.io/github/last-commit/Cronix2/securitytrail.git?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
    <img src="https://img.shields.io/github/languages/top/Cronix2/securitytrail.git?style=default&color=0080ff" alt="repo-top-language">
    <img src="https://img.shields.io/github/languages/count/Cronix2/securitytrail.git?style=default&color=0080ff" alt="repo-language-count">
</p>

---

## 🔗 Table of Contents

- [� Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [👾 Features](#-features)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [☑️ Prerequisites](#️-prerequisites)
  - [⚙️ Installation](#️-installation)
  - [🤖 Usage](#-usage)
- [🧪 Future Testing](#-future-testing)
- [📌 Project Roadmap](#-project-roadmap)
- [🔰 Contributing](#-contributing)
- [🎗 License](#-license)
  - [🔹 Key Improvements in this README:](#-key-improvements-in-this-readme)

---

## 📍 Overview

**Subdomain Discover** is a project designed for **subdomain enumeration and monitoring**. It automates the discovery of subdomains for **defensive security** purposes, such as **attack surface monitoring**.  

This tool allows users to:  
- Identify active subdomains of a target  
- Detect misconfigurations  
- Monitor the evolution of an organization’s subdomains  

The project includes a **Flask-based web interface** for result visualization, fully containerized using **Docker**.

---

## 👾 Features

- ✅ **Automation**: Automatically detects subdomains  
- 🔍 **DNS Exploration**: Uses DNS queries to retrieve subdomains  
- 🔌 **Extensibility**: Potential for integrating external sources (APIs, OSINT)  
- 📂 **Results Export**: Structured formats (CSV, JSON, or database)  
- 🌐 **Web Visualization**: Flask-based interface deployed with **Docker**  

---

## 📁 Project Structure

```sh
└── securitytrail.git/
    ├── LICENSE
    ├── Subdomains
    │   └── subdomain_list.txt
    ├── docker-compose.yml
    ├── init.sql
    └── python-scripts
        ├── Dockerfile
        ├── ip_generator.py
        ├── main.py
        ├── requirements.txt
        ├── static
        ├── subdomain_discover.py
        ├── supervision_site.py
        └── templates
```

---

## 🚀 Getting Started

### ☑️ Prerequisites

Before running `securitytrail.git`, ensure you have:  
- **Docker** installed on your machine  
- **Docker Compose** for easy deployment  

### ⚙️ Installation

**Clone the repository:**  
```sh
❯ git clone https://github.com/Cronix2/securitytrail.git
```

**Navigate to the project directory:**  
```sh
❯ cd securitytrail.git
```

### 🤖 Usage

**Run the project using Docker Compose:**  
```sh
❯ docker-compose up -d
```

This will automatically deploy all necessary services, including the **Flask API** and subdomain enumeration tools.  

To stop the containers:  
```sh
❯ docker-compose down
```

---

## 🧪 Future Testing

🚧 **Tests are not yet implemented** 🚧  
A future test suite may be added to improve the stability and reliability of the project.

---

## 📌 Project Roadmap

The project is continuously evolving based on user needs.  
Potential future improvements include:  
- Integration of external APIs for better subdomain detection  
- Enhancements to the web interface  
- Improved logging and history tracking  

---

## 🔰 Contributing

Contributions are welcome! To contribute:  

1. **Fork the repository**  
2. **Clone your fork:**  
   ```sh
   git clone https://github.com/your-username/securitytrail.git
   ```
3. **Create a new branch for your changes:**  
   ```sh
   git checkout -b new-feature
   ```
4. **Make your changes and commit them:**  
   ```sh
   git commit -m "Added [your feature]"
   ```
5. **Push your branch to your fork:**  
   ```sh
   git push origin new-feature
   ```
6. **Create a Pull Request** to the original repository  

---

## 🎗 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  
For more details, see the [LICENSE](https://github.com/Cronix2/securitytrail.git/blob/main/LICENSE) file.

---

🚀 **Thank you for using SecurityTrail.git!**  
```

---

### 🔹 Key Improvements in this README:
✔ **Fully translated into English**  
✔ **Maintains the structured, professional format you requested**  
✔ **Clear installation and usage instructions focused on Docker**  
✔ **Future testing and roadmap sections included**  

If you need any further refinements, let me know! 🚀🔥