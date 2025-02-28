import tkinter as tk #Questo modulo è ottenibile solo attraverso l'installer di python!!!
from tkinter import filedialog, messagebox, font
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, ImageDraw, ImageFont
from ultralytics import YOLO
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv(override=True) 

def open_inferenza_yolo_window():
    inferenza_window = tk.Toplevel(root)
    inferenza_window.title("Yolo - Predict")
    inferenza_window.geometry("600x400")  # Imposta la dimensione della finestra
    inferenza_window.resizable(True, True)  # Disabilita il ridimensionamento

    # Definisci un font con il testo in grassetto e dimensione maggiore
    bold_font = font.Font(family="Helvetica", size=16, weight="bold")

    # Nasconde la finestra principale
    root.withdraw()

    # Frame per le immagini
    image_frame = tk.Frame(inferenza_window)
    image_frame.pack(pady=20)

    if selected_model.get()==1:
    # Load a pretrained YOLO model
        model = YOLO(os.getenv("PATH_YOLO_REAL"))
    elif selected_model.get()==2:
        model = YOLO(os.getenv("PATH_YOLO_SYNTH"))  
    elif selected_model.get()==3:
        model = YOLO(os.getenv("PATH_YOLO_MIXED25"))  
    elif selected_model.get()==4:
        model = YOLO(os.getenv("PATH_YOLO_MIXED50"))
    elif selected_model.get()==5:
        model = YOLO(os.getenv("PATH_YOLO_MIXED25_DA"))
    elif selected_model.get()==6:
        model = YOLO(os.getenv("PATH_YOLO_MIXED25_DA_V2"))
    # Specifica il percorso iniziale dove cercare l'input
    initial_directory = os.getenv("PATH_DEMO_TEST_IMAGES")

    # Mappatura tra class id e class name
    class_name_mapping = {
    0: "power_supply",
    1: "oscilloscope",
    2: "welder station",
    3: "electric screwdriver",
    4: "screwdriver",
    5: "pliers",
    6: "welder probe tip",
    7: "oscilloscope probe tip",
    8: "low voltage board",
    9: "high voltage board",
    10: "register",
    11: "electric screwdriver battery",
    12: "working area",
    13: "welder base",
    14: "socket",
    15: "left red button",
    16: "left green button",
    17: "right red button",
    18: "right green button",
    19: "hand",
}

    os.makedirs("tmp", exist_ok=True)

    def on_closing():
        # Mostra di nuovo la finestra principale quando si chiude la finestra di inferenza
        root.deiconify()
        inferenza_window.destroy()

    def read_yolo_labels(label_file, img_width, img_height):
        if not os.path.exists(label_file):
            print(label_file)
            messagebox.showerror("Attenzione", "Labels non trovate.\nImpossibile disegnare i bounding box!\nVisualizzo l'immagine originale")
            boxes = None
            lines = None
            return boxes, lines
        
        with open(label_file, 'r') as f:
            lines = f.readlines()
        
        # Converte le linee in liste di float (coordinate YOLO)
        boxes = []
        for line in lines:
            data = line.strip().split()
            class_id = int(data[0])
            x_center = float(data[1])
            y_center = float(data[2])
            width = float(data[3])
            height = float(data[4])
            
            # Calcola le coordinate del rettangolo (x1, y1, x2, y2)
            x1 = int((x_center - width / 2) * img_width)
            y1 = int((y_center - height / 2) * img_height)
            x2 = int((x_center + width / 2) * img_width)
            y2 = int((y_center + height / 2) * img_height)
            
            boxes.append((class_id, x1, y1, x2, y2))
        
        return boxes, lines

    def draw_boxes_on_image(image_path, boxes):
        img = Image.open(image_path)
        
        class_colors = {
            0: (6, 41, 255),      
            1: (27, 210, 228),    
            2: (247, 240, 247),  
            3: (16, 212, 176),   
            4: (15, 32, 102),    
            5: (255, 110, 222),   
            6: (255, 63, 69),    
            7: (203, 232, 2),    
            8: (255, 165, 0),    
            9: (128, 0, 128),    
            10: (0, 255, 127),    
            11: (139, 69, 19),   
            12: (255, 255, 0),   
            13: (255, 20, 147),  
            14: (70, 130, 180),   
            15: (0, 191, 255),    
            16: (34, 139, 34),   
            17: (255, 0, 0),      
            18: (0, 255, 0),      
            19: (178, 34, 34),    
        }

        
        # Disegna i rettangoli e scrivi il nome della classe sull'immagine
        draw = ImageDraw.Draw(img)
        for box in boxes:
            class_id, x1, y1, x2, y2 = box
            
            # Ottiene il colore per la classe corrente
            if class_id in class_colors:
                color = class_colors[class_id]
            # else:
            #     color = (0, 0, 0)  # Colore nero per classi non definite
            
            # Disegna il rettangolo con il colore specifico
            draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
            
            class_name = class_name_mapping[class_id]
            print(class_name)

            # Scrive il nome della classe all'interno del rettangolo
            draw.text((x1, y1), class_name, fill=(255, 255, 255), font=ImageFont.truetype("arial.ttf", size=25))
        
        return img
    

    def pick_file( file_path ):
        if not file_path:
            return
        
        # Ottieni il nome dell'immagine dall'intero percorso
        filename_without_extension = os.path.splitext(os.path.basename(file_path))[0]
        img = Image.open(file_path)
        boxes, lines = read_yolo_labels(os.getenv("PATH_DEMO_TEST_LABELS") + "/" + filename_without_extension + ".txt", img.width, img.height)
        if boxes is not None:
            img = draw_boxes_on_image(file_path, boxes)
            coin_count_label_gt.config(text="Immagine originale", font=bold_font)
        img = img.resize((640, 640))
        img = ImageTk.PhotoImage(img)
        selected_image_label.config(image=img)
        selected_image_label.image = img
        selected_image_label.file_path = file_path
        # Regola la dimensione della finestra principale in base alle dimensioni dell'immagine
        result = model(file_path)[0]  # predict on an image
        result.save("tmp/predict.png")
        # Convert the array to an image ensuring the RGB format is maintained
        result_img = Image.open("tmp/predict.png")
        result_img = result_img.resize((640, 640))

        result_img = ImageTk.PhotoImage(result_img)
        result_image_label.config(image=result_img)
        result_image_label.image = result_img

        coin_count_label.config(text="Immagine predetta", font=bold_font)
        inferenza_window.update_idletasks()  # Aggiorna il layout prima di ottenere le dimensioni della finestra
        inferenza_window.geometry(f"{(640 + 50) * 2}x{(640 + 150)}")  # Adatta le dimensioni della finestra


    def dnd_callback( file_path ): 
        pick_file( file_path.strip('{}') )

    def select_button_callback():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")], initialdir=initial_directory)
        pick_file( file_path )
        

    def drop(event):
        file_path = event.data
        if file_path:
            dnd_callback(file_path)

    select_button = tk.Button(inferenza_window, text="Seleziona immagine di test", command=select_button_callback)
    select_button.pack()

    drop_label = tk.Label(inferenza_window, text="O trascina l'immagine in questo box", width=40, height=10, bg="lightgrey")
    drop_label.pack()
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind('<<Drop>>', drop)

    selected_image_label = tk.Label(image_frame)
    selected_image_label.grid(row=0, column=0, padx=10)

    result_image_label = tk.Label(image_frame)
    result_image_label.grid(row=0, column=1, padx=10)

    # Label for coin count
    coin_count_label = tk.Label(image_frame, text="")
    coin_count_label.grid(row=1, column=1, padx=10)

    # Label for ground truth coin count
    coin_count_label_gt = tk.Label(image_frame, text="")
    coin_count_label_gt.grid(row=1, column=0, padx=10)

    # Aggiungi un evento per riportare la finestra principale alla visibilità quando si chiude la finestra di inferenza
    inferenza_window.protocol("WM_DELETE_WINDOW", on_closing)


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


root = TkinterDnD.Tk()
root.title("Menu Principale")
root.geometry("400x300")  # Imposta la dimensione della finestra principale
root.resizable(False, False)  # Disabilita il ridimensionamento

# Centra la finestra principale nello schermo
center_window(root)

inferenza_yolo_button = tk.Button(root, text="Inferenza con yolo", command=open_inferenza_yolo_window)
inferenza_yolo_button.pack(pady=20)

# Variabile per il modello selezionato
selected_model = tk.IntVar() #select_model.get() da il valore della radio
selected_model.set(1)  # Seleziona di default il primo modello

# Creazione dei radio button per la selezione del modello
tk.Frame(root).pack(pady=10)  # Spazio superiore per migliorare il layout
radio_frame = tk.Frame(root)
radio_frame.pack()

tk.Radiobutton(radio_frame, text=f"Modello allenato su dati reali", variable=selected_model, value=1).pack(anchor="center", pady=2)
tk.Radiobutton(radio_frame, text=f"Modello allenato su dati sintetici", variable=selected_model, value=2).pack(anchor="center", pady=2)
tk.Radiobutton(radio_frame, text=f"Modello allenato su dati misti (100% sint. + 25% real.)", variable=selected_model, value=3).pack(anchor="center", pady=2)
tk.Radiobutton(radio_frame, text=f"Modello allenato su dati misti (100% sint. + 50% real)", variable=selected_model, value=4).pack(anchor="center", pady=2)
tk.Radiobutton(radio_frame, text=f"Modello allenato su dati misti (100% sint. + 25% real. + CycleGAN)", variable=selected_model, value=5).pack(anchor="center", pady=2)
tk.Radiobutton(radio_frame, text=f"Modello allenato su dati misti (100% sint. + 25% real. + CycleGAN V2)", variable=selected_model, value=6).pack(anchor="center", pady=2)

root.mainloop()
