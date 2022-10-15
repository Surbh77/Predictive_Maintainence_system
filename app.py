from copyreg import pickle
from json import tool
from operator import methodcaller
from flask import Flask,render_template,request,redirect
import pickle
import numpy as np

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    airtemp=0
    list1=0
    proctemp=0
    rotatespeed=0
    torque=0
    toolwear=0
    type=0
    Type_H=0
    Type_M=0
    Type_L=0
    prediction=0
    if request.method=='POST':
        airtemp=request.form['airtemp']
        proctemp=request.form['prostemp']
        rotatespeed=request.form['rotatespeed']
        torque=request.form['torque']
        toolwear=request.form['toolwear']
        type=request.form['type']
        if type=='High':
            Type_H=1
        elif type=='Medium':
            Type_M=1
        else:
            Type_L=1
        list1=[airtemp,proctemp,rotatespeed,torque,toolwear,Type_H,Type_M,Type_L]
        prediction=predict(list1)
    return render_template('index.html',prediction=prediction)

@app.route('/',methods=['GET','POST'])
def predict(list1):
    model=pickle.load(open('model/ref_model.pkl','rb'))
    inputvalue=np.array([list1])
    output=model.predict(inputvalue)
    if(output[0]==1):
        prediction='No Failure'
    elif(output[0]==0):
        prediction='Heat Dessipation Failure'
    elif(output[0]==3):
        prediction='Power Failure'
    elif(output[0]==2):
        prediction='Overstrain Failure'
    elif(output[0]==5):
        prediction='Tool Wear Failure'
    elif(output[0]==4):
        prediction='Random Failure'
    print(prediction)
    
    return prediction

if __name__=='__main__':
    app.run(debug=True)