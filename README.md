<p align="center">
  <img src="resources/logo.png"/>
</p>
<p align="center">
    <h1 align="center">AVIONICS-GROUND-STATION-APP</h1>
</p>
<!-- <p align="center">
    <em>HTTP error 401 for prompt `slogan`</em>
</p> -->
<p align="center">
	<!-- <img src="https://img.shields.io/github/license/mertkaplandar/avionics-ground-station-app?style=flat&color=0080ff" alt="license"> -->
	<img src="https://img.shields.io/github/last-commit/mertkaplandar/avionics-ground-station-app?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/mertkaplandar/avionics-ground-station-app?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/mertkaplandar/avionics-ground-station-app?style=flat&color=0080ff" alt="repo-language-count">
<p>
<!-- <p align="center">
		<em>Developed with the software and tools below.</em>
</p> -->
<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Qt-000000.svg?style=flat&logo=Qt" alt="Qt">
	<img src="https://img.shields.io/badge/Folium-77B829.svg?style=flat&logo=Folium&logoColor=white" alt="Folium">
	<img src="https://img.shields.io/badge/JSON-000000.svg?style=flat&logo=JSON&logoColor=white" alt="JSON">
</p>
<hr>

## 🔗 Quick Links

> - [📍 Overview](#-overview)
> - [📦 Features](#-features)
> - [📂 Repository Structure](#-repository-structure)
> - [🧩 Modules](#-modules)
> - [🚀 Getting Started](#-getting-started)
>   - [⚙️ Installation](#️-installation)
>   - [🤖 Running avionics-ground-station-app](#-running-avionics-ground-station-app)
> - [🛠 Project Roadmap](#-project-roadmap)
> - [👏 Acknowledgments](#-acknowledgments)
<!-- > - [🤝 Contributing](#-contributing) -->
<!-- > - [📄 License](#-license) -->


---

## 📍 Overview

This application is designed to display data from an avionics system. The main reason for its design is to display data from the avionics system of the Atmaca Rocket Team's RFAL1 rocket participating in the 2024 Teknofest Rocket Competition and also to transmit the incoming data to the referee ground station.

A sample ground station system with the necessary explanations for the program to work is included in the link [here](https://github.com/mertkaplandar/rocket-ground-station-hardware).

---

## 📦 Features

- Provides connection to the ground station system by selecting COM port and baund rate
- Displays data from the ground station with text boxes
- Visualizes latitude and longitude data from the ground station on the map
- Displays the serial port of the ground station system
- Transmits data received from the avionics system to the referee ground station in accordance with the structure in the Teknofest 2024 Rocket Competition Specification
- Provides dark and light theme options
- Saves received data in json format with instant time and date data.

---

## 📂 Repository Structure

```sh
└── avionics-ground-station-app/
    ├── README.md
    ├── config.json
    ├── ground-station-app.py
    ├── hyi_controller.py
    ├── requirements.txt
    ├── resources
    │   ├── entry.html
    │   ├── icon.ico
    │   ├── icon.png
    │   ├── logo.png
    │   └── rocket.png
    └── styles
        ├── style-dark.qss
        └── style-white.qss
```

## 🚀 Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `3.12`

### ⚙️ Installation

1. Clone the avionics-ground-station-app repository:

```sh
git clone https://github.com/mertkaplandar/avionics-ground-station-app
```

2. Change to the project directory:

```sh
cd avionics-ground-station-app
```

3. Create venv:

```sh
python -m venv env
```

4. Activate the venv:

```sh
env/Scripts/activate
```

5. Install the dependencies:

```sh
pip install -r requirements.txt
```

### 🤖 Running avionics-ground-station-app

Use the following command to run avionics-ground-station-app:

```sh
python main.py
```

<!-- ### 🧪 Tests

To execute tests, run:

```sh
pytest
```

--- -->

## 🛠 Project Roadmap

- [ ] `► `

<!-- --- 

 ## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/mertkaplandar/avionics-ground-station-app/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/mertkaplandar/avionics-ground-station-app/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/mertkaplandar/avionics-ground-station-app/issues)**: Submit bugs found or log feature requests for Avionics-ground-station-app.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/mertkaplandar/avionics-ground-station-app
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

--- -->

<!-- ## 📄 License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.
, -->


