from asyncio.windows_events import NULL
from PIL import Image
import os
from time import sleep
from colorama import Style, init, deinit
init()
ASCII_CHARS = list("@#S%?*+;:,.")

desired_width = 500

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


def terminalSize(width=50, height=20):
    # os.system('mode con: cols={} lines={}'.format(width, height))
    os.system('mode {}, {}'.format(width, height))

def terminalDefault(): #  returns to the default terminal size (kinda of, but not really, it's still a little weird and i cba)
    changeFontSize(16)
    terminalSize(70,30)

def changeFontSize(size=2): #Changes the font size to *size* pixels (kind of, but not really. You'll have to try it to chack if it works for your purpose ;) )
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

    font.dwFontSize.X = size
    font.dwFontSize.Y = size

    set_current_console_font_ex_func(stdout, False, byref(font))
    
    # kernel32 = WinDLL.kernel32
    # kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7) #  enables ansi characters



def list_Dir(path = 'CWD'):

    # print(colours.HEADER + " === Available files === \n === " + colours.ENDC + colours.OKGREEN + "")
    print(f"{colours.HEADER} === Available files === \n ==={colours.ENDC}{colours.OKGREEN} Green{colours.ENDC}{colours.HEADER} files are valid images ==={colours.ENDC}")

    if path == 'CWD':
        for file in os.listdir():
            if file.endswith(".jpg") or file.endswith(".png"):
                print(colours.OKGREEN + file + colours.ENDC)
            # if file.endswith(".jpg") or file.endswith(".png"):
            #     print(file)
            else:
                print(file)
    else:
        for file in os.listdir(path):
            if file.endswith(".jpg") or file.endswith(".png"):
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

def imageToAscii(new_width = desired_width):
    
    #  print(str(round(new_width * 0.5625)) + " AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    list_Dir()
    path = input("Path: ")

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

    changeFontSize(2)
    terminalSize(new_width, round(new_width * get_ratio(image)))
    

    print(ascii_image)

    with open("ascii_image_txt", 'w') as f:
        f.write(ascii_image)


# def imgFolderToAscii(new_width = desired_width)::

imageToAscii()

input()
terminalDefault()