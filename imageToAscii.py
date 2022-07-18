from asyncio.windows_events import NULL
from PIL import Image
from sys import argv
import os
import cv2
from colorama import init, deinit, reinit, Fore
from keyboard import is_pressed
from datetime import datetime
init()
# ASCII_CHARS = list("@#S%?*+;:,.")
ASCII_CHARS = list(".,:;+*?%S$@")
f = NULL
try:
    desired_width = int(argv[1])
except:
    print("No width specified. Using default width of 300")
    desired_width = 300

try:
    if str(argv[2]) == "-o":
        output_file = str(argv[3])
        noPrint = False
    elif str(argv[2]) == "-oN":
        output_file = str(argv[2])
        noPrint = True
    else:
        noPrint = False
        
except:
    print("No output file specified. Printing to console")
    noPrint = False

webcam_width = 300
class colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[208m'


def terminalSize(width=50, height=20):
    # os.system('mode con: cols={} lines={}'.format(width, height))
    os.system('mode {}, {}'.format(width, height))

def terminalDefault(): #  returns to the default terminal size (kinda of, but not really, it's still a little weird and i cba)
    changeFontSize(8,16)
    terminalSize(120,30)

def changeFontSize(xSize = 2, ySize = 2): #Changes the font size to *size* pixels (kind of, but not really. You'll have to try it to chack if it works for your purpose ;) )
    from ctypes import POINTER, WinDLL, Structure, sizeof, byref
    from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(Structure):
        _fields_ = [
            ("X", SHORT),
            ("Y", SHORT),
        ]

    class CONSOLE_FONT_INFOEX(Structure):
        _fields_ = [
            ("cbSize", ULONG),
            ("nFont", DWORD),
            ("dwFontSize", COORD),
            ("FontFamily", UINT),
            ("FontWeight", UINT),
            ("FaceName", WCHAR * LF_FACESIZE)
        ]

    kernel32_dll = WinDLL("kernel32.dll")

    get_last_error_func = kernel32_dll.GetLastError
    get_last_error_func.argtypes = []
    get_last_error_func.restype = DWORD

    get_std_handle_func = kernel32_dll.GetStdHandle
    get_std_handle_func.argtypes = [DWORD]
    get_std_handle_func.restype = HANDLE

    get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
    get_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
    get_current_console_font_ex_func.restype = BOOL

    set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
    set_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
    set_current_console_font_ex_func.restype = BOOL

    stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = sizeof(CONSOLE_FONT_INFOEX)

    font.dwFontSize.X = xSize
    font.dwFontSize.Y = ySize

    set_current_console_font_ex_func(stdout, False, byref(font))
    
    # kernel32 = WinDLL.kernel32
    # kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) #  enables ansi characters



def list_Dir(path = 'CWD', filetypes = ['.jpg', '.png']):

    # print(colours.HEADER + " === Available files === \n === " + colours.ENDC + colours.OKGREEN + "")
    print(f"{colours.HEADER} === Available files === \n ==={colours.ENDC}{colours.OKGREEN} Green{colours.ENDC}{colours.HEADER} files are valid images ==={colours.ENDC}")

    if path == 'CWD':
        for file in os.listdir():
            # if file.endswith(".jpg") or file.endswith(".png"):
            for filetype in filetypes:
                if file.endswith(filetype):
                    print(colours.OKGREEN + file + colours.ENDC)
                    break
            # if file.endswith(".jpg") or file.endswith(".png"):
            #     print(file)
            else:
                print(file)
    else:
        for file in os.listdir(path):
            for filetype in filetypes:
                if file.endswith(filetype):
                    print(colours.OKGREEN + file + colours.ENDC)
                    break
            # if file.endswith(".jpg") or file.endswith(".png"):
            #     print(file)
            else:
                print(file)
                
def resize_image(image, new_width=desired_width):
    width, height = image.size
    ratio = height/width
    print(f"{colours.OKBLUE} ratio = {ratio} {colours.ENDC}")
    new_height = int(new_width * ratio)
    newsize = (new_width, new_height)
    resized_image = image.resize(newsize)
    return(resized_image)

def get_ratio(image):
    width, height = image.size
    ratio = height/width
    return(ratio)

def greyify(image):
    grayscale_image = image.convert("L")
    return(grayscale_image)


def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return(characters)

def imageToAscii(path, new_width = desired_width, Print = True, output_file = NULL):
    
    #  print(str(round(new_width * 0.5625)) + " AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    # list_Dir()
    # path = input("Path: ")

    imageOpened = False
    while not imageOpened:
        try:
            image = Image.open(path)
            imageOpened = True
        except:
            print(f"couldn't open {path}")
            path = input("Path: ")

    deinit()

    new_image_data = pixels_to_ascii(greyify(resize_image(image)))   
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))

    if Print:
        changeFontSize(2)
        terminalSize(new_width, round(new_width * get_ratio(image)))
        print(ascii_image)
        
    if output_file != NULL:
        with open(output_file, "a") as f:
            f.write(ascii_image + "\n|\n")
    
    terminalDefault()   

def findFps(video):
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
        
    return(fps)

def videoToAscii(path, new_width = desired_width, Print = True, output_file = NULL):


    videoOpened = False
    while not videoOpened:
        try:
            video = cv2.VideoCapture(path)
            videoOpened = True
        except:
            print(f"couldn't open {path}")
            path = input("Path: ")

    success, cv2image = video.read()
    image = Image.fromarray(cv2image)
    
    count = 0
    if Print:
        changeFontSize(2)
        terminalSize(new_width, round(new_width * get_ratio(image)))
        deinit()
    
    if output_file != NULL:
        f = open(output_file, 'w')
    
    
    time1 = datetime.now()
    
    while success and not is_pressed('enter'):
        success, cv2image = video.read()
        if success:
            image = Image.fromarray(cv2image)
        else: 
            break
        
        # print("Read a new frame: " + str(success) + ", " + str(count))
        print(f"Read a new frame: {success}, {count}")
        
        new_image_data = pixels_to_ascii(greyify(resize_image(image)))   
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))
        
        if Print:
            print(ascii_image)
        
        if output_file != NULL:
            f.write(ascii_image + "\n|\n")
            
        count += 1

    time2 = datetime.now()
    elapsedTime = time2 - time1
    if Print:
        terminalDefault()
    reinit()
    print(f"Average of {colours.OKCYAN}{count/elapsedTime.total_seconds()}{colours.ENDC}fps over {colours.OKCYAN}{divmod(elapsedTime.total_seconds(), 60)[0]}{colours.ENDC} minutes and {colours.OKCYAN}{divmod(elapsedTime.total_seconds(), 60)[1]}{colours.ENDC} seconds")
    # os.mkdir("frames")
    
def webcamToAscii(new_width = webcam_width):
    cap = cv2.VideoCapture(0)
    success, cv2image = cap.read()
    image = Image.fromarray(cv2image).transpose(Image.FLIP_LEFT_RIGHT)
    with open("log.txt", 'w') as log:
        print(round(get_ratio(image)), file=log)
    count = 0
    changeFontSize(2)
    terminalSize(new_width, round(new_width * get_ratio(image)))
    deinit()
    
    time1 = datetime.now()
    
    while success and not is_pressed('enter'):
        success, cv2image = cap.read()
        if success:
            image = Image.fromarray(cv2image).transpose(Image.FLIP_LEFT_RIGHT)
        else: 
            break
        
        print("Read a new frame: " + str(success))
        
        new_image_data = pixels_to_ascii(greyify(resize_image(image, webcam_width)))   
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))
        
        print(ascii_image)
        count += 1

    time2 = datetime.now()
    elapsedTime = time2 - time1
    terminalDefault()
    reinit()
    print(f"Average of {colours.OKCYAN}{count/elapsedTime.total_seconds()}{colours.ENDC}fps over {colours.OKCYAN}{divmod(elapsedTime.total_seconds(), 60)[0]}{colours.ENDC} minutes and {colours.OKCYAN}{divmod(elapsedTime.total_seconds(), 60)[1]}{colours.ENDC} seconds")
    # os.mkdir("frames")
    
def main():
    print("main function called")
    prompt = f"1) {Fore.YELLOW}image to ascii{colours.ENDC}\n2) {Fore.YELLOW}video to ascii {colours.ENDC} \n3) {Fore.YELLOW}webcam to ascii {colours.ENDC}\n{colours.HEADER}=>{colours.ENDC}"
    print(prompt, end="")
    textIn = input()
    # textIn = input(prompt)
    
    if textIn == "1":
        list_Dir()
        path = input("Path: ")
        imageToAscii(path,desired_width,True,NULL)
        
    elif textIn == "2":
        list_Dir('CWD', ['mp4'])
        path = input("Path: ")
        
        videoToAscii(path, desired_width, True, NULL)

    elif textIn == "3":
        webcamToAscii()
        
if __name__ == "__main__":      
    main()
    input()
