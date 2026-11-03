from flask import Flask, render_template, request
from database import DBhandler

app = Flask(__name__)

DB = DBhandler()

@app.route("/submit_item_post", methods=["POST"])
def reg_item_submit():

    # 1. 상품 등록 form 데이터 받기
    data = request.form

    # 2. 이미지 파일 받기
    image_file = request.files["repImg"]

    # 3. 이미지 저장 경로 생성
    img_path = "static/images/{}".format(image_file.filename)

    # 4. 이미지 저장
    image_file.save(img_path)

    # 5. Firebase에 상품 정보 저장
    DB.insert_item(
        data["prodName"],
        data,
        img_path
    )

    # 6. 결과 페이지
    return render_template(
        "result.html",
        data=data,
        img_path=img_path
    )

@app.route("/list")
def get_list():
    return render_template("list.html")


@app.route("/review")
def review():
    return render_template("review.html")
    


@app.route("/reg_items")
def reg_items ():
    return render_template("reg_items.html")
    


@app.route("/reg_reviews")
def reg_reviews():
    return render_template("reg_reviews.html")
    

@app.route("/")
def index():
    return render_template("index.html")
    



if __name__ == "__main__":
    app.run(debug=True)