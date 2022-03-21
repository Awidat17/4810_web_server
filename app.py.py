import re
from urllib.request import urlopen
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "work"

status = "Working"

url = 'http://checkip.dyndns.org'
req = urlopen(url).read().decode('utf-8')
myIp = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", req)
myIp = str("http://" + str(myIp)[2:-2] + "/count")

@app.route("/")
def home():
    return render_template("index.html", author = myIp, enemys = ["ploii", "will", "alex", "greg"])

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
    if request.method == "POST":
        return redirect(url_for("demo"))
    elif "count" in session:
        session["count"] = int(session["count"]) - 1
        return render_template("count.html", cnt = session["count"], status = status)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80, debug=True)