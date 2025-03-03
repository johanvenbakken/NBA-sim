# **NBA-Sim technical documentation**
## **Table of contents**
1. [introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Architecture](#architecture)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

## **Introduction**
This is the technical documentation for NBA-sim, a project fully developed by Johan Venbakken. NBA-sim is a draft based simulation game based on the NBA. 

## **Project Overview**
NBA-sim is a project for those of you who are obbsessed with basketball, or just enjoy watching the game

## **Installation**
To install NBA-sim do the following
1. **Clone the repository**
```sh
git clone https://github.com/johanvenbakken/NBA-sim.git
```
2. **Navigate to the project directory**
```sh
cd NBA-sim
```

3. **Install flask**
```sh
pip install flask
```

4. **install mariadb**
```sh
brew install mariadb
brew services start mariadb
```

## **Usage**
To use NBA-sim follow these steps
1. **Set up the database**
Before starting the application, you need to import the database dump
```sh
mysql -u nba_admin -p NBA_sim < database/nba_sim_backup.sql
```

2. **start the application**
```sh
export FLASK_APP=backend.py  
flask run --port 3030
```
3. Open your browser and navigate to `http://localhost:3030`.

PS: (it is not possible right now to create a user, log in or use the leaderboard)
## **Architecture**
NBA-sim is built using the following technologies
- **Flask**: A lightweight web framework for building backend applications in Python. Flask is used in this project to handle server-side logic, routing, and template rendering.

- **MySQL**:  A popular relational database management system for storing and managing structured data. MySQL is used in this project to handle user data, authentication, and application-related information.

- **Markdown**: A lightweight markup language for formatting text using simple syntax. Markdown is used in this project for documentation, making it easy to write and structure README files and technical documents.

- **JavaScript, HTML, and CSS**: The core technologies for building web frontends. HTML structures the content, CSS styles the appearance, and JavaScript adds interactivity to create a dynamic user experience.

## **Contributing**
We do not welcome contributions yet, but if you have any ideas yo can contact me on [johanhven@gmail.com](mailto:johanhven@gmail.com)

## **License**
We are not yet licensed 
## **Contact**
You can contact us on [johanhven@gmail.com](mailto:johanhven@gmail.com)