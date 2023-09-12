from OpenGL.arrays import vbo
import OpenGL.GL as gl
from OpenGL import GLU
from PyQt5 import QtOpenGL
from PyQt5 import QtGui
from PIL import Image as img
import numpy as np
import ctypes
import os

def get_image_format(image_path):
    """
    Determine the image format of a given image.

    Args:
    - image_path (str): Path to the image file.

    Returns:
    - str: The format of the image (e.g., "PNG", "JPG"). Returns None if the file is not a recognized image format.
    """
    try:
        with img.open(image_path) as imgs:
            return imgs.format
    except Exception as e:
        print(f"Error reading image: {e}")
        return None

class BaseGeometry():
    def __init__(self):
        pass

    def move(self):
        pass

    def initGeometry(self):
        pass

    def initializeTextures(self):
        pass

    def paintGL(self):
        error = gl.glGetError()
        if error != gl.GL_NO_ERROR:
            print("OpenGL error:", error)
    
class Image(BaseGeometry):
    def __init__(self, image_path=None, width=20, height=20, position=(0, 0, 0), cameraPosition=(0,0,-30), isIcon=False):
        super().__init__()
        self.width = width
        self.height = height
        self.position = position
        self.image_path = image_path 
        self.texture_id = None
        self.camera_position = cameraPosition
        self.isIcon = isIcon
        
        if self.image_path is not None:
            self.image = img.open(self.image_path)
            if self.image.mode != "RGBA":
                self.image = self.image.convert("RGBA")
            if not self.isIcon:
                self.width, self.height = self.resize_width_height(self.image.width, self.image.height)
            else:
                # Make it completely red while keeping the alpha channel
                # data = np.array(self.image)   # Convert image to numpy array
                # red, green, blue, alpha = data.T  # Transpose data to split each channel
                # data[..., :3] = [255, 0, 0]   # Set RGB values to red
                # self.image = img.fromarray(data)  # Convert back to an image
                pass

    def adjustedPosition(self):
        curPos = self.position
        curCam = self.camera_position
        newPos = (curCam[0]+curPos[0], curCam[1]+curPos[1], curCam[2]+curPos[2])
        return newPos

    def resize_width_height(self, w, h):
        newW = 20
        newH = 20
        if w > h:
            newW = 30
            newH = newW * (h / w)
        else:
            newH = 23
            newW = newH * (w / h)
        return newW, newH

    def initializeTextures(self):
        if self.image_path is not None:
            self.texture_id = self.load_texture(self.image_path)
        else:
            print('No image')

    def load_texture(self, image_path):
        # Open the image file
        transposedImage = self.image.transpose(img.FLIP_TOP_BOTTOM)

        image_data = transposedImage.tobytes("raw", "RGBA", 0, -1)
        
        # Generate a new texture ID
        texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
        
        # Upload the image data to the texture
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, transposedImage.width, transposedImage.height, 
                        0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image_data)
        
        # Set texture parameters
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        
        # Handle transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Set the transparency level for rendering
        transparency_level = 0.1
        gl.glColor4f(1.0, 1.0, 1.0, transparency_level)

        return texture_id

    def initGeometry(self):
        
        # Similar to Plane class but includes texture coordinates
        half_width = self.width / 2
        half_height = self.height / 2
        px, py, pz = self.adjustedPosition()
        
        # Vertex array for the plane with texture coordinates
        self.planeVtxArray = np.array([
            [px - half_width, py - half_height, pz, 0.0, 1.0],  # Bottom-left
            [px + half_width, py - half_height, pz, 1.0, 1.0],  # Bottom-right
            [px + half_width, py + half_height, pz, 1.0, 0.0],  # Top-right
            [px - half_width, py + half_height, pz, 0.0, 0.0],  # Top-left
        ])
        
        self.vertVBO = vbo.VBO(np.reshape(self.planeVtxArray, (1, -1)).astype(np.float32))
        self.vertVBO.bind()
        
        # Index array for the plane using triangles
        self.planeIdxArray = [0, 1, 2, 2, 3, 0]

    def paintGL(self):

        # Clear the depth buffer
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)

        # Enable depth testing
        gl.glEnable(gl.GL_DEPTH_TEST)
        
        # Render the textured quad
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)

        # Bind the VBO before setting the vertex and texture pointers
        self.vertVBO.bind()

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 20, self.vertVBO)  # 20 bytes stride (5 floats * 4 bytes)
        gl.glTexCoordPointer(2, gl.GL_FLOAT, 20, self.vertVBO + 12)  # 12 bytes offset (3 floats * 4 bytes)

        planeIdxArrayCtypes = (ctypes.c_uint * len(self.planeIdxArray))(*self.planeIdxArray)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glDrawElements(gl.GL_TRIANGLES, len(self.planeIdxArray), gl.GL_UNSIGNED_INT, planeIdxArrayCtypes)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)

        gl.glDisable(gl.GL_TEXTURE_2D)

    def setCameraPos(self, newPos):
        self.camera_position = newPos