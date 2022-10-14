# Rocket-Elevators-Python-Controller

# Usage
To do some tests you can uncomment a bit of code at the end of my file. The scenarios are the same as on the Javascript program so I didn't translate all of them into code. In the video, I'll look into Javascript and Python but I almost used same methods on both, except for the findElevator method. First, you need to download the latest stable version of python.

## Example
Commands that you can use to download npm and use it after to run tests :
pytest
or to try the scenario at the end of the file :
python residential_controller.py

# Description
Example:

This program controls a Column of elevators.

It sends an elevator when a user presses a button on a floor and it takes
a user to its desired floor when a button is pressed from the inside of elevator.

Elevator selection is based on scores given by their activity when the request is done. 1 is the best score you have, it means the elevator is at your floor, it is stopped and it goes in the same direction as you requested. At the opposite, the worst score is 4, when most of elevators are unavailable and you peek the closest to you.

# Video Link
Here is my explanation video link about my code : https://youtu.be/Z-z0zh8e3Vk