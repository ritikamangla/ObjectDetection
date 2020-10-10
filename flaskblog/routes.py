import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect,request
from flaskblog import app,db,bcrypt

from flaskblog.forms import UpdateAccountForm
from flask_login import login_user, current_user,logout_user,login_required
from imageai.Detection import ObjectDetection
import os
import cv2
import numpy as np
import cv2
import pytesseract
import re




@app.route("/")
@app.route("/home")
def home():
	return render_template('account2.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_,f_ext=os.path.splitext(form_picture.filename)
	picture_fn=random_hex+f_ext
	picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)

	#output_size=(300,3000)
	i=Image.open(form_picture)
	#i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


def loadModels(imagepath):
	execution_path = os.getcwd()
	detector = ObjectDetection()
	detector.setModelTypeAsYOLOv3()
	x = execution_path + "\\flaskblog"
	detector.setModelPath( os.path.join(x , "yolo.h5"))
	detector.loadModel()
	print("Models have been loaded")

	input_image_path = x + "\\static\\profile_pics\\" + imagepath
	detections = detector.detectObjectsFromImage(input_image= input_image_path , output_image_path= input_image_path)
	#detections = detector.detectObjectsFromImage(input_image= input_image_path , output_image_path=os.path.join(execution_path , "imagenew.png"))
    

	people = 0
	l = []
	for eachObject in detections:
	    #print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
	    if eachObject["name"] =='person' and eachObject["percentage_probability"]>50.00:
	        people = people + 1

	#count = templateMatching(input_image_path)
	#people = people - count
	return people


@app.route("/account",methods=['GET', 'POST'])
def account():
	form=UpdateAccountForm()
	print("IN ACCOUNT")
	if form.validate_on_submit():
		print("Form validate")
		if form.picture.data:
			picture_file=save_picture(form.picture.data)
			print("HEYYYY")
		return redirect(url_for('display' , image_f = picture_file))


	return render_template('account.html', title='Account',form=form)

@app.route("/display/<image_f>",methods=['GET', 'POST'])
def display(image_f):
	#print(current_user.image_file)
	image_file = image_f
	f = loadModels(image_file)
	
	print("Faces are:",f)
	image_file = url_for('static',filename='profile_pics/'+ image_file)
	return render_template('display.html' , image_file = image_file)