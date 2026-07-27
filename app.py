import os
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from caption_service import generate_caption

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey_change_in_production'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['image']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No image selected for upload')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Generate the caption using the external service module
            try:
                caption = generate_caption(filepath)
            except Exception as e:
                caption = f"Error generating caption: {str(e)}"
                
            return render_template('index.html', filename=filename, caption=caption)
        else:
            flash('Invalid file type. Allowed types are: png, jpg, jpeg, gif')
            return redirect(request.url)
            
    # GET request just renders the form
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask app on localhost (127.0.0.1) port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
