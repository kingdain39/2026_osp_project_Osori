from flask import Flask, render_template, request, flash, redirect, url_for, session, abort
from database import DBhandler
import hashlib
from pathlib import Path
from uuid import uuid4
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "helloosp"
app.config["REVIEW_UPLOAD_FOLDER"] = Path(app.static_folder) / "uploads" / "reviews"
DB = DBhandler()

ALLOWED_REVIEW_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def _save_review_image(image_file):
    """Save a review image and return only its generated filename."""
    original_name = secure_filename(image_file.filename or "")
    if not original_name or "." not in original_name:
        return None

    extension = original_name.rsplit(".", 1)[1].lower()
    if extension not in ALLOWED_REVIEW_IMAGE_EXTENSIONS:
        return None

    upload_folder = app.config["REVIEW_UPLOAD_FOLDER"]
    upload_folder.mkdir(parents=True, exist_ok=True)
    saved_name = f"{uuid4().hex}.{extension}"
    image_file.save(upload_folder / saved_name)
    return saved_name

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_confirm", methods=["POST"])
def login_confirm():
    user_id = request.form["user_id"]
    password = request.form["password"]

    user = DB.get_user(user_id)
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    if user and user["pw"] == pw_hash:
        session["user_id"] = user_id
        return redirect(url_for("index"))

    flash("Wrong ID or PW!")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup_post", methods =["POST"])
def register_user():
    # form에서 입력한 값들을 data에 담기
    data = request.form
    
    # 비밀번호를 해시화하기
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    # DB에 회원정보 저장하기
    if DB.insert_user(data, password_hash):
        return render_template("login.html")
    else:
        return render_template("signup.html", error="User ID already exists!")


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

@app.route("/item/<item_key>")
def item_detail(item_key):
    item = DB.get_item(item_key)

    # 존재하지 않는 상품이면 404 응답
    if item is None:
        abort(404)

    return render_template(
        "item_detail.html",
        item=item,
        item_key=item_key
    )

@app.route("/list")
def get_list():
    # 페이지 번호: 숫자가 아니면 1페이지
    page = request.args.get("page", default=1, type=int)
    per_page = 4

    # 상품 키를 기준으로 정렬해서 페이지마다 순서를 일정하게 유지
    items = sorted(DB.get_items().items(), key=lambda item: item[0])

    total_items = len(items)
    total_pages = max(1, (total_items + per_page - 1) // per_page)

    # 페이지 번호를 유효한 범위로 제한
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    page_items = items[start:start + per_page]

    return render_template(
        "list.html",
        items=page_items,
        page=page,
        total_pages=total_pages,
        total_items=total_items
    )


@app.route("/review")
def review():
    return render_template("review.html")
    


@app.route("/reg_items")
def reg_items ():
    return render_template("reg_items.html")
    


@app.route("/reg_reviews")
def reg_reviews():
    return render_template(
        "reg_reviews.html",
        product_name=request.args.get("product_name", ""),
        product_id=request.args.get("product_id", ""),
    )


@app.route("/submit_review_post", methods=["POST"])
@app.route("/reviews/new", methods=["POST"])
def reg_review_submit():
    """Create one Firebase review record and save its uploaded photo."""
    title = request.form.get("title", "").strip()
    product_name = request.form.get("product_name", "").strip()
    product_id = request.form.get("product_id", "").strip()
    body = request.form.get("body", request.form.get("content", "")).strip()
    rating = request.form.get("rating", "").strip()
    image_file = request.files.get("photo") or request.files.get("review_photo")

    if not all([title, product_name, body, rating, image_file and image_file.filename]):
        flash("리뷰 제목, 상품명, 사진, 내용, 별점을 모두 입력해주세요.")
        return redirect(url_for("reg_reviews", product_name=product_name, product_id=product_id))

    try:
        rating_value = int(rating)
    except ValueError:
        rating_value = 0
    if rating_value not in range(1, 6):
        flash("별점은 1점에서 5점 사이여야 합니다.")
        return redirect(url_for("reg_reviews", product_name=product_name, product_id=product_id))

    photo_filename = _save_review_image(image_file)
    if photo_filename is None:
        flash("사진은 png, jpg, jpeg, gif, webp 파일만 업로드할 수 있습니다.")
        return redirect(url_for("reg_reviews", product_name=product_name, product_id=product_id))

    DB.insert_review(
        title=title,
        product_name=product_name,
        product_id=product_id,
        body=body,
        rating=rating_value,
        photo_filename=photo_filename,
        writer_id=session.get("user_id", ""),
    )

    # The review-detail route will be implemented by the review 조회 담당자.
    flash("리뷰가 등록되었습니다.")
    return redirect(url_for("review"))
    

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
