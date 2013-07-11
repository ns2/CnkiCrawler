
import cracker
from PIL import Image
img=Image.open('C:/codeimg/C4.gif')
symbols=cracker.crack(img, './codelib')
print symbols