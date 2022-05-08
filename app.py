from urllib.request import urlopen
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "work"

status = "Working"

@app.route("/")
def home():
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
    
    myIpAdd = request.host_url
    myIp = str(str(myIpAdd) + "count")

    if request.method == "POST":
        return redirect(url_for("demo"))
    elif "count" in session:
        session["count"] = int(session["count"]) - 1
        return render_template("count.html", cnt = session["count"], status = status, ip_add = myIp)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug=True)