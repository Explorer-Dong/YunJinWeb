# @Time   : 2023-12-03 23:33
# @File   : models.py
# @Author : Mr_Dwj

'''
ORM映射模型
	1. Poem: 诗词表
	2. ...
'''

from exts import db


class Poem(db.Model):
	__tablename__ = "poems"
	dynasty = db.Column(db.String(10), primary_key=True)
	ori = db.Column(db.String(100))
	fro = db.Column(db.String(30))
	kind = db.Column(db.String(10))
	
	def __init__(self, dynasty, ori, fro, kind):
		self.dynasty = dynasty  # 朝代
		self.ori = ori          # 原文
		self.fro = fro          # 朝代
		self.kind = kind        # 文体
