from mainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import cv2
import pyrealsense2 as rs
import numpy as np
import csv
import os
import shutil
from threading import Lock


class Controller(Ui_MainWindow):
    def __init__(self, parent):
        self.parent = parent
        self.setupUi(self.parent)

        self.pose = "poses.txt"
        self.image_1_odo = None
        self.image_2_odo = None
        self.pose_old = None
        self.pose_new = None
        self.pose_1_x = None
        self.pose_1_y = None
        self.pose_1_z = None
        self.pose_2_x = None
        self.pose_2_y = None
        self.pose_2_z = None

        self.i = 0
        self.i_save = 0
        self.frame_mutex = Lock()
        self.frame_data = {"left": None,
                           "right": None,
                           "timestamp_ms": None
                           }
        self.data = None
        self.timer_tes = "pause"
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.initCameraIntel()

        self.openImage.clicked.connect(self.open_camera_1)
        self.openImage_2.clicked.connect(self.resetPoseCameraIntel)
        self.saveSequenceBtn.clicked.connect(self.saveMove)

    def initCameraIntel(self):
        try:
            self.pipe_img = rs.pipeline()
            self.cfg_img = rs.config()
            self.pipe_img.start(self.cfg_img)
            self.cfg_img.enable_stream(rs.stream.pose, rs.format.six_dof)
            self.cfg_img.enable_stream(rs.stream.fisheye, 1)
            self.cfg_img.enable_stream(rs.stream.fisheye, 2)
            print("camera detected")
        except:
            print("no camera detected")

    def resetPoseCameraIntel(self):
        self.initCameraIntel()
        self.i = 0
        self.i_save = 0
        self.nextFrame()

    def open_camera_1(self):
        """
        open the camera from the available source in the system,
        this function provide 2 source namely USB cam and Streaming Cam from Raspberry pi.
        """
        self.cam = True
        self.nextFrame()

    def nextFrame(self):
        """
        looping the frame showing in label user interface.

        """
        if self.cam:
            frames = self.pipe_img.wait_for_frames()
            pose = frames.get_pose_frame()
            self.valid = self.frame_data["timestamp_ms"] is not None

            left = frames.get_fisheye_frame(1)
            left = np.asanyarray(left.get_data())
            image3 = cv2.resize(left, (848, 800), interpolation=cv2.INTER_AREA)
            label = self.labelIntelL
            label.setMaximumSize(QtCore.QSize(848, 800))
            label.setMinimumSize(QtCore.QSize(848, 800))
            image3 = QtGui.QImage(image3.data, image3.shape[1], image3.shape[0],
                                  QtGui.QImage.Format_Indexed8)  # .rgbSwapped() #.isGrayscale()
            label.setPixmap(QtGui.QPixmap.fromImage(image3))

            right = frames.get_fisheye_frame(2)
            right = np.asanyarray(right.get_data())
            image4 = cv2.resize(right, (848, 800), interpolation=cv2.INTER_AREA)
            label = self.labelIntelR
            label.setMaximumSize(QtCore.QSize(848, 800))
            label.setMinimumSize(QtCore.QSize(848, 800))
            image4 = QtGui.QImage(image4.data, image4.shape[1], image4.shape[0],
                                  QtGui.QImage.Format_Indexed8)  # .rgbSwapped() #.isGrayscale()
            label.setPixmap(QtGui.QPixmap.fromImage(image4))
            if pose:
                self.pose_data = pose.get_pose_data()
                self.frameSystem.setText(str(self.i))
                self.frameIntel.setText(str(pose.frame_number))

                # self.timer.setInterval(40)
                x_now = self.pose_data.translation.x
                y_now = self.pose_data.translation.y
                z_now = self.pose_data.translation.z
                r_x_now = self.pose_data.rotation.x
                r_y_now = self.pose_data.rotation.y
                r_z_now = self.pose_data.rotation.z

                if self.saveSequenceBtn.isChecked():
                    with open(self.pose, mode='a') as csv_file:
                        employee_writer = csv.writer(csv_file, delimiter=' ')
                        employee_writer.writerow([round(x_now, 5),
                                                  round(y_now, 5),
                                                  round(z_now, 5),
                                                  round(r_x_now, 5),
                                                  round(r_y_now, 5),
                                                  round(r_z_now, 5)])
                    cv2.imwrite("intelL/" + str(self.i_save) + ".png", left)
                    cv2.imwrite("intelR/" + str(self.i_save) + ".png", right)
                    self.frameSave.setText(str(self.i_save))
                    self.i_save += 1
                self.i += 1
                self.move_x.setText(str(round(x_now, 3)))
                self.move_y.setText(str(round(y_now, 3)))
                self.move_z.setText(str(round(z_now, 3)))
        self.timer.start(int(1000 / 18))

    def saveMove(self):
        self.resetPoseCameraIntel()
        if self.saveSequenceBtn.isChecked():
            with open(self.pose, mode='a') as csv_file:
                employee_writer = csv.writer(csv_file, delimiter=' ')
                employee_writer.writerow([0,
                                          0,
                                          0,
                                          0,
                                          0,
                                          0])

    def saveSequence(self):
        if self.saveSequenceBtn.isChecked():
            self.removeAllFiles("intelL")
            self.removeAllFiles("intelR")

            if os.path.exists("poses_13.txt"):
                os.remove("poses_13.txt")

            if os.path.exists("start.txt"):
                os.remove("start.txt")

    def removeAllFiles(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == "__main__":
    apps = QtWidgets.QApplication(sys.argv)
    ui = QtWidgets.QMainWindow()
    a = Controller(ui)
    ui.show()
    sys.exit(apps.exec_())
