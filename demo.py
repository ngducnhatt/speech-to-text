import tkinter as tk
from tkinter import filedialog, messagebox
import whisper


def transcribe_audio(file_path):
    """
    Sử dụng Whisper để chuyển đổi âm thanh sang văn bản.
    """
    try:
        # Tải mô hình Whisper
        model = whisper.load_model("base")  # Hoặc "small", "medium", "large"
        result = model.transcribe(file_path)  # Xử lý file âm thanh
        return result["text"]
    except Exception as e:
        return f"Lỗi: {e}"


def open_audio_file():
    """
    Cho phép người dùng chọn file âm thanh từ hệ thống.
    """
    file_path = filedialog.askopenfilename(
        title="Chọn file âm thanh",
        filetypes=[("Audio Files", "*.wav *.mp3 *.flac *.m4a *.aac *.ogg *.wma")]
    )
    if file_path:
        transcribe_button.config(state=tk.NORMAL)
        file_label.config(text=f"Đã chọn: {file_path.split('/')[-1]}")
        file_path_var.set(file_path)
    else:
        messagebox.showerror("Lỗi", "Chưa chọn file âm thanh nào!")


def handle_transcription():
    """
    Gọi Whisper để xử lý file âm thanh và hiển thị kết quả.
    """
    file_path = file_path_var.get()
    if not file_path:
        messagebox.showerror("Lỗi", "Vui lòng chọn file âm thanh trước.")
        return

    try:
        transcribed_text = transcribe_audio(file_path)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, transcribed_text)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


# Giao diện người dùng Tkinter
root = tk.Tk()
root.title("Chuyển đổi âm thanh sang văn bản bằng Whisper")
root.geometry("600x500")

file_path_var = tk.StringVar()  # Biến lưu đường dẫn file âm thanh

# Khung chọn file
frame_file = tk.Frame(root)
frame_file.pack(pady=20)

file_label = tk.Label(frame_file, text="Chọn file âm thanh (.wav, .mp3, .flac, ...):")
file_label.pack(side=tk.LEFT, padx=10)

select_button = tk.Button(frame_file, text="Chọn file", command=open_audio_file)
select_button.pack(side=tk.LEFT)

# Nút chuyển đổi
transcribe_button = tk.Button(root, text="Chuyển đổi", command=handle_transcription, state=tk.DISABLED)
transcribe_button.pack(pady=10)

# Hiển thị kết quả
output_label = tk.Label(root, text="Văn bản được chuyển đổi:")
output_label.pack()

output_text = tk.Text(root, height=15, wrap=tk.WORD)
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Chạy ứng dụng
root.mainloop()
