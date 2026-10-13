from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/submit_item_post", methods =["POST"])
def reg_item_submit():
    # ① 글자 입력값 6개를 통째로 data에 담기
        # ② 사진 파일을 꺼내기
        # ③ 사진을 static/uploads/ 에 저장하기 
        # ④ 화면에서 쓸 사진 경로(img_path) 만들기
        # ⑤ result.html을 돌려주면서 data, img_path 넘기기
    data = request.form
    image_file = request.files["repImg"]
    image_file.save("static/images/{}".format(image_file.filename))
    return render_template("result.html",data=data,img_path="static/images/{}".format(image_file.filename))
    



@app.route("/list")
def get_list():
    return "list.html"


@app.route("/review")
def review():
    return "review.html"


@app.route("/reg_items")
def reg_items ():
    return "reg_items.html"


@app.route("/reg_reviews")
def reg_reviews():
    return "reg_reviews.html"

@app.route("/")
def index():
    return "index.html"



if __name__ == "__main__":
    app.run(debug=True)