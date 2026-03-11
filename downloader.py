import customtkinter as ctk
import yt_dlp
import threading
import os
import webbrowser
from PIL import Image
from tkinter import filedialog, messagebox

# Konfiguracja wyglądu
ctk.set_appearance_mode("Dark")  # Tryb ciemny
ctk.set_default_color_theme("blue")  # Niebieski motyw

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Podstawowa konfiguracja okna
        self.title("YT Downloader Pro")
        self.geometry("600x650")
        self.resizable(False, False)

        # Zmienne
        self.video_info = None
        self.save_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        self.create_widgets()

    def create_widgets(self):
        # Tytuł i Logo
        try:
            img = Image.open(r"K:\KLIENCI\BLACKBOX\AIBLACKBOX logo_pl.png")
            # Skalowanie proporcjonalne w zaleznosci od oryginalnej wielkosci
            ratio = 250 / img.width
            new_h = int(img.height * ratio)
            logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(250, new_h))
            self.label_title = ctk.CTkLabel(self, image=logo_img, text="")
        except Exception:
            self.label_title = ctk.CTkLabel(self, text="YT Downloader Professional", font=("Roboto", 24, "bold"))
            
        self.label_title.pack(pady=15)
        # Przekierowanie AI BlackBox
        self.label_title.bind("<Button-1>", lambda e: webbrowser.open("https://aiblackbox.co.uk/"))
        self.label_title.configure(cursor="hand2")

        # --- Sekcja URL ---
        self.url_frame = ctk.CTkFrame(self)
        self.url_frame.pack(pady=10, padx=20, fill="x")

        self.entry_url = ctk.CTkEntry(self.url_frame, placeholder_text="Wklej link z YouTube tutaj...")
        self.entry_url.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        self.btn_check = ctk.CTkButton(self.url_frame, text="Sprawdź", command=self.start_check_thread, width=100)
        self.btn_check.pack(side="right", padx=10, pady=10)

        # Informacja o wideo
        self.label_video_title = ctk.CTkLabel(self, text="", font=("Roboto", 14), text_color="#4ade80")
        self.label_video_title.pack(pady=5)

        # --- Karty wyboru (Tabview) ---
        self.tabview = ctk.CTkTabview(self, width=500, height=200)
        self.tabview.pack(pady=10)
        
        self.tab_audio = self.tabview.add("Audio (Muzyka)")
        self.tab_video = self.tabview.add("Video (Film)")

        # === Opcje AUDIO ===
        self.lbl_audio_fmt = ctk.CTkLabel(self.tab_audio, text="Format:")
        self.lbl_audio_fmt.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.combo_audio_fmt = ctk.CTkComboBox(self.tab_audio, values=["mp3", "flac"])
        self.combo_audio_fmt.grid(row=0, column=1, padx=20, pady=10)

        self.lbl_audio_bit = ctk.CTkLabel(self.tab_audio, text="Jakość (Bitrate):")
        self.lbl_audio_bit.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.combo_audio_bit = ctk.CTkComboBox(self.tab_audio, values=["192", "256", "320"])
        self.combo_audio_bit.set("320") # Domyślnie
        self.combo_audio_bit.grid(row=1, column=1, padx=20, pady=10)

        # === Opcje VIDEO ===
        self.lbl_video_fmt = ctk.CTkLabel(self.tab_video, text="Format:")
        self.lbl_video_fmt.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.combo_video_fmt = ctk.CTkComboBox(self.tab_video, values=["mp4", "avi"])
        self.combo_video_fmt.grid(row=0, column=1, padx=20, pady=10)

        self.lbl_video_res = ctk.CTkLabel(self.tab_video, text="Rozdzielczość:")
        self.lbl_video_res.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.combo_video_res = ctk.CTkComboBox(self.tab_video, values=["Sprawdź link najpierw"])
        self.combo_video_res.grid(row=1, column=1, padx=20, pady=10)

        # --- Wybór folderu ---
        self.frame_path = ctk.CTkFrame(self)
        self.frame_path.pack(pady=20, padx=20, fill="x")

        self.btn_path = ctk.CTkButton(self.frame_path, text="Wybierz folder zapisu", command=self.select_folder, fg_color="gray")
        self.btn_path.pack(side="left", padx=10, pady=10)
        
        self.lbl_path = ctk.CTkLabel(self.frame_path, text=f"Zapisz w: {self.save_path}", font=("Arial", 10))
        self.lbl_path.pack(side="left", padx=10)

        # --- Pasek postępu i Przycisk Pobierz ---
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.lbl_status = ctk.CTkLabel(self, text="Gotowy")
        self.lbl_status.pack(pady=5)

        self.btn_download = ctk.CTkButton(self, text="POBIERZ", command=self.start_download_thread, 
                                          width=200, height=50, font=("Roboto", 16, "bold"), fg_color="#dc2626", hover_color="#b91c1c")
        self.btn_download.pack(pady=20)

    # --- Logika Aplikacji ---

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_path = folder
            self.lbl_path.configure(text=f"Zapisz w: {self.save_path}")

    def start_check_thread(self):
        url = self.entry_url.get()
        if not url:
            messagebox.showwarning("Błąd", "Wklej link!")
            return
        
        self.btn_check.configure(state="disabled", text="Szukam...")
        threading.Thread(target=self.check_info, args=(url,), daemon=True).start()

    def check_info(self, url):
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.video_info = info
                
                # Przetwarzanie rozdzielczości
                formats = info.get('formats', [])
                resolutions = set()
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('height'):
                        resolutions.add(f['height'])
                
                sorted_res = sorted(list(resolutions), reverse=True)
                # Wybierz top 3, minimum 720p jeśli są
                top_resolutions = [r for r in sorted_res if r >= 720][:3]
                if not top_resolutions:
                    top_resolutions = sorted_res[:3]
                
                res_values = [f"{r}p" for r in top_resolutions]

                # Aktualizacja UI z głównego wątku (CustomTkinter radzi sobie z prostymi setami, ale dla bezpieczeństwa)
                self.after(0, lambda: self.update_ui_after_check(info.get('title'), res_values))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Błąd", f"Nie udało się pobrać informacji:\n{str(e)}"))
        finally:
            self.after(0, lambda: self.btn_check.configure(state="normal", text="Sprawdź"))

    def update_ui_after_check(self, title, resolutions):
        self.label_video_title.configure(text=title[:60] + "..." if len(title) > 60 else title)
        self.combo_video_res.configure(values=resolutions)
        if resolutions:
            self.combo_video_res.set(resolutions[0])

    def start_download_thread(self):
        if not self.video_info:
            messagebox.showwarning("Uwaga", "Najpierw kliknij 'Sprawdź', aby załadować wideo.")
            return

        mode = self.tabview.get() # "Audio (Muzyka)" lub "Video (Film)"
        url = self.entry_url.get()
        
        self.btn_download.configure(state="disabled", text="Pobieranie...")
        self.progress_bar.set(0)
        
        threading.Thread(target=self.download_process, args=(url, mode), daemon=True).start()

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p = d.get('_percent_str', '0%').replace('%','')
                progress = float(p) / 100
                self.progress_bar.set(progress)
                self.lbl_status.configure(text=f"Pobieranie: {d.get('_percent_str')} | Prędkość: {d.get('_speed_str')}")
            except:
                pass
        elif d['status'] == 'finished':
            self.lbl_status.configure(text="Przetwarzanie (konwersja)...")
            self.progress_bar.set(1)

    def download_process(self, url, mode):
        try:
            output_template = os.path.join(self.save_path, '%(title)s.%(ext)s')
            
            ydl_opts = {
                'outtmpl': output_template,
                'progress_hooks': [self.progress_hook],
            }
            # Jesli folder C:\ffmpeg\bin istnieje, dodaj go. Jesli nie, yt-dlp znajdzie samodzielnie w PATH
            if os.path.exists(r'C:\ffmpeg\bin\ffmpeg.exe'):
                ydl_opts['ffmpeg_location'] = r'C:\ffmpeg\bin'

            if mode == "Audio (Muzyka)":
                fmt = self.combo_audio_fmt.get()
                bitrate = self.combo_audio_bit.get()
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': fmt,
                    'preferredquality': bitrate,
                }]
            else:
                fmt = self.combo_video_fmt.get()
                res_str = self.combo_video_res.get()
                res = res_str.replace("p", "")
                
                ydl_opts['format'] = f'bestvideo[height={res}]+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'

                if fmt == 'avi':
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'avi',
                    }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.after(0, lambda: messagebox.showinfo("Sukces", "Pobieranie zakończone!"))
            self.after(0, lambda: self.lbl_status.configure(text="Gotowe"))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Błąd", f"Wystąpił błąd:\n{str(e)}"))
        finally:
            self.after(0, lambda: self.btn_download.configure(state="normal", text="POBIERZ"))

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()