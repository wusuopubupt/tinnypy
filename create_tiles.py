#!/usr/bin/env python

"""
@author : wdxbupt2009@gmail.com
@date   : 2014-09-23
@desc   : Creating tiles from an image with PIL

"""

from PIL import Image
import Image

def check_alpha(raw_image):
    image = raw_image.resize((8, 8), Image.ANTIALIAS).convert('RGBA')
    #image = raw_image.convert('RGBA')
    pixel_data = image.load()
    for y in xrange(image.size[1]): 
        for x in xrange(image.size[0]): 
            print("R:%s, G:%s, B:%s, A:%s\n" % (pixel_data[x,y][0], pixel_data[x,y][1], pixel_data[x,y][2], pixel_data[x,y][3]))
            if pixel_data[x, y][3] > 1:
                return True
    return False            

def create_tiles(path, filename, tile_width, tile_height):
    image = Image.open(path+filename)
    img_width, img_height = image.size
    print("\nimage width: %s, image height:%s\n" % (img_width, img_height))

    #clear data
    #open('filename.txt', 'w').close  
    #f = open('filename.txt','a')

    f = open('filename.txt','w')
    
    if img_width % tile_width == 0 and img_height % tile_height == 0 :
        currentx, currenty = 0, 0
        saved_blank_img = False
        i = 0

        while currenty < img_height:
            while currentx < img_width:
                print currentx,",",currenty

                tile = image.crop((currentx,currenty,currentx + tile_width, currenty + tile_height))
                if check_alpha(tile):
                    #name = "x_%s_y_%s.png" % (currentx, currenty)
                    name = "%s" % i
                    tile.save("%s.png" % name, "PNG")
                else:
                    name = "1"
                    if not saved_blank_img:
                        tile.save("1.png", "PNG")
                        saved_blank_img = True

                currentx += tile_width
                i = i+1

                if currentx < img_width:
                    f.write(name + ',') 
                else:
                    f.write(name + '\n')

            #end while    
            currenty += tile_height
            currentx = 0
    else:
        print ("sorry your image does not fit neatly into", tile_width,"*",tile_height,"tiles")

    if f:
        f.close() 

def main():
    tile_width = 100
    tile_height = 100
    path = "./"
    filename = "map.PNG"

    create_tiles(path, filename, tile_width, tile_height);


if __name__=='__main__':
    main() 
