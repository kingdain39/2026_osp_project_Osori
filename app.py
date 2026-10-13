from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "!"

@app.route("/submit_item_post")
def reg_item_submit(){
    
}

if __name__ == "__main__":
    app.run(debug=True)