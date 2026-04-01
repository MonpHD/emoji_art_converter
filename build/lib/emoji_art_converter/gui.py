import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from PIL import Image, ImageTk
import pyperclip

from .core import image_to_emoji

class EmojiArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emoji Art Converter")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e2a2f")
        
        self.image_path = None
        self.emoji_string = None
        
        # Stil
        self.root.option_add("*Font", "SegoeUI 10")
        
        # Hauptrahmen
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bildauswahl
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="📷 Bild auswählen", command=self.select_image).pack(side=tk.LEFT, padx=5)
        self.img_label = ttk.Label(btn_frame, text="Kein Bild geladen")
        self.img_label.pack(side=tk.LEFT, padx=10)
        
        # Einstellungen
        settings_frame = ttk.LabelFrame(main_frame, text="Einstellungen", padding=5)
        settings_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(settings_frame, text="Breite (Spalten):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.width_var = tk.IntVar(value=80)
        self.width_spin = ttk.Spinbox(settings_frame, from_=20, to=200, textvariable=self.width_var, width=5)
        self.width_spin.grid(row=0, column=1, padx=5, pady=5)
        
        # Konvertierungs-Button
        self.convert_btn = ttk.Button(settings_frame, text="✨ Konvertieren", command=self.convert_image, state=tk.DISABLED)
        self.convert_btn.grid(row=0, column=2, padx=20, pady=5)
        
        # Fortschrittsbalken
        self.progress = ttk.Progressbar(settings_frame, mode="indeterminate")
        self.progress.grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=5)
        
        # Ergebnisbereich
        result_frame = ttk.LabelFrame(main_frame, text="Emoji-Kunst", padding=5)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Zoom-Slider
        zoom_frame = ttk.Frame(result_frame)
        zoom_frame.pack(fill=tk.X, pady=2)
        ttk.Label(zoom_frame, text="Zoom:").pack(side=tk.LEFT)
        self.zoom_var = tk.IntVar(value=100)
        self.zoom_slider = ttk.Scale(zoom_frame, from_=30, to=200, orient=tk.HORIZONTAL, variable=self.zoom_var, command=self.apply_zoom)
        self.zoom_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.zoom_label = ttk.Label(zoom_frame, text="100%")
        self.zoom_label.pack(side=tk.LEFT)
        ttk.Button(zoom_frame, text="Reset", command=self.reset_zoom).pack(side=tk.RIGHT, padx=5)
        
        # Textbereich für Emojis
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        self.text_widget = tk.Text(text_frame, wrap=tk.NONE, font=("Courier New", 10), bg="#0a0f12", fg="#f0f0e0")
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll_y = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x = ttk.Scrollbar(result_frame, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        scroll_x.pack(fill=tk.X)
        self.text_widget.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Buttons unten
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        self.copy_btn = ttk.Button(button_frame, text="📋 In Zwischenablage kopieren", command=self.copy_to_clipboard, state=tk.DISABLED)
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Beenden", command=root.destroy).pack(side=tk.RIGHT, padx=5)
    
    def select_image(self):
        path = filedialog.askopenfilename(
            title="Bild auswählen",
            filetypes=[("Bilder", "*.jpg *.jpeg *.png *.bmp *.webp"), ("Alle Dateien", "*.*")]
        )
        if path:
            self.image_path = path
            self.img_label.config(text=os.path.basename(path))
            self.convert_btn.config(state=tk.NORMAL)
            # Vorschaubild anzeigen (optional)
            self.show_preview(path)
    
    def show_preview(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((200, 200))
            self.preview_img = ImageTk.PhotoImage(img)
            # Hier könnte man ein Label für die Vorschau einfügen, lassen wir erstmal
        except:
            pass
    
    def convert_image(self):
        if not self.image_path:
            messagebox.showerror("Fehler", "Kein Bild ausgewählt.")
            return
        self.convert_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.progress.start(10)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, "Konvertiere...")
        self.root.update()
        
        def task():
            try:
                width = self.width_var.get()
                result = image_to_emoji(self.image_path, width=width)
                self.emoji_string = result
                self.root.after(0, self.display_result)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Fehler", str(e)))
                self.root.after(0, self.reset_ui_after_convert)
            finally:
                self.root.after(0, self.stop_progress)
        
        threading.Thread(target=task, daemon=True).start()
    
    def display_result(self):
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, self.emoji_string)
        self.copy_btn.config(state=tk.NORMAL)
        self.convert_btn.config(state=tk.NORMAL)
    
    def stop_progress(self):
        self.progress.stop()
    
    def reset_ui_after_convert(self):
        self.convert_btn.config(state=tk.NORMAL)
        self.copy_btn.config(state=tk.DISABLED)
    
    def copy_to_clipboard(self):
        if self.emoji_string:
            pyperclip.copy(self.emoji_string)
            messagebox.showinfo("Erfolg", "Emoji-Kunst wurde in die Zwischenablage kopiert!")
    
    def apply_zoom(self, *args):
        zoom = self.zoom_var.get()
        self.zoom_label.config(text=f"{zoom}%")
        base_size = 10  # Basis-Schriftgröße in Pixel
        new_size = int(base_size * zoom / 100)
        self.text_widget.config(font=("Courier New", new_size))
    
    def reset_zoom(self):
        self.zoom_var.set(100)
        self.apply_zoom()

def launch_gui():
    root = tk.Tk()
    app = EmojiArtApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()