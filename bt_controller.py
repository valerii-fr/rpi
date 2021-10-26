from evdev import InputDevice, categorize, ecodes

print("VR BOX Controller test")

#create objects

vrbox = InputDevice('/dev/input/event2')

btnUp = 273
btnDown = 272
x_var = 0
y_var = 1

for event in vrbox.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == btnUp:
                print("UP")
            elif event.code == btnDown:
                print("DOWN")
    elif event.type == ecodes.EV_REL:
        if event.code == x_var:
            print("X: {x}" .format(x=event.value))
        elif event.code == y_var:
            print("Y: {y}".format(y=event.value))