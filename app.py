from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
  if request.method == 'GET':
    return render_template('home.html')
  elif request.method == 'POST':
    f = request.files['file']
    *filename, ext = f.filename.split('.')
    filename = '.'.join(filename)
    if ext.lower() != 'txt':
      raise Exception("Only support txt file")
    f.save(f"{filename}.{ext}")
    
  return render_template('home.html')


if __name__ == '__main__':
  app.run(debug=True)

