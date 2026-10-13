from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

# # 리뷰 목록 페이지 URL 라우팅
# @app.route('/review')
# def view_review():5
#     return render_template('review.html')

# # 리뷰 등록 페이지 URL 라우팅
# @app.route('/reg_reviews')
# def reg_review():
#     return render_template('reg_reviews.html')

# # 상품 등록 URL 라우팅
# @app.route('/product')
# def view_review():
#     return render_template('product.html')

# # 상품 목록 URL 라우팅
# @app.route('/product')
# def view_review():
#     return render_template('product.html')

if __name__ == '__main__':
    app.run(debug=True)