from PIL import Image
import sys



def fixedColor(im, (x, y), r=1):
    colorTotal = 0
    for i in range(-r, r + 1):
        for j in range(-r, r + 1):
            colorTotal = colorTotal + sum(im.getpixel((x + i, y + j)))
    return float(colorTotal) / (2 * r + 1) / (2 * r + 1) / 3

def blackpointCount(im, x, height):
    black = 0
    for j in range(height):
        color = sum(im.getpixel((x, j)))
        if(color == 0):
            black = black + 1
    return black

def cutImage(im,width,height):
    xpoint = []
    bottom = 33  # end postion from top
    top = 10  # start postion of top
    imageList = []
    for i in range(width - 1):
            if(blackpointCount(im, i, height) < 3 and blackpointCount(im, i + 1, height) >= 3):
                xpoint.append(i)
            if(blackpointCount(im, i, height) >= 3 and blackpointCount(im, i + 1, height) < 3):
                xpoint.append(i + 1)
    
    for i in range(5):
        right = xpoint.pop()
        left = xpoint.pop()
        im_letter = im.crop((left, top, right, bottom))
        imageList.append(im_letter)
      #  im_letter.save(r"D:\codelib\letter"+str(i)+".jpg", "jpeg")
    imageList.reverse()
    return imageList

def recogImage(imList, imageMap):
    symbolList = []
    for im in imList:
        maxSim = 0
        for key in imageMap:
            keyImage=Image.open(imageMap[key]).convert("RGB")
            sim = similarity(im, keyImage)
            if sim > maxSim:
                maxSim = sim
                symbol = key
        symbolList.append(symbol)
    return symbolList

def similarity(image1, image2):
    (width, height) = image2.size
    image1=image1.resize((width, height))
    matchDots = 0
    for i in range(width):
        for j in range(height):
            colorpoint= (sum(image1.getpixel((i, j)))+sum(image2.getpixel((i, j))))/6
            if colorpoint>=200 or colorpoint <=20:
                matchDots = matchDots + 1
    return float(matchDots) / width / height
            
def getImageMap(path):
    imageMap = {'0':'', '2':'', '4':'', '6':'', '8':'', 'B':'', 'D':'', 
               'F':'', 'H':'', 'J':'', 'L':'', 'N':'', 'P':'', 'R':'', 
               'T':'', 'V':'', 'X':'', 'Z':''}
    for key in imageMap:
        imageMap[key]=path+"\\"+key+".jpg"
    return imageMap


def crack(validateImage,libPath):
    """
    Main
    """
    width = 126
    height = 44
    im = validateImage.resize((width, height))
    im = im.convert('RGB')
   # im.show()
    im_transform = Image.new("RGB", (width, height), (255, 255, 255))
    
    ratio = 5
    for i in range(int(height / ratio) + 2, width):
        for j in range(height):
            im_transform.putpixel((i, j), im.getpixel((i - j / ratio, j)))
    # im_transform.show()
    
    im_new = Image.new("RGB", (width, height), (255, 255, 255))
    for i in range(3, width - 3):
        for j in range(3, height - 3):
            if fixedColor(im_transform, (i, j), 2) < 140:
                im_new.putpixel((i, j), (0, 0, 0))
    
    letters=cutImage(im_new,width,height)
    imageMap=getImageMap(libPath)
    symbolList=recogImage(letters,imageMap)
    return symbolList


