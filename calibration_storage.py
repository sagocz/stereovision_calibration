import cv2

def saveCoefficients(mtx, dist, path):

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("K", mtx)
    cv_file.write("D", dist)
    cv_file.release()

def saveStereoCoefficients(path, K1, D1, K2, D2, R, T, E, F, R1, R2, P1, P2, Q)

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("K1", K1)
    cv_file.write("D1", D1)
    cv_file.write("K2", K2)
    cv_file.write("D2", D2)
    cv_file.write("R", R)
    cv_file.write("T", T)
    cv_file.write("E", E)
    cv_file.write("F", F)
    cv_file.write("R1", R1)
    cv_file.write("R2", R2)
    cv_file.write("P1", P1)
    cv_file.write("P2", P2)
    cv_file.write("Q", Q)

def loadCoefficients(path):

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    camera_matrix = cv_file.getNode('K').mat()
    dist_matrix = cv_file.getNode('D').mat()

    cv_file.release()

    return [camera_matrix, dist_matrix]

def loadStereoCoefficients(path):

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    K1 = cv_file.getNode('K1').mat()
    D1 = cv_file.getNode('D1').mat()
    K2 = cv_file.getNode('K2').mat()
    D2 = cv_file.getNode('D2').mat()
    R = cv_file.getNode('R').mat()
    T = cv_file.getNode('T').mat()
    E = cv_file.getNode('E').mat()
    F = cv_file.getNode('F').mat()
    R1 = cv_file.getNode('R1').mat()
    R2 = cv_file.getNode('R2').mat()
    P1 = cv_file.getNode('P1').mat()
    P2 = cv_file.getNode('P2').mat()
    Q = cv_file.getNode('Q').mat()

    cv_file.release()
    return [K1, D1, K2, D2, R, T, E, F, R1, R2, P1, P2, Q] 