import cv2
import numpy as np
from pygrabber.dshow_graph import FilterGraph
from typing import Dict, Union, Any

class Camera:
    def __init__(self, camera_name: str = 'UC60 Video') -> None:
        self.cap = None
        self.devices = None
        self.camera_name = camera_name
        self.name = ""
        try:
            self.devices = FilterGraph().get_input_devices()
        except ValueError:
            pass

    @property
    def cameras_list(self) -> Dict[int, str]:
        if self.devices is not None:
            return {device_index: device_name for device_index, device_name in enumerate(self.devices)}
        else:
            return {}

    @property
    def frame(self) -> Union[np.ndarray, None]:
        if self.cap:
            _, frame = self.cap.read()
            return frame
        else:
            return None

    def open_camera(self) -> None:
        if self.cameras_list:
            for i in self.cameras_list:
                if self.cameras_list[i] == self.camera_name:
                    self.cap = cv2.VideoCapture(i)
                    self.name = self.cameras_list[i]
                elif self.cap == None:
                    self.cap = cv2.VideoCapture(0)
                    self.name = self.cameras_list[0]
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', 'E', 'V', 'C'))
        else:
            self.cap = None
            self.name = None
    
    def set_cap_size(self, width: int, height: int):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

    def release_camera(self):
        if self.cap is not None:
            self.cap.release()

    def __del__(self):
        self.release_camera()
