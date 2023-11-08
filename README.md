# v1
- Commented out all gyro features
- Building basic move/turnr/turnl functions
- ToDo: implement and practice barebone functions (practice timing), then implement gyro if possible, then implement calibration
- Find wheel ration so we can set all wheel speeds to global variable 'x' and change it at once based on competition target time (another ToDo)
- We need a second and third global variable. The second variable will by 'y', representing the ratio the static variable x changes by. The third variable will be the time sleep needed to hit 50 cm, which will be divided by y (therefore keepign the travel distance as 50 cm for all speeds
- Gyro to go straight cuz its kinda funky
- Idea: turn speed to stall (roughly a second extra per turn is not too bad)
