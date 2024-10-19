import pytesseract
from PIL import ImageGrab, Image
import cv2
import numpy as np
import pyautogui
import time
import re
import pygetwindow as gw


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\YOBER\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

color = 'gray'
KeyMaster = ['QmemuPL>y','Q™emu','QmMeEmMUPL>y','Qm™emu','QMeEmMUPL>Y','QMeEMUPLPY','QMemu','QMEMUPL>Y','QmemuPL>y','QmemuPLyy','QmwemupLyy','QmuemuPLyy','QMemMuPL>y','QMemMuPL>y']
KeyPrincipal = ['Usuarios','en','linea']
keySelect = ['MONEDAS','A','GANAR','Puntos','para','el','Ranking:']
keyReproduce = ['PLAN','MONEDAS','A','GANAR','SEGUNDOS']
keyBack = ['HAS','OBTENIDO','UN','TOTAL','DE']


def get_window_coordinates(window_title):
    windows = gw.getAllTitles()
    for window in windows:
        if window_title in window:
            win = gw.getWindowsWithTitle(window)[0]
            left, top, right, bottom = win.left, win.top, win.right, win.bottom
            return (left, top, right, bottom)
    return None

#CAPTURAR TEXTO DE PANTALLA
def capture_and_analyze_region(region):
    screenshot = ImageGrab.grab(bbox=region)
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    screenshot_pil = Image.fromarray(cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB))
    detected_text_data = pytesseract.image_to_data(screenshot_pil, output_type=pytesseract.Output.DICT)
    return detected_text_data

#FUNCION PARA DETECTAR NUMERO COMO POR EJEMPLO +12 +11 +15 +9
def extract_values_with_plus(detected_text_data):
    numeric_values = []

    for i, word in enumerate(detected_text_data['text']):
        match = re.match(r'\+(\d+)', word)
        if match:
            numeric_values.append(int(match.group(1)))
    
    if not numeric_values:
        return ''

    return '+' + str(max(numeric_values))


#DELIMITAR SECCION DE PANTALLA
def click_in_keyword(word_data, region, keyword):
    for i, word in enumerate(word_data['text']):
        if keyword.lower() in word.lower():
            x = word_data['left'][i] + region[0]
            y = word_data['top'][i] + region[1]
            width = word_data['width'][i]
            height = word_data['height'][i]
            return x + width // 2, y + height // 2
            

def detect__screen(screen_mobile,x1,y1,x2,y2):
    detected = True
    contador = 0
    global color
    while detected:
        detected_text_data = capture_and_analyze_region(screen_mobile)
        if all_key_words_present(detected_text_data, KeyPrincipal):#estas en pantalla principal
            print("Estamos en la pantalla principal")
            color = 'green'
            pyautogui.click(x1 + 200,y1 + 880)
            #time.sleep(6)
            #pyautogui.click(x1 + 250,y1 + 300)
        elif all_key_words_present(detected_text_data, keySelect):#esta en selecionar video
            print("Etrando a selecionar video")
            maximo = extract_values_with_plus(detected_text_data)
            x,y = click_in_keyword(detected_text_data,screen_mobile,maximo)
            pyautogui.click(x,y)
            time.sleep(5)
            pyautogui.click(x1 + 280, y1 + 280)
            print("Video elejido")
        elif all_key_words_present(detected_text_data, keyReproduce):#estas en la pantalla de reproduciendo
            color = 'yellow'
        elif all_key_words_present(detected_text_data, keyBack):#estas en la pantalla de regresar atras
            print("Estamos en la pantalla de regresar a menu principal")
            color = 'blue'
            pyautogui.click(x1 + 282,y1 + 1000)
        else:
            contador += 1
            print("pantalla desconocida")
        if contador >= 100:
            color = 'red'
            detected = False 
            print("Se perdio la pantalla principal")
    return detected


def all_key_words_present(detected_text_data, KeyMaster):
    # Extraemos las palabras detectadas por el OCR
    detected_words = [word.lower() for word in detected_text_data['text'] if word.strip() != ""]
    
    # Verificamos si todas las palabras clave están presentes
    return all(key.lower() in detected_words for key in KeyMaster)

def main():
    while True:

        coordinates = get_window_coordinates("MEmu")
        if coordinates:
            startX, startY, endX, endY = coordinates
            screen_mobile = (startX,startY + 500,endX,endY)
            detect__screen(screen_mobile,startX,startY,endX,endY)
        #time.sleep(50)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




