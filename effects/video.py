import cv2
from BaseEffect import BaseEffect, ColorMode
from helpers import process_image

VIDEO_NAME = 'videos/tennis.mp4'

def generate_frames(video_name, points):
    cap = cv2.VideoCapture(video_name)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frames.append(process_image(points, frame) / 2.0)
        else:
            break
    cap.release()
    return frames

class Effect(BaseEffect):
    def __init__(self, points):
        super().__init__(points)
        self.color_mode = ColorMode.RGB
        self.max_fps = 30
        self.frames = generate_frames(VIDEO_NAME, self.points)
        self.frame = 0

    def update(self):
        self.colors = self.frames[self.frame]
        self.frame += 1
        self.frame %= len(self.frames)
