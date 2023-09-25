# -*- coding: utf-8 -*-
import math
import cv2
import random
import cvzone
import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector
from tkinter import *

window_width = 1100
window_height = 800

cap = cv2.VideoCapture(0)
cv2.namedWindow("Fairuz", cv2.WINDOW_NORMAL)  # Use WINDOW_NORMAL flag for resizable window
cv2.resizeWindow("Fairuz", window_width, window_height)
detector = HandDetector(detectionCon=0.2, maxHands=1)


class SnakeGameClass:
    def __init__(self, pathFood):
        self.initializeData()
        self.gameOver = False
        self.score = 0
        # interactging with the food
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape  # get deminsions size image

    def randomLocation(self):
        self.foodPoint = random.randint(100, 300), random.randint(100, 300)

    def initializeData(self):
        self.points = []  # all points of snake
        self.lenghts = []  # distances between each point
        self.currentLength = 0  # total lenght of the snake
        self.allowedLength = 150
        self.previousHead = 0, 0
        self.foodPoint = 0, 0
        self.randomLocation()

    def update(self, imgMain, currentHead):

        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300 // 2, 400 // 2], scale=3, thickness=3,
                               offset=20)
            cvzone.putTextRect(imgMain, f'Your Score {self.score}', [300 // 2, 550 // 2], scale=2, thickness=2,
                               offset=10)

        else:
            cx, cy = currentHead
            px, py = self.previousHead
            self.points.append((cx, cy))
            distance = math.hypot(cx - px, cy - py)
            self.lenghts.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy
            # length reduction
            self.reduceLength()
            # check if the snake ate the food
            rx, ry = self.foodPoint
            if (rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2
                    < cy < ry + self.hFood // 2):
                self.score += 1

                self.allowedLength += 50
                self.randomLocation()

            # draw snake
            if (self.points):
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 10)
                cv2.circle(imgMain, self.points[-1], 10, (200, 0, 200), cv2.FILLED)
            # draw dount
            cvzone.putTextRect(imgMain, f'Score {self.score}', [50, 50], scale=3, thickness=2,
                               offset=10)
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))

            if self.score >= 30:
                self.initializeData()
                cvzone.putTextRect(imgMain, "Level Passed Successfully!", [300 // 2, 400 // 2], scale=2, thickness=2,
                                   offset=10)
            # check for collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 200, 0), 2)
            distace = cv2.pointPolygonTest(pts, (cx, cy), True)
            if (-1 <= distace <= 1):
                self.gameOver = True
                self.initializeData()

        return imgMain

    def reduceLength(self):
        if (self.currentLength > self.allowedLength):
            for i, lenght in enumerate(self.lenghts):
                # i keep reducing form the length snake until reach the allowed length
                self.currentLength -= lenght
                self.lenghts.pop(i)
                self.points.pop(i)
                if (self.currentLength < self.allowedLength):
                    break


game = SnakeGameClass("donut.png")

window_open = True

while window_open:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]

        if 'lmList' in hand:
            lmlist = hand['lmList']
            tip = lmlist[8][0:2]
            img = game.update(img, tip)

    # Add a note to the video screen
    cv2.putText(img, "Press Esc to Stop", (350, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display the video frame
    cv2.imshow("Fairuz", img)

    # Check for the "Escape" key (27) to close the window
    key = cv2.waitKey(1)
    if key == 27:
        window_open = False  # Set the flag to False to exit the loop

# Release the video capture and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
