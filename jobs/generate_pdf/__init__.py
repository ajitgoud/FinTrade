import os
import img2pdf

def generate_pdf(reports_dir, pdf_name, imgs_dir, subs=None):
    if subs and isinstance(subs, list):
        for sub in subs:
            pdf_file = f'{sub}_{pdf_name}'.capitalize()
            pdf_file = os.path.join(reports_dir, pdf_file)
            imgs_src = os.path.join(imgs_dir, sub)
            imgs = os.listdir(imgs_src)
            if len(imgs) > 0:
                with open(pdf_file, "wb") as pdf:
                    pdf.write(
                        img2pdf.convert(
                            [os.path.join(imgs_src, i) for i in os.listdir(imgs_src) if i.endswith(".png")])
                        )

    else:
        pdf_file = f'{pdf_name}'.capitalize()
        pdf_file = os.path.join(reports_dir, pdf_file)
        imgs = os.listdir(imgs_dir)
        if len(imgs) > 0:
            with open(pdf_file, "wb") as pdf:
                pdf.write(
                    img2pdf.convert(
                        [os.path.join(imgs_dir, i) for i in os.listdir(imgs_dir) if i.endswith(".png")])
                )