from PIL import Image
from pix2tex.cli import LatexOCR
from IPython.display import display, Latex
from pylatexenc.latex2text import LatexNodes2Text

file = "num6.png"
img = Image.open(file)

#Convert Image to latex
model = LatexOCR()
a = model(img)

a = "$"+a+"$"

#Convert Latex to Text
print(LatexNodes2Text().latex_to_text(a))