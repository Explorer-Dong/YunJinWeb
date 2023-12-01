from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库，将数据库的URI替换为实际的数据库URI
app.config[
	"SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:123456@localhost:3306/poem"

# 配置数据库追踪信息，将其设置为False，否则会影响性能
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 创建数据库对象
db = SQLAlchemy(app)


# 定义数据库模型
class Poem(db.Model):
	# 指定正确的表名
	__tablename__ = "poem_table"
	# 定义表结构
	dynasty = db.Column(db.String(10), primary_key=True)  # 主键
	ori = db.Column(db.String(100))
	fro = db.Column(db.String(30))
	kind = db.Column(db.String(10))
	
	# 定义构造函数
	def __init__(self, dynasty, ori, fro, kind):
		self.dynasty = dynasty
		self.ori = ori
		self.fro = fro
		self.kind = kind


@app.route("/", methods=["POST", "GET"])
def index():
	page = request.args.get("page", 1, type=int)  # 获取当前页数，默认为第一页
	per_page = 6  # 每页显示的条目数
	
	if request.method == "POST":
		keyword = request.form.get("content", "")
		
		if keyword == "":
			return render_template("index.html", poems=[], keyword=keyword)
		else:
			poems = Poem.query.filter(Poem.ori.like("%" + keyword + "%")).paginate(page=page, per_page=per_page)
			return render_template("index.html", poems=poems, keyword=keyword)
	else:
		poems = Poem.query.paginate(page=page, per_page=per_page)
		return render_template("index.html", poems=poems, keyword="")


# 实现跳转到其他页面的逻辑
@app.route("/add1", methods=["POST", "GET"])
def add1():
	return render_template("add1.html")


@app.route("/add2", methods=["POST", "GET"])
def add2():
	return render_template("add2.html")


@app.route("/add3", methods=["POST", "GET"])
def add3():
	return render_template("add3.html")


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


if __name__ == "__main__":
	app.run(debug=True)
