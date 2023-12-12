from flask import Flask, request, render_template
import os, json
import config               # 导入配置文件
from exts import db         # 导入数据库实例
from models import Poem     # 导入Poem模型ORM类

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


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
		file_size = round(os.path.getsize(file_path) / 1024, 2)
		file_type = os.path.splitext(file)[1]
		file_info_list.append({
			'name': os.path.splitext(file)[0],
			'type': file_type,
			'size': file_size
		})
	
	return render_template("files.html", files=file_info_list)


@app.route("/intro", methods=["POST", "GET"])
def intro():
	return render_template("intro.html")


@app.route("/photo", methods=["POST", "GET"])
def photo():
	with open('static/json/image_text.json', 'r', encoding='gbk') as f:
		image_text = json.load(f)
	return render_template("photo.html", image_text=image_text)


if __name__ == "__main__":
	app.run(debug=True, port='5000', host='0.0.0.0')
