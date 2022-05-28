
globe = 17

def changer():
    global globe
    for i in range(3):
        globe += i
        print("func. globe: " + str(globe))

def view():
    print(str(globe) + ":" + str(globe + 10))

changer()
view()
changer()
view()
print("final globe: " + str(globe))

