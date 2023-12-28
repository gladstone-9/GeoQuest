# GeoQuest: A Google Maps Scavenger Hunt

Welcome to __GeoQuest__, the Google Maps Scavenger Hunt project designed for a thrilling adventure at the University of Virginia! This repository contains all of the resources and code necessary to create an exciting and interactive scavenger hunt using the power of the Google Maps API. Whether you're planning an engaging activity for students, a team-building experience for colleagues, or just a fun adventure with friends, GeoQuest offers a flexible framework to get you started.

### Features
* __Customizable Scavenger Hunts:__ Easily create your scavenger hunt by defining locations, clues, and challenges using the Google Maps API.

* __Leaderboard System:__ Rank participants based upon various criteria.

* __Interactive Map:__ Display an engaging map to guide participants and showcase important hunt-related information.

* __User-friendly Interface:__ A straightforward web interface for participants to interact with during the scavenger hunt.


### Getting Started

Setting up a Virtual Environment: 
1. __Install the Virtual Environment Package__: If the ```venv``` module isn't imported for your current environment enter ```python -m pip install --user virtualenv``` into the terminal

2. __Creating the Virtual Environment:__ To create the environment enter ```python -m venv env``` into the console where ```env``` will be the name of the virtual environment.

3. __Activate the Environment:__ Add the environment's executable to the shell path by typing ```.\env\Scripts\activate``` for Windows or ```source env/bin/activate``` for macOS/Linux

4. __Install Required Packages__: If the environment doesn't currently have all the modules that this project uses imported, they can be added with ```python -m pip install -r requirements.txt```

5. __Verify Django Installation__: Check that Django has been installed into the virtual environment with ```python -m django --version```

6. __Deactivating the environment:__ When you want to exit the virtual environment simply type ```deactivate```


<br>


To set up and run your scavenger hunt using GeoQuest, follow these simple steps:

1. __Clone the Repository:__ Clone this repository to your local machine by entering ```git clone https://github.com/gladstone-9/GeoQuest.git``` into a terminal

2. __Configuration:__ Configure your Google Maps API credentials and other settings in the project files.

3. __Customize Your Hunt:__ Define the University of Virginia locations, clues, and challenges for your scavenger hunt.

4. __Run the Application:__ From the root directory, enter ```python manage.py runserver``` into the terminal to start the application. Then use the webapp to invite participants to embark on their GeoQuest adventure at UVA!


<br>


> **_NOTE:_**  Anytime a command starting with ```python``` is run in the above steps, it's assumed to be on a Windows machine. If using Linux or macOS, replace the ```python``` command with ```python3``` (e.g. ```python3 -m pip install Django```). 

<br>


### The Team

| Name              | Computing Id | Role                 |
| --------          | -------      | -------              |
| Gabe Silverstein  | jgb9fz       | Scrum Master         |
| Janice Guo        | vdq8tp       | DevOps Manager       |
| Gabriel Gladstone | zwy7ce       | Testing Manager      |
| Brian Xiao        | qhu2fg       | Requirements Manager |
| Shruthi Kalathur  | wxs2qx       | UX Designer          |

Current superusers include ```geoQuest-admin``` (password: admin-password123) and ```cs3240.super@gmail.com``` (password: geoQuest_admin).
Current users include ```cs3240.student@gmail.com``` (password: geoQuest_student).
<br>
Use the Account->Login page instead of logging in with google. 

<br>
Prepare for an unforgettable adventure at the University of Virginia with GeoQuest! 🏛️🌍🔍
<br>
We encourage users new to the site to check out the UVA Trivia Quest!

## 

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/xHnRfY9D)
