import json
import time
import numpy as np
from websocket import create_connection

MAX_FPS = 40
MAX_SPF = 1 / MAX_FPS

class RemoteTree(object):
    def __init__(self, remote_url, points):
        self.points = points
        self.ws = create_connection('ws://' + remote_url)
    
    def off(self):
        self.ws.close()
    
    def render_frame(self, frame):
        rgb = (frame() * 255).astype(np.uint8).tolist()
        out = json.dumps(rgb)
        self.ws.send(out)
        response = self.ws.recv()
        buffer_size = int(response)
        if buffer_size > 20:
            time.sleep(10 * MAX_SPF)