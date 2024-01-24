# SJTU EE208
import re
from ast import keyword
from flask import Flask, redirect, render_template, request, url_for
from bs4 import BeautifulSoup
INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
from ImgSearchFiles import searchimg

from java.io import File,StringReader
from java.nio.file import Path
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.cjk import CJKAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from org.apache.lucene.search.highlight import Highlighter,QueryScorer 

from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)



def search_contents_relevance(searcher,analyzer,command):
        heads = []
        urls = []
        texts = []
        times = []
        imgs = []

        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs

        # 获取关键字上下文，并对关键字进行高亮处理
        HighlightFormatter = SimpleHTMLFormatter("<span style = 'color:red'>","</span>")
        highlighter = Highlighter(HighlightFormatter, QueryScorer(query))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            heads.append(doc.get('title'))
            urls.append(doc.get('url'))
            times.append(doc.get('time'))
            img = eval(doc.get('img'))
            if len(img)==0:
                imgs.append("//k.sinaimg.cn/n/default/feedbackpics/transform/116/w550h366/20180409/SXMa-fyvtmxe2860250.png/w300h200f1t0l0q100syf.jpg")
            else:
                imgs.append(img[0][6:])
            text = doc.get('contents')

            ts = analyzer.tokenStream('contents', StringReader(text))
            texts.append(highlighter.getBestFragments(ts,text,1,'...'))
        print(len(heads))
        return heads,urls,texts,times,imgs

def search_contents_time(searcher, analyzer, command):
        heads = []
        urls = []
        texts = []
        times = []
        imgs = []

        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, 30).scoreDocs

        # 获取关键字上下文，并对关键字进行高亮处理
        HighlightFormatter = SimpleHTMLFormatter("<span style = 'color:red'>","</span>")
        highlighter = Highlighter(HighlightFormatter, QueryScorer(query))

        lst = []
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            lst.append([])
            lst[i].append(doc.get("time"))
            lst[i].append(doc.get("title"))
            lst[i].append(doc.get("url"))
            lst[i].append(doc.get("name"))
            lst[i].append(doc.get("path"))
            lst[i].append(doc.get("contents"))
            lst[i].append(eval(doc.get("img")))
        lst.sort(reverse=True)
        
        for ans in lst:
            heads.append(ans[1])
            urls.append(ans[2])
            times.append(ans[0])
            text = ans[5]

            ts = analyzer.tokenStream('contents', StringReader(text))
            texts.append(highlighter.getBestFragments(ts,text,1,'...'))
            img = ans[6]
            if len(img) == 0:
                imgs.append("//k.sinaimg.cn/n/default/feedbackpics/transform/116/w550h366/20180418/vaBs-fzihnep5214969.png/w300h200f1t0l0q100syf.jpg")
            else:
                imgs.append(img[0][6:])
        print(len(heads))
        return heads,urls,texts,times,imgs

def content_categories(searcher, analyzer, command):
    heads = []
    urls = []
    times = []
    imgs = []

    # 可以作为分类：电视 电影 好莱坞 综艺 韩娱 专题 音乐 明星 演出
    if command == '':
        return

    query = QueryParser("contents", analyzer).parse(command)
    
    scoreDocs = searcher.search(query, 50).scoreDocs

    lst = []
    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        lst.append([])
        lst[i].append(doc.get("time"))
        lst[i].append(doc.get("title"))
        lst[i].append(doc.get("url"))
        lst[i].append(doc.get("name"))
        lst[i].append(doc.get("path"))
        lst[i].append(doc.get("contents"))
        lst[i].append(eval(doc.get("img")))
    lst.sort(reverse=True)

    for ans in lst:
        heads.append(ans[1])
        urls.append(ans[2])
        times.append(ans[0])
        img = ans[6]
        if len(img) == 0:
            imgs.append("https://lupic.cdn.bcebos.com/20220320/3086293165_14_561_400.jpg")
        else:
            imgs.append(img[0][6:])
        imgs.append

    return heads,urls,times,imgs


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        keywords = request.form['keywords']    
        if keywords == '':
            return render_template('Home.html')
        return redirect(url_for('search_relevance', keywords=keywords))
    
    keywords = '的' # 获取用户输入数据
    STORE_DIR = "code/index"
    vm.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = CJKAnalyzer()

    # 获取与用户输入数据相关的网页标题、超链接以及关键词上下文
    heads,urls,texts,times,imgs= search_contents_time(searcher, analyzer, keywords) 
    header = []
    for i in range(1,6,4):
        dic = {}
        dic['head'] = heads[i]
        dic['url'] = urls[i]
        dic['text'] = texts[i]
        dic['time'] = times[i]
        dic['img'] = imgs[i]
        header.append(dic)

    data1 = []
    for i in range(2,7):
        dic = {}
        dic['head'] = heads[i]
        dic['url'] = urls[i]
        dic['text'] = texts[i]
        dic['time'] = times[i]
        dic['img'] = imgs[i]
        data1.append(dic)
    
    data2 = []
    for i in range(7,12):
        dic = {}
        dic['head'] = heads[i]
        dic['url'] = urls[i]
        dic['text'] = texts[i]
        dic['time'] = times[i]
        dic['img'] = imgs[i]
        data2.append(dic)
    del searcher
    data = list(zip(data1,data2))
    return render_template("Home.html",data=data,header=header)


@app.route('/search_time',methods=['GET'])
def search_time():
    keywords = request.args.get('keywords') # 获取用户输入数据
    if keywords == '':
        return render_template('Home.html')
    STORE_DIR = "code/index"
    vm.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = CJKAnalyzer()

    # 获取与用户输入数据相关的网页标题、超链接以及关键词上下文
    heads,urls,texts,times,imgs= search_contents_time(searcher, analyzer, keywords) 
    data = []
    for i in range(len(heads)):
        dic = {}
        dic['head'] = heads[i]
        dic['url'] = urls[i]
        dic['text'] = texts[i]
        dic['time'] = times[i]
        dic['img'] = imgs[i]
        data.append(dic)
    del searcher       
    #翻页
    found=len(data)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    per_page=int(request.args.get('per_page',default=6)) #这样可以整除
    #要传进template的代码
    res = [single for single in data[(page-1)*per_page:page*per_page]]
    pagination=Pagination(found=found,page=page,search=True,total=found,per_page=per_page,bs_version=4)
    return render_template("Search.html",res=res,keywords=keywords,pagination=pagination)

@app.route('/search_relevance', methods=['GET'])
def search_relevance():
    keywords = request.args.get('keywords') # 获取用户输入数据
    if keywords == '':
        return render_template('Home.html')
    STORE_DIR = "code/index"
    vm.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = CJKAnalyzer()

    # 获取与用户输入数据相关的网页标题、超链接以及关键词上下文
    heads,urls,texts,times,imgs = search_contents_relevance(searcher, analyzer, keywords) 
    data = []
    for i in range(len(heads)):
        dic = {}
        dic['head'] = heads[i]
        dic['url'] = urls[i]
        dic['text'] = texts[i]
        dic['time'] = times[i]
        dic['img'] = imgs[i]
        data.append(dic)
    del searcher       

    #翻页
    found=len(data)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    per_page=int(request.args.get('per_page',default=6)) #这样可以整除
    #要传进template的代码
    res = [single for single in data[(page-1)*per_page:page*per_page]]
    pagination=Pagination(found=found,page=page,search=True,total=found,per_page=per_page,bs_version=4)
    return render_template("Search.html",res=res,keywords=keywords,pagination=pagination)

@app.route('/categories', methods=['GET'])
def categories():
    keywords = request.args.get('keywords')
    if keywords == None:
        keywords='首页'
    print("keywords:",keywords)
    STORE_DIR = "code/index"
    vm.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = CJKAnalyzer()

    # 获取与用户输入数据相关的网页标题、超链接以及关键词上下文
    heads,urls,times,imgs= content_categories(searcher, analyzer, keywords) 
    data = []
    for i in range(len(heads)):
        dic = {}
        dic['head'] = heads[i]
        dic['url'] = urls[i]
        dic['time'] = times[i]
        dic['img'] = imgs[i]
        data.append(dic)
    del searcher       

    #翻页
    found=len(data)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    per_page=int(request.args.get('per_page',default=9)) #这样可以整除
    #要传进template的代码
    res = [single for single in data[(page-1)*per_page:page*per_page]]
    pagination=Pagination(found=found,page=page,search=True,total=found,per_page=per_page,bs_version=4)
    print(pagination.link)
    flag = 1
    if str(keywords) == '电视':
        flag = 2
    if str(keywords) == '电影':
        flag = 3
    if str(keywords) == '好莱坞':
        flag = 4
    if str(keywords) == '综艺':
        flag = 5
    if str(keywords) == '韩娱':
        flag = 6
    if str(keywords) == '专题':
        flag = 7
    if str(keywords) == '音乐':
        flag = 8
    if str(keywords) == '明星':
        flag = 9
    if str(keywords) == '演出':
        flag = 10
    return render_template("Categories.html",res=res,keywords=keywords,pagination=pagination,flag=flag)

# app /photo
def allowd_file(filename):
    ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/photo', methods=['GET','POST'])
def photo():

    keywords = request.args.get('keywords')
    if keywords == None:
        keywords='首页'
    STORE_DIR = "code/index"
    vm.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = CJKAnalyzer()

    # 获取与用户输入数据相关的网页标题、超链接以及关键词上下文
    heads,urls,times,imgs= content_categories(searcher, analyzer, keywords) 
    data = []
    for i in range(len(heads)):
        dic = {}
        dic['head'] = heads[i]
        dic['url'] = urls[i]
        dic['time'] = times[i]
        dic['img'] = imgs[i]
        data.append(dic)
    del searcher       

    #翻页
    found=len(data)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    per_page=int(request.args.get('per_page',default=9)) #这样可以整除
    #要传进template的代码
    res = [single for single in data[(page-1)*per_page:page*per_page]]
    pagination=Pagination(found=found,page=page,search=True,total=found,per_page=per_page,bs_version=4)

    UPLOAD_FOLDER=os.path.join(os.getcwd(),'code','upload')
    if request.method == 'POST':
        file = request.files['image']
        if file and allowd_file(file.filename):
            filename=file.filename
            file.save(os.path.join(UPLOAD_FOLDER,filename))
            filepath=os.path.join(UPLOAD_FOLDER,filename)
            print(filepath)
            data=searchimg(filepath)
            res2 = [single for single in data[(page-1)*per_page:page*per_page]]
 

        return render_template("Photo.html",res=res2,keywords=keywords,pagination=pagination)
    return render_template("Photo.html",res=res,keywords=keywords,pagination=pagination)

@app.route('/introduce', methods=['GET'])
def introduction():
    return render_template("introduce.html")

#错误处理
@app.errorhandler(Exception)
def page_not_found(e):
    return render_template('404.html'),404


if __name__ == '__main__':
    vm = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    app.run(debug=True, port=8080)
    