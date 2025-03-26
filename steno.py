import cv2
import numpy as np
import time

class stenography:
    
    def msgtobinary(msg):
        if type(msg) == str:
            result= ''.join([ format(ord(i), "08b") for i in msg ])
        
        elif type(msg) == bytes or type(msg) == np.ndarray:
            result= [ format(i, "08b") for i in msg ]
        
        elif type(msg) == int or type(msg) == np.uint8:
            result=format(msg, "08b")

        else:
            raise TypeError("Input type is not supported in this function")
        
        return result



    def encode_img_data(data):
        img = cv2.imread("img.png")
        if (len(data) == 0): 
            raise ValueError('Data entered to be encoded is empty')
        
        no_of_bytes=(img.shape[0] * img.shape[1] * 3) // 8
     
        data +='*^*^*'    
        
        binary_data=stenography.msgtobinary(data)
        length_data=len(binary_data)
        
        index_data = 0
        
        for i in img:
            for pixel in i:
                b, g, r = stenography.msgtobinary(pixel)
                if index_data < length_data:
                    pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data < length_data:
                    pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data < length_data:
                    pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                    index_data += 1
                if index_data >= length_data:
                    break
            if index_data >= length_data:
                break
            
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        success, encoded_image = cv2.imencode('.png', img)
        return encoded_image.tobytes()
        
    def decode_img_data(img):
        # image = np.frombuffer(img, dtype=np.uint8)
        image = cv2.imdecode(np.frombuffer(img, np.uint8), -1)

        image2 = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2BGR)
        data_binary = ""
        for i in image2:
            for pixel in i:
                r, g, b = stenography.msgtobinary(pixel) 
                data_binary += r[-1]  
                data_binary += g[-1]  
                data_binary += b[-1]  
                total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
                decoded_data = ""
                for byte in total_bytes:
                    decoded_data += chr(int(byte, 2))
                    if decoded_data[-5:] == "*^*^*": 
                        return decoded_data[:-5]
