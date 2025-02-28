import os
import shutil
import random

def create_cycle_gan_dataset(real_images_dir, synth_images_dir, output_dir):
    """
    Crea un dataset per CycleGAN con due cartelle: trainA (synth) e trainB (real).
    
    :param real_images_dir: Directory contenente tutte le immagini reali.
    :param synth_images_dir: Directory contenente tutte le immagini sintetiche.
    :param output_dir: Directory principale in cui verrà creato il dataset.
    """

    # Definizione delle cartelle di output
    trainA_dir = os.path.join(output_dir, "trainA")  # Synthetic images
    trainB_dir = os.path.join(output_dir, "trainB")  # Real images

    # Creazione delle directory
    os.makedirs(trainA_dir, exist_ok=True)
    os.makedirs(trainB_dir, exist_ok=True)

    # Lista delle immagini reali e sintetiche
    real_images = [img for img in os.listdir(real_images_dir) if img.endswith((".jpg", ".png", ".jpeg"))]
    synth_images = [img for img in os.listdir(synth_images_dir) if img.endswith((".jpg", ".png", ".jpeg"))]

    # Seleziona casualmente lo stesso numero di immagini sintetiche delle reali
    selected_synth_images = random.sample(synth_images, len(real_images))

    def copy_images(images_list, src_dir, dst_dir):
        """Copia le immagini dalla sorgente alla destinazione."""
        for img_file in images_list:
            shutil.copy(os.path.join(src_dir, img_file), os.path.join(dst_dir, img_file))

    # Copia le immagini reali in trainB
    copy_images(real_images, real_images_dir, trainB_dir)

    # Copia le immagini sintetiche selezionate in trainA
    copy_images(selected_synth_images, synth_images_dir, trainA_dir)

    print(f"✅ Copiate {len(real_images)} immagini reali in trainB")
    print(f"✅ Copiate {len(selected_synth_images)} immagini sintetiche in trainA")
    print(f"✅ Dataset CycleGAN creato in '{output_dir}'")

# Esegui la funzione
real_images_dir = "real"
synth_images_dir = "synth"
output_dir = "datasets/cycleDataset"

create_cycle_gan_dataset(real_images_dir, synth_images_dir, output_dir)
