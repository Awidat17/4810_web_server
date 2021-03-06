from urllib.request import urlopen
from flask import Flask, redirect, render_template, request, session, url_for
import socket

# initializes app
app = Flask(__name__)
app.secret_key = "work"
status = "Worked"

# home page 
@app.route("/", methods=["POST", "GET"])
def home():
    # checks if web page button pressed
    if request.method == "POST":
        # open count web page
        return redirect(url_for("count"))
    else:
        # keep home page open
        return render_template("index.html")

# status page
@app.route("/count", methods=["POST", "GET"])
def count():
    
    # gets ip address
    myIpAdd = request.host_url
    myIp = str(str(myIpAdd) + "count")
    msg_str = None

    # tries to creats a new socket and gets the number of masks and status
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((socket.gethostname(),4321))
        msg = s.recv(1024) 
        msg_str = (msg.decode("utf-8")).split(':')
        s.close()
    except:
        msg_str = ["0", "Reload..."]
    
    # checks if web page button pressed
    if request.method == "POST":
        # open home web page
        return redirect(url_for("home"))
    else:
        # open count web page
        return render_template("count.html", cnt = msg_str[0], status = msg_str[1], ip_add = myIp)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug=True)


