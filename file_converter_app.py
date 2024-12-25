from tkinter import Tk, Label, Button, Radiobutton, IntVar, filedialog, ttk, StringVar, Frame
from PIL import Image
import os

def load_images():
    global img_paths
    img_paths = filedialog.askopenfilenames(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    if img_paths:
        label_status.config(text=f"{len(img_paths)} images loaded.")

def compress_images():
    if not img_paths:
        label_status.config(text="Please load images first!")
        return

    
    quality_map = {1: 30, 2: 60, 3: 90}
    selected_quality = quality_map.get(quality_var.get(), 60)
    selected_format = format_var.get()

    output_dir = filedialog.askdirectory()
    if not output_dir:
        return

    try:
        progress_bar["maximum"] = len(img_paths)
        for idx, img_path in enumerate(img_paths, start=1):
            with Image.open(img_path) as img:
                # Generate output file path
                base_name, ext = os.path.splitext(os.path.basename(img_path))
                output_path = os.path.join(output_dir, f"{base_name}_compressed.{selected_format.lower()}")
                img.save(output_path, quality=selected_quality, format=selected_format, optimize=True)
            progress_bar["value"] = idx
            progress_bar.update_idletasks()
        label_status.config(text=f"Compression completed! Files saved in: {output_dir}")
    except Exception as e:
        label_status.config(text=f"Error: {e}")


app = Tk()
app.title("Image Compression App - Vaid")
app.geometry("600x400")

img_paths = []


Label(app, text="Batch Image Compression App", font=("Arial", 16)).pack(pady=10)

Button(app, text="Load Images", command=load_images).pack(pady=10)

Label(app, text="Select Compression Quality").pack(pady=5)


quality_var = IntVar(value=2)  
Radiobutton(app, text="Low", variable=quality_var, value=1).pack(anchor="w", padx=50)
Radiobutton(app, text="Medium", variable=quality_var, value=2).pack(anchor="w", padx=50)
Radiobutton(app, text="High", variable=quality_var, value=3).pack(anchor="w", padx=50)

Label(app, text="Select Output Format").pack(pady=5)


format_var = StringVar(value="JPG")  
Radiobutton(app, text="JPG", variable=format_var, value="JPG").pack(anchor="w", padx=50)
Radiobutton(app, text="PNG", variable=format_var, value="PNG").pack(anchor="w", padx=50)

Button(app, text="Compress and Save", command=compress_images).pack(pady=10)


progress_bar = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

label_status = Label(app, text="", wraplength=400, justify="center")
label_status.pack(pady=20)


app.mainloop()
