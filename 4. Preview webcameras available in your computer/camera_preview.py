import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CameraPreviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Preview")

        # Create GUI elements
        self.camera_index = 0
        self.resolution = (640, 480)
        self.cap = None

        self.preview_label = ttk.Label(self.root)
        self.preview_label.pack(padx=10, pady=10)

        self.camera_combo = ttk.Combobox(self.root, state="readonly")
        self.camera_combo.pack(pady=5)
        self.resolution_combo = ttk.Combobox(self.root, state="readonly")
        self.resolution_combo.pack(pady=5)
        self.start_button = ttk.Button(self.root, text="Start Preview", command=self.start_preview)
        self.start_button.pack(pady=5)
        self.stop_button = ttk.Button(self.root, text="Stop Preview", command=self.stop_preview, state="disabled")
        self.stop_button.pack(pady=5)
        self.quit_button = ttk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=5)

        self.populate_camera_combo()
        self.populate_resolution_combo()

    def populate_camera_combo(self):
        num_cameras = 0
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if not cap.read()[0]:
                break
            num_cameras += 1
            cap.release()
        camera_list = list(range(num_cameras))
        self.camera_combo["values"] = camera_list
        self.camera_combo.current(0)

    def populate_resolution_combo(self):
        resolutions = [(640, 480), (800, 600), (1280, 720)]
        resolution_list = [f"{res[0]}x{res[1]}" for res in resolutions]
        self.resolution_combo["values"] = resolution_list
        self.resolution_combo.current(0)

    def start_preview(self):
        self.camera_index = int(self.camera_combo.get())
        selected_resolution = self.resolution_combo.get()
        self.resolution = tuple(map(int, selected_resolution.split("x")))

        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        self.stop_button.config(state="normal")
        self.start_button.config(state="disabled")
        self.camera_combo.config(state="disabled")
        self.resolution_combo.config(state="disabled")

        self.show_frame()

    def stop_preview(self):
        self.cap.release()
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.camera_combo.config(state="normal")
        self.resolution_combo.config(state="normal")
        self.show_placeholder_image()

    def show_placeholder_image(self):
        # You can set any placeholder image here
        pass

    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.preview_image = Image.fromarray(frame)
            self.preview_image_tk = ImageTk.PhotoImage(self.preview_image)
            self.preview_label.configure(image=self.preview_image_tk)
            self.preview_label.image = self.preview_image_tk
            self.preview_label.after(10, self.show_frame)
        else:
            print("Error: Failed to capture frame.")
            self.stop_preview()

def main():
    root = tk.Tk()
    app = CameraPreviewApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
