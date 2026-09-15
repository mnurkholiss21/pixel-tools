"""Simple desktop image pixelator built with Tkinter and Pillow."""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageEnhance, ImageOps, ImageTk


SUPPORTED_FILETYPES = [
    ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"),
    ("All files", "*.*"),
]


def pixelate_image(input_path, pixel_size=10, color_mode="Original", color_count=16):
    """Return a pixelated copy of an image without changing the source file."""
    if pixel_size < 1:
        raise ValueError("Pixel size must be at least 1.")

    image = ImageOps.exif_transpose(Image.open(input_path))
    image.load()

    if color_mode == "Grayscale":
        image = ImageOps.grayscale(image).convert("RGB")
    elif color_mode == "Vivid":
        image = ImageEnhance.Color(image.convert("RGB")).enhance(1.8)
    elif color_mode == "Game Boy":
        image = ImageOps.grayscale(image).convert("RGB").quantize(
            colors=4, method=Image.Quantize.MEDIANCUT
        ).convert("RGB")
    elif image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "transparency" in image.info else "RGB")

    width, height = image.size
    small_size = (max(1, width // pixel_size), max(1, height // pixel_size))
    small_image = image.resize(small_size, Image.Resampling.BILINEAR)

    if color_mode == "Limited colors":
        small_image = small_image.convert("RGB").quantize(
            colors=max(2, min(256, color_count)), method=Image.Quantize.MEDIANCUT
        ).convert("RGB")

    return small_image.resize((width, height), Image.Resampling.NEAREST)


class PixelConverterApp:
    """Tkinter interface for choosing, previewing, and saving pixel art."""

    def __init__(self, root):
        self.root = root
        self.root.title("PixelTools - Image Pixelator")
        self.root.geometry("980x720")
        self.root.minsize(760, 560)
        self.root.configure(bg="#202124")

        self.original_image = None
        self.original_path = ""
        self.result_image = None
        self.preview_reference = None
        self.status = tk.StringVar(value="Choose an image to get started.")
        self.pixel_size = tk.IntVar(value=12)
        self.color_mode = tk.StringVar(value="Original")
        self.color_count = tk.IntVar(value=16)

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#202124")
        header.pack(fill="x", padx=24, pady=(20, 8))
        tk.Label(
            header,
            text="PixelTools",
            font=("Segoe UI", 24, "bold"),
            fg="#f1f3f4",
            bg="#202124",
        ).pack(side="left")
        tk.Button(
            header,
            text="Open image",
            command=self.open_image,
            font=("Segoe UI", 10, "bold"),
            bg="#8ab4f8",
            fg="#202124",
            relief="flat",
            padx=14,
            pady=7,
            cursor="hand2",
        ).pack(side="right")

        controls = tk.Frame(self.root, bg="#292a2d")
        controls.pack(fill="x", padx=24, pady=8)
        controls.columnconfigure(1, weight=1)

        tk.Label(controls, text="Pixel size", fg="#e8eaed", bg="#292a2d").grid(
            row=0, column=0, padx=(16, 8), pady=14, sticky="w"
        )
        tk.Scale(
            controls,
            from_=1,
            to=100,
            orient="horizontal",
            variable=self.pixel_size,
            command=lambda _value: self.update_preview(),
            showvalue=True,
            bg="#292a2d",
            fg="#e8eaed",
            highlightthickness=0,
            troughcolor="#55575c",
            activebackground="#8ab4f8",
        ).grid(row=0, column=1, padx=8, sticky="ew")

        tk.Label(controls, text="Color mode", fg="#e8eaed", bg="#292a2d").grid(
            row=0, column=2, padx=(16, 8), sticky="w"
        )
        mode_menu = ttk.Combobox(
            controls,
            textvariable=self.color_mode,
            values=("Original", "Grayscale", "Vivid", "Game Boy", "Limited colors"),
            state="readonly",
            width=16,
        )
        mode_menu.grid(row=0, column=3, padx=(0, 16), pady=14)
        mode_menu.bind("<<ComboboxSelected>>", lambda _event: self.update_preview())

        self.preview = tk.Label(
            self.root,
            text="Your preview will appear here",
            font=("Segoe UI", 14),
            fg="#9aa0a6",
            bg="#292a2d",
            height=20,
        )
        self.preview.pack(fill="both", expand=True, padx=24, pady=8)

        footer = tk.Frame(self.root, bg="#202124")
        footer.pack(fill="x", padx=24, pady=(8, 20))
        tk.Label(footer, textvariable=self.status, fg="#bdc1c6", bg="#202124").pack(
            side="left"
        )
        tk.Button(
            footer,
            text="Save result",
            command=self.save_image,
            font=("Segoe UI", 10, "bold"),
            bg="#81c995",
            fg="#202124",
            relief="flat",
            padx=14,
            pady=7,
            cursor="hand2",
        ).pack(side="right")

    def open_image(self):
        path = filedialog.askopenfilename(title="Choose an image", filetypes=SUPPORTED_FILETYPES)
        if not path:
            return

        try:
            self.original_image = ImageOps.exif_transpose(Image.open(path))
            self.original_image.load()
            self.original_path = path
            self.status.set(f"Loaded: {os.path.basename(path)}")
            self.update_preview()
        except (OSError, ValueError) as error:
            messagebox.showerror("Could not open image", str(error))

    def update_preview(self):
        if self.original_image is None:
            return

        try:
            self.result_image = pixelate_image(
                self.original_path,
                self.pixel_size.get(),
                self.color_mode.get(),
                self.color_count.get(),
            )
        except (OSError, ValueError) as error:
            self.status.set(str(error))
            return

        preview_image = self.result_image.copy()
        preview_image.thumbnail((900, 520), Image.Resampling.LANCZOS)
        self.preview_reference = ImageTk.PhotoImage(preview_image)
        self.preview.configure(image=self.preview_reference, text="")
        self.status.set(
            f"{self.result_image.width} x {self.result_image.height} | "
            f"Pixel size: {self.pixel_size.get()}"
        )

    def save_image(self):
        if self.result_image is None or not self.original_path:
            messagebox.showinfo("Nothing to save", "Open an image first.")
            return

        base_name = os.path.splitext(os.path.basename(self.original_path))[0]
        save_path = filedialog.asksaveasfilename(
            title="Save pixel art",
            initialfile=f"{base_name}_pixelated.png",
            defaultextension=".png",
            filetypes=[
                ("PNG image", "*.png"),
                ("JPEG image", "*.jpg"),
                ("All files", "*.*"),
            ],
        )
        if not save_path:
            return

        image_to_save = self.result_image
        if os.path.splitext(save_path)[1].lower() in (".jpg", ".jpeg"):
            if image_to_save.mode == "RGBA":
                background = Image.new("RGB", image_to_save.size, "white")
                background.paste(image_to_save, mask=image_to_save.getchannel("A"))
                image_to_save = background
            else:
                image_to_save = image_to_save.convert("RGB")

        try:
            image_to_save.save(save_path)
            self.status.set(f"Saved: {os.path.basename(save_path)}")
            messagebox.showinfo("Saved", f"Pixel art saved to:\n{save_path}")
        except OSError as error:
            messagebox.showerror("Could not save image", str(error))


def main():
    root = tk.Tk()
    PixelConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
