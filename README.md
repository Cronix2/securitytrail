<p align="center">
    <img src="https://media.discordapp.net/attachments/1036960627127762944/1338872869886885919/DALL_E-2025-02-11-14.59__1_-removebg-preview.png?ex=67acaa07&is=67ab5887&hm=c09b811527429af6f109febf904b602e52d3f64040e80f22c61617d61d3c3ac2&=&format=webp&quality=lossless&width=570&height=570" align="center" width="30%">
</p>

<p align="center">
    <h1 align="center">SECURITYTRAIL.GIT</h1>
</p>

<p align="center">
    <em><code>❯ Subdomain enumeration and monitoring tool</code></em>
</p>

<p align="center">
    <img src="https://img.shields.io/github/license/Cronix2/securitytrail?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="License">
    <img src="https://img.shields.io/github/last-commit/Cronix2/securitytrail?style=for-the-badge&logo=git&logoColor=white&color=0080ff" alt="Last Commit">
    <img src="https://img.shields.io/github/languages/top/Cronix2/securitytrail?style=for-the-badge&color=0080ff" alt="Top Language">
    <img src="https://img.shields.io/github/languages/count/Cronix2/securitytrail?style=for-the-badge&color=0080ff" alt="Languages Count">
</p>

<p align="center">
		<em>Developed with the software and tools below.</em>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Docker-2CA5E0.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
    <img src="https://img.shields.io/badge/MariaDB-336791.svg?style=flat&logo=MariaDB&logoColor=white" alt="MariaDB">
</p>

---

## 🔗 Table of Contents

- [🔗 Table of Contents](#-table-of-contents)
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

The project is continuously evolving based on user needs.Potential future improvements include:

- Integration of external APIs for better subdomain detection
- Enhancements to the web interface
- Improved logging and history tracking

---

## 🔰 Contributing

Contributions are welcome! To contribute:

1. **Fork the repository**
2. **Clone your fork:**
   ```sh
   git clone https://github.com/Cronix2/securitytrail.git
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
