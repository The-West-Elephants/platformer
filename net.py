# Import package
from OpenGL.GL import *


class Net:
    def __init__(self, x, y, width, height, image_index):
        # Define variables
        self.image_index = image_index
        self.rect = {"x": x, "y": y, "width": width, "height": height}

    def draw(self):
        # Draw net
        glBindTexture(GL_TEXTURE_2D, self.image_index)
        glEnable(GL_TEXTURE_2D)
        glTranslate(self.rect["x"], self.rect["y"], 0)
        glBegin(GL_QUAD_STRIP)
        glTexCoord2f(0, 1)
        glVertex2f(0, 0)
        glTexCoord2f(1, 1)
        glVertex2f(self.rect["width"], 0)
        glTexCoord2f(0, 0)
        glVertex2f(0, self.rect["height"])
        glTexCoord2f(1, 0)
        glVertex2f(self.rect["width"], self.rect["height"])
        glEnd()
        glTranslate(-self.rect["x"], -self.rect["y"], 0)
        glDisable(GL_TEXTURE_2D)
