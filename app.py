from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import whisper

# Cấu hình ứng dụng Flask
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Bảo mật CSRF
app.config['UPLOAD_FOLDER'] = 'uploads'  # Thư mục lưu file tải lên
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'flac', 'm4a', 'aac', 'ogg', 'wma'}

# Tạo thư mục lưu file nếu chưa tồn tại
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Kiểm tra định dạng file hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Hàm chuyển đổi âm thanh sang văn bản
def transcribe_audio(file_path):
    try:
        model = whisper.load_model("base")  # Hoặc "small", "medium", "large"
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        return f"Lỗi: {e}"

# Route chính
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Kiểm tra file tải lên
        if 'file' not in request.files:
            flash("Không tìm thấy file tải lên!", "error")
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash("Chưa chọn file!", "error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # Lưu file tải lên

            # Gọi Whisper để xử lý
            transcribed_text = transcribe_audio(file_path)

            # Xóa file sau khi xử lý để tiết kiệm dung lượng
            os.remove(file_path)

            return render_template('index.html', transcribed_text=transcribed_text)

        else:
            flash("Định dạng file không hợp lệ!", "error")
            return redirect(request.url)

    return render_template('index.html')

# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
