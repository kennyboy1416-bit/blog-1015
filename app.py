from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# 範例文章
posts = [
    {
        "id": 1,
        "title": "我的第一篇部落格文章",
        "author": "王小明",
        "content": "大家好！這是我的第一篇部落格文章。"
    },
    {
        "id": 2,
        "title": "學習 Python Flask",
        "author": "陳小華",
        "content": "Flask 是一個輕量級的 Python Web 框架。"
    }
]

# 首頁：顯示所有文章
@app.route("/")
def index():
    return render_template("index.html", posts=posts)


# 文章詳細頁面
@app.route("/post/<int:post_id>")
def post_detail(post_id):
    post = next(
        (p for p in posts if p["id"] == post_id),
        None
    )

    if post is None:
        abort(404)

    return render_template("post.html", post=post)


# 新增文章表單與接收表單資料
@app.route("/create", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()

        # 檢查欄位是否都有填寫
        if not title or not author or not content:
            return render_template(
                "create.html",
                error="請填寫所有欄位。",
                title=title,
                author=author,
                content=content
            ), 400

        # 自動產生新的文章 ID
        new_id = max(
            (post["id"] for post in posts),
            default=0
        ) + 1

        new_post = {
            "id": new_id,
            "title": title,
            "author": author,
            "content": content
        }

        # 將文章加入清單
        posts.insert(0, new_post)

        # 發布成功後回到首頁
        return redirect(url_for("index"))

    return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)