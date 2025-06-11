from flask import Flask, render_template,request
app = Flask(__name__)
@app.route('/',methods=['GET'  ])
def index():

    return render_template(r"english_tool.html")


if __name__ == '__main__':
    app.run(debug=True )