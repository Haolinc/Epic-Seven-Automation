# Epic Seven Automation Tool
This project utilizes ADB (Android Debug Bridge) tools to connect the emulators and simulate click actions. Since it uses ADB to communicate with emulators, it won't take away the keyboard and mouse control. 

# Current Feature
## Refresh Shop Demo
![Shop Refresh Demo](https://github.com/user-attachments/assets/a9f84448-8fa2-4701-a5bd-232e0a2a566e)

## Daily Arena Demo
To be added

# Getting Started
## Prerequisites
Please make sure to use **Python 3.11.0** as the higher python version is not compatible with one of the libraries in requirement.txt.

Use  ```sh pip install -r requirement.txt ``` to install required libraries

Use ```sh py main.py ``` to start the script

# Possible Questions
### Is this script usable in different emulators?
This script has been tested in LD player, BlueStack, and Google Play Games Developer Emulator (**Not Goole Play Games**) with various resolutions including 1920x1080, 1600x900, and 2400x1080. 
Please be aware that the higher resolution the slower it might be when running the script.
### Why there is No Device Found after starting the script even though my emulator is started?
Please make sure that your ADB (Android Debug Bridge) in your emulator setting is checked. If the issue persists then please try rebooting your pc.
