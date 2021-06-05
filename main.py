import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

suc = 1

Tp_x = [0]
Tp_y = [0]
Tp_z = [0]

Ta_x = 0
Ta_y = 0

var = ["Tp_x[0]", "Tp_y[0]", "Tp_z[0]", "Ta_x", "Ta_y"]
comment = ["X location of target:", "Y location of target:", "Z location of target:", "X angle of target direction:",
           "Y angle of target direction:"]
for i in range(5):
    exec(var[i] + " = float(input(comment[i]))")

Tspd = 1

Mp_x = [0]
Mp_y = [0]
Mp_z = [0]

Ma_x = 0
Ma_y = 0

Mspd = 3

d = []
stop = 1000
stop2 = 10

der = [0, 0, 0]
i = 0
j = 0

ii = 5
jj = 0

Ab = [0, 0]
Ae_x = [0]
Ae_y = [0]

acel = 10

p = 4

def distanceT():  # 미사일-목표 거리
    return np.sqrt(((Tp_x[-1] - Mp_x[-1]) ** 2) + ((Tp_y[-1] - Mp_y[-1]) ** 2) + ((Tp_z[-1] - Mp_z[-1]) ** 2))


def distance():  # x,y,z축 거리
    return (Tp_x[-1] - Mp_x[-1]), (Tp_y[-1] - Mp_y[-1]), (Tp_z[-1] - Mp_z[-1])


def angle():  # 미사일-목표 각도
    d = distance()
    x = np.arctan2(d[0], d[1])
    y = np.arctan2(d[2], np.sqrt(d[0] ** 2 + d[1] ** 2))

    if x < 0:
        x += np.pi * 2

    if d[2] < 0:
        y = np.pi / 2 - y

    if x > np.pi * 2:
        x % (np.pi * 2)

    if y >= (np.pi * 2):
        if (y % (np.pi * 2)) >= np.pi:
            x += np.pi
            y = np.pi - (y % np.pi)
        else:
            y = y % np.pi

    if y >= np.pi:
        x += np.pi
        y -= np.pi * 2

    if y <= -np.pi * 2:
        if -(y % (np.pi * 2)) >= np.pi:
            y += np.pi * 2
        else:
            x += np.pi
            y = -(y - np.pi * 2)

    if y <= -np.pi:
        x += np.pi
        y += np.pi * 2

    if x < 0:
        x += np.pi * 2

    return x, y


def angle_sight():  # 미사일-목표 각도
    d = distance()
    x = np.arctan2(d[0], d[1])
    y = np.arctan2(d[2], np.sqrt(d[0] ** 2 + d[1] ** 2))

    x -= Ma_x

    if x <= 0:
        x += np.pi * 2
    if x >= np.pi * 2:
        x = x % (np.pi * 2)

    if d[2] < 0:
        y = np.pi / 2 - y

    if y >= (np.pi * 2):
        if (y % (np.pi * 2)) >= np.pi:
            x += np.pi
            y = np.pi - (y % np.pi)
        else:
            y = y % np.pi

    if y <= -np.pi * 2:
        if -(y % (np.pi * 2)) >= np.pi:
            y += np.pi * 2
        else:
            x += np.pi
            y = -(y - np.pi * 2)

    if y <= -np.pi:
        x += np.pi
        y += np.pi * 2

    if y >= np.pi:
        x += np.pi
        y -= np.pi * 2

    y = y - np.pi / 2 - Ma_y

    if y >= np.pi / 2:
        x += np.pi
        y = np.pi / 2 - y

    if d[-1] > d[-2]:
        if y <= -np.pi:
            x += np.pi
            y = -(y + np.pi)

    if x < 0:
        x += np.pi * 2

    if x >= np.pi * 2:
        x = x % (np.pi * 2)

    return x, y


Ma_x, Ma_y = angle()
d.append(distanceT())

while distanceT() > 2:  # 충돌할때까지 반복
    i += 1
    j += 1
    stop -= 1

    x = Tspd * np.sin(np.radians(Ta_y)) * np.sin(np.radians(Ta_x))
    y = Tspd * np.sin(np.radians(Ta_y)) * np.cos(np.radians(Ta_x))
    z = Tspd * np.cos(np.radians(Ta_y))

    Tp_x.append(Tp_x[-1] + x)
    Tp_y.append(Tp_y[-1] + y)
    Tp_z.append(Tp_z[-1] + z)

    x = Mspd * np.sin(Ma_y) * np.sin(Ma_x)
    y = Mspd * np.sin(Ma_y) * np.cos(Ma_x)
    z = Mspd * np.cos(Ma_y)

    Mp_x.append(Mp_x[-1] + x)
    Mp_y.append(Mp_y[-1] + y)
    Mp_z.append(Mp_z[-1] + z)

    x = 50 * np.sin(Ma_y) * np.sin(Ma_x) + Mp_x[-1]
    y = 50 * np.sin(Ma_y) * np.cos(Ma_x) + Mp_y[-1]  # 예상 위치
    z = 50 * np.cos(Ma_y) + Mp_z[-1]
    der[0], der[1], der[2] = x, y, z

    d.append(distanceT())

    if i == ii:
        Ae_x.append(angle_sight()[0] - Ab[0])
        Ae_y.append(angle_sight()[1] - Ab[1])

        Ma_x += Ae_x[-1] * p
        Ma_y += Ae_y[-1] * p

        if Ma_x <= 0:
            Ma_x += np.pi * 2
        if Ma_x >= (np.pi * 2):
            Ma_x = Ma_x % (np.pi * 2)

    if i == ii:
        Ab = angle_sight()
        i = 0

    plt.pause(0.00001)

    ax.scatter(Mp_x, Mp_y, Mp_z, c='b', marker='o', s=1)
    ax.scatter(Tp_x, Tp_y, Tp_z, c='r', marker='o', s=1)
    if j == jj:
        plt.plot([Mp_x[-1], der[0]], [Mp_y[-1], der[1]], [Mp_z[-1], der[2]], c='g')
        j = 0

    if stop < 0 or (d[-1] > d[-2] and Ae_x[-1] < 0.00001 and Ae_y[-1] < 0.00001):
        suc = 0
        break

if suc == 1:
    print("Target destroy")
else:
    print("Fail")

plt.show()
