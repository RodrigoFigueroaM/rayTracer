from PyQt5.QtGui import QMatrix4x4, QVector3D

from rayTracer.Camera import Camera


def test1():
    D = QMatrix4x4(4, -1, 1, 0,
                   2, 2, 3, 0,
                   5, -2, 6, 0,
                    0, 0, 0, 1)

    Dx = QMatrix4x4(12, -1, 1, 0,
                    1, 2, 3, 0,
                    22, -2, 6,0,
                    0, 0, 0, 1)

    Dy = QMatrix4x4(4, 12, 1, 0,
                    2, 1, 3, 0,
                    5, 22, 6,0,
                    0, 0, 0, 1)

    Dz = QMatrix4x4(4, -1, 12, 0,
                    2, 2, 1, 0,
                    5, -2, 22, 0,
                    0, 0, 0, 1)

    print('det(D)= ', D.determinant())
    print('det(Dx)= ', Dx.determinant())
    print('det(Dy)= ', Dy.determinant())
    print('det(Dz)= ', Dz.determinant())

    print('x = ', Dx.determinant()/D.determinant())
    print('y = ', Dy.determinant()/D.determinant())
    print('z = ', Dz.determinant()/D.determinant())


def test2():
    cam = Camera(position=QVector3D(0, 0, 3),
                 lookAt=QVector3D(0, 0, 0),
                 up=QVector3D(0, 1, 0),
                 viewingPlaneDistance = 1)
    e = cam.position
    l = cam.lookAt
    ed = cam.direction
    w = cam._back
    u = cam.right
    v = cam.up

    # print(e)
    # print(l)
    # print(ed)
    # print("W", w)
    # print('U', u)
    # print(v)

    xw = (250 - 0.5 * (500 + 1.0))
    yw = (250 - 0.5 * (500 + 1.0))
    s = QVector3D(xw, yw, cam.viewingPlaneDistance)
    print(s)
    pt = cam.up * s.y() + cam.right * s.x() - cam._back * s.z()
    print(pt)
    rayO = cam.position
    rayD = (pt - cam.position).normalized()
    print('rayO = ', rayO)
    print('rayD = ', rayD)
    ray = cam.rayCast(250, 250, 500, 500)
    print(ray)
    ray = cam.obliqueRayCast(250, 250, 500, 500)
    print(ray)
    ray = cam.perspectiveRayCast(250, 250, 500, 500)
    print(ray)



def test3():
    xw = (0 - 0.5 * (500 + 1.0))
    yw = (0 - 0.5 * (500 + 1.0))
    print(xw, yw)
# test2()



def testChallenge():
    ''' infront of monster'''
    monsterPos = QVector3D(100, 100, 0)
    monsterDir = QVector3D(1, 0, 0)
    applePos = QVector3D(1, 0, 0)
    monsterFacing = monsterDir - monsterPos
    monsterToApple = applePos - monsterPos
    print(QVector3D.dotProduct(monsterFacing.normalized(), monsterToApple.normalized()))
    # print(monsterFacing)


print(QVector3D(0.5, 0.5, 0.5) * QVector3D(250,250,250) * 0.5)