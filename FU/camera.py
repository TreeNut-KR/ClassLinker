import cv2
from pygrabber.dshow_graph import FilterGraph

class Camera:
    def __init__(self):
        self.available_cameras = {}
        try:
            self.devices = FilterGraph().get_input_devices()
        except ValueError:
            self.devices = None
        self.camera_name = 'UC60 Video'
        self.cap = None
        self.name = ""
        
    def get_available_cameras(self):
        self.available_cameras = {}
        if self.devices is not None:
            for device_index, device_name in enumerate(self.devices):
                self.available_cameras[device_index] = device_name
        else:
            pass
        
    def cameras_list(self):
        self.get_available_cameras()
        return self.available_cameras
    
    def open_camera(self):
        available_cameras = self.cameras_list()
        if available_cameras:
            for i in available_cameras:
                if available_cameras[i] == self.camera_name:
                    self.cap = cv2.VideoCapture(i)
                    self.name = available_cameras[i]
                elif self.cap == None:
                    self.cap = cv2.VideoCapture(0)
                    self.name = available_cameras[0]
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', 'E', 'V', 'C'))
        else:
            self.cap = None
            self.name = None
    
    def set_cap_size(self, width: int, height: int):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame

    def release_camera(self):
        if self.cap is not None:
            self.cap.release()

    def is_camera_open(self):
        return self.cap is not None

    def __del__(self):
        self.release_camera()
