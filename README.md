# 4810_web_server

app.py launchs the web server which displays the dispensers telemetry. The telemetry information is sent to app.py through a socket connection between it and the sensors.py file.
sensors.py has 2 primary functions. One is sending the mask telemetry information to the app.py file. The other is to operate the dispener. 
support.py is a helper file for sensors.py, which contains initializations, and base functions. 

When you run app.py, if the terminal states "Running on http://0.0.0.0:5000/ ", you'll need to aquire the usable ip adress another way. If you're using linux you can use the command "sudo ifconfig". Once the devices ip address is aquired, put the IP in a browser with the format "http://x.x.x.x:5000/" and you'll connect to the web server.

sensors.py should be run before app.py to ensure the socket port can be properly binded to by sensors.py as it acts as the server of the sockets.