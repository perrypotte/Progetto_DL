import os
import json

# Definizione delle dimensioni delle immagini
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

# Lista dei file JSON da elaborare
ALLOWED_JSON_FILES = {"r_test_coco.json", "r_val_coco.json", "r_train_coco.json", "train_coco.json", "val_coco.json"}

def convert_coco_to_yolo(json_dir, image_sets, output_dirs):
    """
    Converte le annotazioni in formato COCO in formato YOLO, solo per i JSON specificati.
    
    :param json_dir: Directory contenente i file JSON in formato COCO.
    :param image_sets: Dizionario con categorie (test, real, synth) e rispettive directory delle immagini.
    :param output_dirs: Dizionario con categorie (test, real, synth) e rispettive directory per le annotazioni YOLO.
    """
    # Creazione delle directory di output se non esistono
    os.makedirs(output_dirs["test"], exist_ok=True)
    os.makedirs(output_dirs["real"], exist_ok=True)
    os.makedirs(output_dirs["synth"], exist_ok=True)

    # Scansione dei file JSON nella directory
    for json_file in os.listdir(json_dir):
        if json_file not in ALLOWED_JSON_FILES:
            continue  # Ignora i file che non sono nella lista consentita
        
        json_path = os.path.join(json_dir, json_file)

        # Leggi il file JSON
        with open(json_path, "r") as f:
            data = json.load(f)

        # Verifica che il JSON abbia le chiavi necessarie
        if "images" not in data or "annotations" not in data:
            print(f"⚠️  Il file {json_file} non è in formato COCO valido. Skipping.")
            continue
        
        # Creazione di una mappatura ID immagine -> Nome file immagine
        image_id_to_name = {img["id"]: img["file_name"] for img in data["images"]}

        # Creazione di un dizionario per raccogliere le annotazioni per ogni immagine
        yolo_annotations = {img_name: [] for img_name in image_id_to_name.values()}

        # Elaborazione delle annotazioni
        for ann in data["annotations"]:
            image_id = ann["image_id"]
            category_id = ann["category_id"]  # ID della classe (deve essere già in YOLO format)

            # COCO usa [x_min, y_min, width, height]
            x_min, y_min, width, height = ann["bbox"]

            # Normalizzazione YOLO
            x_center = (x_min + width / 2) / IMAGE_WIDTH
            y_center = (y_min + height / 2) / IMAGE_HEIGHT
            norm_width = width / IMAGE_WIDTH
            norm_height = height / IMAGE_HEIGHT

            # Creazione della riga in formato YOLO
            yolo_line = f"{category_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}"
            
            # Aggiungi l'annotazione alla giusta immagine
            if image_id in image_id_to_name:
                img_name = image_id_to_name[image_id]
                yolo_annotations[img_name].append(yolo_line)

        # Salvataggio delle annotazioni nella directory corretta
        for img_name, annotations in yolo_annotations.items():
            # Determina dove salvare il file YOLO
            if img_name in os.listdir(image_sets["test"]):
                output_label_path = os.path.join(output_dirs["test"], os.path.splitext(img_name)[0] + ".txt")
            elif img_name in os.listdir(image_sets["real"]):
                output_label_path = os.path.join(output_dirs["real"], os.path.splitext(img_name)[0] + ".txt")
            elif img_name in os.listdir(image_sets["synth"]):
                output_label_path = os.path.join(output_dirs["synth"], os.path.splitext(img_name)[0] + ".txt")
            else:
                print(f"⚠️  Immagine {img_name} non trovata in nessuna directory. Skipping.")
                continue

            # Scrive il file YOLO
            with open(output_label_path, "w") as f:
                f.write("\n".join(annotations))

            print(f"✅ Salvata annotazione YOLO per {img_name} in {output_label_path}")

# Percorsi delle directory
annotations_directory = "annotations"  # Directory con i file JSON in formato COCO
image_sets = {
    "test": "test",   # Directory delle immagini test
    "real": "real",   # Directory delle immagini reali
    "synth": "synth"  # Directory delle immagini sintetiche
}
output_dirs = {
    "test": "testLabels",
    "real": "realLabels",
    "synth": "synthLabels"
}

# Esegui la conversione
convert_coco_to_yolo(annotations_directory, image_sets, output_dirs)
