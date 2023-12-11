from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import config
from exts import db
from models import Poem
import os

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 将ORM模型与数据库进行同步
# migrate = Migrate(app, db)


@app.route("/", methods=["POST", "GET"])
def homepage():
	"""
	输入：
		1. 搜索字段复选框: search_fields
		2. 搜索关键词表单: search_keyword
	返回：
		1. keyword: 搜索关键词
		2. poems: 过滤出来的诗词信息
		3. fields: 搜索字段
	"""
	
	if request.method == "POST":
		# 输入：搜索字段 & 搜索关键词
		fields = request.form.getlist("search_fields")
		keyword = request.form.get("search_keyword")
		
		if not len(fields):
			# 无搜索字段，默认搜索诗词原文
			fields.append("ori")
			poems = Poem.query.filter(Poem.ori.like("%" + keyword + "%"))
		else:
			# 有搜索字段，按照字段依次搜索
			filters = []
			for field in fields:
				if field == "dynasty":
					filters.append(Poem.dynasty.like("%" + keyword + "%"))
				elif field == "ori":
					filters.append(Poem.ori.like("%" + keyword + "%"))
				elif field == "fro":
					filters.append(Poem.fro.like("%" + keyword + "%"))
				elif field == "kind":
					filters.append(Poem.kind.like("%" + keyword + "%"))
			poems = Poem.query.filter(*filters)
		
		if not poems.count():
			# 无搜索结果：提示用户重新输入
			return render_template("homepage.html", poems=[], keyword="__error__")
		else:
			# 有搜索结果：返回搜索结果
			return render_template("homepage.html", poems=poems, keyword=keyword, fields=fields)
	
	else:
		# 初始界面，提示用户输入
		return render_template("homepage.html", poems=[], keyword="__new__")


@app.route("/files", methods=["POST", "GET"])
def files():
	# 获取static文件夹下的所有文件
	file_dir = os.path.join(app.root_path, 'static/files')
	files = os.listdir(file_dir)
	# 获取每个文件的信息
	file_info_list = []
	for file in files:
		file_path = os.path.join(file_dir, file)
		# 获取文件大小(KB)，并保留两位小数
		file_size = round(os.path.getsize(file_path) / 1024, 2)
		# 获取文件类型
		file_type = os.path.splitext(file)[1]
		# 将文件信息添加到列表中
		file_info_list.append({
			'name': file,
			'type': file_type,
			'size': file_size
		})

	return render_template("files.html", files=file_info_list)


@app.route("/intro", methods=["POST", "GET"])
def intro():
	return render_template("intro.html")


@app.route("/photo", methods=["POST", "GET"])
def photo():
	return render_template("photo.html")


if __name__ == "__main__":
	app.run(debug=True)
