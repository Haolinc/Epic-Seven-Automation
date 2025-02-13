# Epic Seven Automation Tool
![app-9](https://github.com/user-attachments/assets/dd3deb72-196b-4051-b477-3524c1de6349)

This project utilizes ADB (Android Debug Bridge) tools to connect the emulators and simulate user actions without taking away the keyboard and mouse control. 

# Current Feature
## Refresh Shop Demo
![Shop Refresh Demo](https://github.com/user-attachments/assets/a9f84448-8fa2-4701-a5bd-232e0a2a566e)

## NPC Challenge Arena Demo
![Daily Arena Demo](https://github.com/user-attachments/assets/b4f48c6e-c5a5-4a7a-ae5f-e606f6b847e5)


# Installation
## Direct Download
Download via Google Drive: https://drive.google.com/file/d/1JcYvzmtRjfqSq9mmjhV9tdmS-F-iL6o2/view?usp=drive_link

## Github
Please make sure to use **Python 3.11.0** as the higher python version is not compatible with one of the libraries in requirement.txt.

Use  ```pip install -r requirement.txt``` to install required libraries.

Then use ```py EpicSevenAutomationLauncher.py``` or directly run ```EpicSevenAutomationLauncher.py``` from IDE to start the tool.

OR

Use ```pyinstaller --onefile --windowed --add-data="image:image" --add-data="platform-tools:platform-tools" --icon=image\app.ico EpicSevenAutomationLauncher.py``` to compile an EXE file.

Executable file usually located under project's ```dist``` folder.

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
