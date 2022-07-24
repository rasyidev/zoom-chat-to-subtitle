from flask import Flask, redirect, render_template, request, send_file, session, flash
import uuid
from module.ZoomChat2Srt import ZoomChat2Txt
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = load_dotenv("SECRET_KEY")

output_filename = ""

@app.route("/", methods=['GET', 'POST'])
def home():
  # remove file session if any
  if session:
    session.clear()

  if request.method == 'GET':
    return render_template('home.html')

  elif request.method == 'POST':
    f = request.files['file']
    *filename, ext = f.filename.split('.')
    filename = '.'.join(filename)

    # set session using uuid
    uuid_session = uuid.uuid4()
    session['file'] = str(uuid_session)

    global output_filename
    output_filename = f"{filename}.srt"

    if filename == '':
      # raise Exception("You havent choose your file yet!")
      flash("You havent choose your file yet!", 'error')
      return redirect(request.url)
    
    if ext.lower() != 'txt':
      raise Exception("Only support txt file")
    f.save(f"uploads/{uuid_session}.{ext}")

    zoomchat2sub = ZoomChat2Txt(f"uploads/{uuid_session}.{ext}")
    zoomchat2sub.save_srt(f"uploads/{uuid_session}.srt")

    # delete txt file
    os.remove(f"uploads/{uuid_session}.txt")

    return redirect('/download')
  return render_template('home.html')

@app.route("/download")
def download_page():
  return render_template("download.html", sid=session['file'])

@app.route("/download/<filesession>")
def download_output(filesession):
  print("FILESESSION", filesession, session['file'], filesession == session['file'])
  if str(session['file']) == filesession:
    return send_file(f"uploads/{filesession}.srt", download_name=output_filename)
  else:
    return """
      <div class="flex justify-center items-center flex-col">
        <h1 class="text-2xl text-red-500">Your file is not uploaded yet</h1>
        <a href="#convert_file"
              class="inline-flex items-center justify-center w-full p-5 py-3 text-base font-medium text-white transition-colors duration-150 transform sm:w-auto bg-gradient-to-r from-blue-700 to-blue-900 hover:from-blue-600 hover:to-blue-600">
              <span class="mx-2">
                Upload File
              </span>
            </a>
      </div>  
    """


@app.route("/ceksession")
def ceksession():
  return f"{session['file']}"
if __name__ == '__main__':
  app.run(debug=True)

