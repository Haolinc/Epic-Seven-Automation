# Epic Seven Automation Tool
This project utilizes ADB (Android Debug Bridge) tools to connect the emulators and simulate click actions. Since it uses ADB to communicate with emulators, it won't take away the keyboard and mouse control. 

# Current Feature
## Refresh Shop Demo
![Shop Refresh Demo](https://github.com/user-attachments/assets/a9f84448-8fa2-4701-a5bd-232e0a2a566e)

## NPC Challenge Arena Demo
![Daily Arena Demo](https://github.com/user-attachments/assets/b4f48c6e-c5a5-4a7a-ae5f-e606f6b847e5)


# Getting Started
## Installation
### Direct Download
(To be added)
### Github
Please make sure to use **Python 3.11.0** as the higher python version is not compatible with one of the libraries in requirement.txt.

Use  ```pip install -r requirement.txt ``` to install required libraries.

Use ```py main.py ``` or directly run ```main.py``` from IDE to start the script.

# Usage
1. Launch the emulator, make sure your emulator is enabled with ADB.
![ADBSetting](https://github.com/user-attachments/assets/537e7d17-5b62-4791-a95d-2b9b99f73a05)


2. Start the application

## Device Selection
1. Select the desired emulator. If it's not listed, click Refresh Device List.

![Starting](https://github.com/user-attachments/assets/8543b65e-b475-47e5-a086-66c2fc1ba1bb)

2. Click Start Application

## Shop Refresh
1. Go to secret shop page

![ShopImage](https://github.com/user-attachments/assets/bdccbe27-a4ed-498d-b846-f692dbbc0904)

2. Input desired refresh iteration, value has to be starting from 0.

![ShopRefreshInput](https://github.com/user-attachments/assets/82ab1bbe-6c72-464f-9e0f-d585faeb90c1)

3. Click Start Shop Refresh to start the application.
## NPC Challenge Arena
1. Go to arena page

![Arena](https://github.com/user-attachments/assets/f8c27e30-46cd-42ea-8ce1-b9a4a7a50db4)
   
2. Input desired challenge iteration, value has to be starting from 0. If you want to purchase friendship bookmark for an additional 5 arena flags, select Arena With Extra.

![ArenaInput](https://github.com/user-attachments/assets/37c1a463-03ab-4311-9d87-e9e9b00537f8)

(Note: When selecting Arena With Extra, enter only the base iteration count (excluding extras). For example, for 5 challenges plus friendship bookmark extra (total 10 iterations), enter 5 and select "Arena With Extra.")


3. Click Start Shop Refresh to start the application.

# Possible Questions
### Is this script usable in different emulators?
This script has been tested in LD player, BlueStack, and Google Play Games Developer Emulator (**Not Goole Play Games**) with various resolutions including 1920x1080, 1600x900, and 2400x1080. 
Please be aware that the higher resolution the slower it might be when running the script.
### Why there is No Device Found after starting the script even though my emulator is started?
Please make sure that your ADB (Android Debug Bridge) in your emulator setting is checked. If the issue persists then please try rebooting your PC.
