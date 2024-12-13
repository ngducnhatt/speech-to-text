import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import whisper


def transcribe_audio(file_path, language=None):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(file_path, language=language, fp16=False)
        return result["text"]
    except Exception as e:
        return f"Lỗi: {e}"


def open_audio_file():
    file_path = filedialog.askopenfilename(
        title="Chọn file âm thanh",
        filetypes=[
            ("Audio Files", "*.wav *.mp3 *.flac *.m4a *.aac *.ogg *.wma")]
    )
    if file_path:
        transcribe_button.config(state=tk.NORMAL)
        file_label.config(text=f"Đã chọn: {file_path.split('/')[-1]}")
        file_path_var.set(file_path)
    else:
        messagebox.showerror("Lỗi", "Chưa chọn file âm thanh nào!")


def handle_transcription():
    file_path = file_path_var.get()
    language = language_var.get()

    if language == "Tự xác định":
        language = None

    if not file_path:
        messagebox.showerror("Lỗi", "Vui lòng chọn file âm thanh trước.")
        return

    try:
        transcribed_text = transcribe_audio(file_path, language)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, transcribed_text)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def save_transcription():
    text_content = output_text.get(1.0, tk.END).strip()
    if not text_content:
        messagebox.showwarning("Thông báo", "Không có văn bản để lưu!")
        return

    file_path = filedialog.asksaveasfilename(
        title="Lưu tệp văn bản",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_content)
            messagebox.showinfo(
                "Thành công", f"Văn bản đã được lưu tại:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")


root = tk.Tk()
root.title("Speech to Text by Ngducnhat v1.0.0")
root.geometry("700x600")
root.configure(bg="#323232")

file_path_var = tk.StringVar()
language_var = tk.StringVar(value="Tự xác định")

frame_file = tk.Frame(root, bg="#323232")
frame_file.pack(pady=20)

file_label = tk.Label(frame_file, text="Chọn file âm thanh (.wav, .mp3, .flac, ...):",
    bg="#323232", fg="#ffffff", font=("Arial", 12))
file_label.pack(side=tk.LEFT, padx=10)

select_button = tk.Button(frame_file, text="Chọn file", command=open_audio_file,
    bg="#ffffff", fg="#323232", font=("Arial", 12), relief="flat")
select_button.pack(side=tk.LEFT)

frame_language = tk.Frame(root, bg="#323232")
frame_language.pack(pady=10)

language_label = tk.Label(frame_language, text="Ngôn ngữ đầu vào:",
    bg="#323232", fg="#ffffff", font=("Arial", 12))
language_label.pack(side=tk.LEFT, padx=10)

language_menu = ttk.Combobox(
    frame_language,
    textvariable=language_var,
    values=["Tự xác định", "en", "vi", "es", "fr", "de", "zh", "ja", "ko"],
    state="readonly",
    font=("Arial", 12)
)
language_menu.pack(side=tk.LEFT)
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground="#323232",
    background="#ffffff", foreground="#ffffff")

transcribe_button = tk.Button(root, text="Chuyển đổi", command=handle_transcription, state=tk.DISABLED,
    bg="#ffffff", fg="#323232", font=("Arial", 14, "bold"), relief="flat")
transcribe_button.pack(pady=10)

# Hiển thị kết quả
output_label = tk.Label(root, text="Văn bản được chuyển đổi:", bg="#323232",
    fg="#ffffff", font=("Arial", 12))
output_label.pack()

output_text = tk.Text(root, height=15, wrap=tk.WORD, bg="#323232", fg="#ffffff",
    font=("Arial", 12), relief="solid", bd=1, insertbackground="#ffffff")
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Nút lưu văn bản
save_button = tk.Button(root, text="Lưu văn bản", command=save_transcription,
    bg="#ffffff", fg="#323232", font=("Arial", 12), relief="flat")
save_button.pack(pady=10)

# Chạy ứng dụng
root.mainloop()
