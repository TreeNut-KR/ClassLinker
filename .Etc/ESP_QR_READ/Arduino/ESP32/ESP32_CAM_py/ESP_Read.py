import numpy as np
import time
import urllib.request
from PIL import Image
from io import BytesIO
from multiprocessing import Pool

from QR import QRcode_read

class ESP_frame(QRcode_read):
    def __init__(self) -> None:
        super().__init__()

    def Reading(self):
        with Pool() as p:
            while True:
                img_resp=urllib.request.urlopen(self.url+'/cam-hi.jpg')
                imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
                frame=Image.open(BytesIO(imgnp))
                frame = np.array(frame)
                result = p.apply_async(self.Decoding, [frame])
                Data = result.get()
                if Data is not None:
                    if self.qr_code_save != Data:
                        self.qr_code_save = Data
                        print(Data)
                time.sleep(0.03)

if __name__ == "__main__":
    ESP_frame().Reading()
