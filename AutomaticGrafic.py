import pytesseract
from PIL import ImageGrab, Image
import cv2
import numpy as np
import pyautogui
import time
import tkinter as tk  # Importamos tkinter para crear la ventana gráfica

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\YOBER\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

full_region = (0, 0, 1920, 1080)
color = 'gray'  # Color inicial
KeyMaster = ['QmemuPL>y','Q™emu','QmMeEmMUPL>y','Qm™emu','QMeEmMUPL>Y','QMeEMUPLPY','QMemu','QMEMUPL>Y','QmemuPL>y','QmemuPLyy','QmwemupLyy','QmuemuPLyy','QMemMuPL>y','QMemMuPL>y']
KeyPrincipal = ['Tus', 'Ranuras', 'Minutos', 'Referidos', 'Adicionales', 'Por', 'Apoyar']
keySelect = []
keyReproduce = ['PLAN', 'MONEDAS', 'A', 'GANAR']
keyBack = ['HAS', 'OBTENIDO', 'UN', 'TOTAL', 'DE']

# Crear una ventana gráfica simple
def create_color_window():
    window = tk.Tk()
    window.title("Ventana de Color")
    window.geometry("300x300")
    
    # Función para actualizar el color de la ventana
    def update_color():
        window.configure(bg=color)  # Cambia el color del fondo de la ventana
        window.after(1000, update_color)  # Actualiza cada 1 segundo
    
    update_color()  # Llamada inicial
    window.mainloop()

# CAPTURAR TEXTO DE PANTALLA
def capture_and_analyze_region(region):
    screenshot = ImageGrab.grab(bbox=region)
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    screenshot_pil = Image.fromarray(cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB))
    detected_text_data = pytesseract.image_to_data(screenshot_pil, output_type=pytesseract.Output.DICT)    
    return detected_text_data

# Función para verificar si hay palabras clave
def check_for_key_words(detected_text_data, KeyMaster):
    detected_words = [word.lower() for word in detected_text_data['text'] if word.strip() != ""]
    for key in KeyMaster:
        if key.lower() in detected_words:
            return key
    return None

# DELIMITAR SECCIÓN DE PANTALLA
def delimit_screen(word_data, region, keyword):
    for i, word in enumerate(word_data['text']):
        if keyword.lower() in word.lower():
            x = word_data['left'][i] + region[0]
            y = word_data['top'][i] + region[1]
            width = word_data['width'][i]
            height = word_data['height'][i]
            
            print(f"Se detecto la pantalla correctamente")

            startX = max((x + width // 2) - 68, 0)
            starY = max((y + height // 2) - 15, 0)

            endX = startX + 585
            endY = starY + 1035
            screen_mobile = (startX,starY,endX,endY)
            detected_screen = detect__screen(screen_mobile,startX,starY,endX,endY)
            return detect__screen

def detect__screen(screen_mobile, x1, y1, x2, y2):
    detected = True
    contador = 0
    global color
    last_click_time = time.time()  # Registra el tiempo inicial
    while detected:
        detected_text_data = capture_and_analyze_region(screen_mobile)
        
        if all_key_words_present(detected_text_data, KeyPrincipal):  # Estás en pantalla principal
            print("Estamos en la pantalla principal")
            color = 'green'
            pyautogui.click(x1 + 200, y1 + 850)
            time.sleep(6)
            pyautogui.click(x1 + 250, y1 + 300)
        elif all_key_words_present(detected_text_data, keyReproduce):  # Estás en la pantalla de reproduciendo
            color = 'yellow'
        elif all_key_words_present(detected_text_data, keyBack):  # Estás en la pantalla de regresar atrás
            print("Estamos en la pantalla de regresar a menu principal")
            color = 'blue'
            pyautogui.click(x1 + 200, y1 + 1020)
        else:
            contador += 1
        if contador >= 100:
            color = 'red'
            detected = False 
            print("Se perdió la pantalla principal")
    return detected

def all_key_words_present(detected_text_data, KeyMaster):
    detected_words = [word.lower() for word in detected_text_data['text'] if word.strip() != ""]
    return all(key.lower() in detected_words for key in KeyMaster)

# Función principal
def main():
    # Lanza la ventana gráfica en un hilo separado
    import threading
    threading.Thread(target=create_color_window).start()

    while True:
        detected_text_data = capture_and_analyze_region(full_region)
        
        found_key = check_for_key_words(detected_text_data, KeyMaster)
        if found_key:
            delimit_screen(detected_text_data, full_region, found_key)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
