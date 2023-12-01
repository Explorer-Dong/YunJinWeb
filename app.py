from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost:3306/poem"


db = SQLAlchemy(app)


class Poem(db.Model):
	__tablename__ = "poem_table"
	dynasty = db.Column(db.String(10), primary_key=True)
	ori = db.Column(db.String(100))
	fro = db.Column(db.String(30))
	kind = db.Column(db.String(10))
	
	def __init__(self, dynasty, ori, fro, kind):
		self.dynasty = dynasty
		self.ori = ori
		self.fro = fro
		self.kind = kind


@app.route("/", methods=["POST", "GET"])
def homepage():
	"""
	参数列表：
	"""
	
	if request.method == "POST":
		# 搜索状态
		keyword = request.form.get("search_of_key", "")
		poems = Poem.query.filter(Poem.ori.like("%" + keyword + "%"))
		
		for it in poems:
			print(it)

		if poems.first() is None:
			return render_template("homepage.html", poems=[], keyword="__error__")
		else:
			return render_template("homepage.html", poems=poems, keyword=keyword)
		
	else: # request.method == "GET"
		# 初始进入当前界面状态
		return render_template("homepage.html", poems=[], keyword="__new__")


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
