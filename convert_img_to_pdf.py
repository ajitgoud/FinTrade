import os
import img2pdf

def generate_pdf(pdf_file, imgs_src):
    with open(pdf_file, "wb") as pdf:
        pdf.write(
            img2pdf.convert(
                [os.path.join(imgs_src, i) for i in os.listdir(imgs_src) if i.endswith(".png")])
            )