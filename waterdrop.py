from PIL import Image, ImageDraw
import glob, os, shutil, getopt, sys

'''
Just a quick watermarking utility.  It will watermark all the files in a src dir with the copyright symbol and the given
copyright text.  I am just going to center it across the top, which could be easily cropped out.  Honestly, you could argue this is a waste of time (cropping, image editing, etc), but it wasn\'t that hard to put in anyway :-)
'''


def waterdrop_file(copyright_text, src_file, debug=False):
    afile, ext = os.path.splitext(src_file)
    
    img = Image.open(src_file)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    text = "\xa9 %s" % (copyright_text)
    text_width, text_height = draw.textsize(text)
    center = width / 2
    # put the actual watermark on there
    position = (center - (text_width/2),10)


    draw.text(position, text)

    black = (255,255,255)

    #make the new image the same size as the old image, etc
    new_image = Image.new(img.mode, (width,height), black)
    new_image.paste( img, (0,0) )
    if debug:
        new_file_name = "%s_debug.jpg" % (afile)
    else:
        new_file_name = "%s_watermarked.jpg" % (afile)

    new_image.save(new_file_name, "JPEG")
    


def waterdrop_dir(copyright_text, src_dir):
    #XXX just does jpgs for now
    files = glob.glob(src_dir + "/*.jpg")
        
    for infile in files:
        waterdrop_file(copyright_text, infile)
    print "done"



class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])

            # argv[1] = copyright text
            # argv[2] = src dir
            waterdrop_dir(argv[1], argv[2])

        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
