from flask import Flask, render_template, request, send_file, jsonify
from module.ZoomChat2Srt import ZoomChat2Txt

app = Flask(__name__)

output_filename = ""

@app.route("/", methods=['GET', 'POST'])
def home():
  if request.method == 'GET':
    return render_template('home.html')

  elif request.method == 'POST':
    f = request.files['file']
    *filename, ext = f.filename.split('.')
    filename = '.'.join(filename)
    global output_filename
    output_filename = f"{filename}.srt"
    
    if ext.lower() != 'txt':
      raise Exception("Only support txt file")
    f.save(f"{filename}.{ext}")

    zoomchat2sub = ZoomChat2Txt(f"{filename}.{ext}")
    zoomchat2sub.save_srt(output_filename)

    return render_template('home.html', download_link=True)
    
    
  return render_template('home.html')

@app.route("/download")
def download_output():
  return send_file("output.srt", download_name=output_filename)


if __name__ == '__main__':
  app.run(debug=True)

