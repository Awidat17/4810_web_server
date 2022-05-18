from urllib.request import urlopen
from flask import Flask, redirect, render_template, request, session, url_for
import socket

app = Flask(__name__)
app.secret_key = "work"

status = "Worked"

@app.route("/")
def home():
    print("hello")
    return render_template("index.html", author = request.host_url, enemys = ["Blow", "Gill"])

@app.route("/demo", methods=["POST", "GET"])
def demo():
    if request.method == "POST":
        count = request.form["nm"]
        session["count"] = count
        return redirect(url_for("count"))
    else:
        return render_template("index2.html")

@app.route("/count", methods=["POST", "GET"])
def count():
    
    # gets ip address
    myIpAdd = request.host_url
    myIp = str(str(myIpAdd) + "count")

    # creats a new socket and gets the number of masks and status
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((socket.gethostname(),1234))
    msg = s.recv(1024) 
    msg_str = (msg.decode("utf-8")).split(':')

    if request.method == "POST":
        return redirect(url_for("demo"))
    elif "count" in session:
        session["count"] = int(session["count"]) - 1
        return render_template("count.html", cnt = msg_str[0], status = msg_str[1], ip_add = myIp)
        #return render_template("count.html", cnt = session["count"], status = status, ip_add = myIp)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug=True)


