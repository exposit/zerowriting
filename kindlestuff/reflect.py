# reflect.py
# take contents of a specified document and convert to html every second
# serve it up as a website; code website to refresh every second on browser end
# note you have to replace the host with the zero's reported host, and I haven't tested in the field (ie, using a phone hotspot or something) at all
# also it's slow and good luck if you lose focus

import sys
from flask import Flask, render_template

if len(sys.argv) == 2: # filename specified hopefully
    fname = sys.argv[1]
else:
    fname = "scribble.md"

app = Flask(__name__, template_folder="")

@app.route('/', methods=["GET", "POST"])
def index():
    #b_lines = [row for row in reversed(list(open("app.py")))]
    b_lines = [row for row in list(open(fname))]
    # if I could figure out how to pull from the buffer directly I could just pipe it over
    return render_template('index.html', b_lines=b_lines)

if __name__ == "__main__":
    app.run(host='192.168.7.176', port=5000, debug=True, threaded=False)
