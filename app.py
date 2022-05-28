from urllib.request import urlopen
from flask import Flask, redirect, render_template, request, session, url_for
import socket

app = Flask(__name__)
app.secret_key = "work"

status = "Worked"

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("count"))
    else:
        return render_template("index.html")

@app.route("/count", methods=["POST", "GET"])
def count():
    
    # gets ip address
    myIpAdd = request.host_url
    myIp = str(str(myIpAdd) + "count")
    msg_str = None
    # tries to creats a new socket and gets the number of masks and status
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((socket.gethostname(),1234))
        msg = s.recv(1024) 
        msg_str = (msg.decode("utf-8")).split(':')
        s.close
    except:
        msg_str = ["No Number Sent", "No Connection"]
    
    if request.method == "POST":
        return redirect(url_for("demo"))
    else:
        return render_template("count.html", cnt = msg_str[0], status = msg_str[1], ip_add = myIp)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 4321, debug=True)


