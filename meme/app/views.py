from app import app
from flask import render_template, redirect, session, request
import facebook

@app.route('/', methods=['GET'])
def homepage():
	session['NumberOfQuestions'] = 20
	return render_template('login.html')

@app.route('/', methods=['POST'])
def getAccessToken():
	session['access_token'] = request.form['access_token']
	session['user_id'] = request.form['user_id']
	print ("access token: " + session['access_token'])
	print ("user id: " + session['user_id'])
	return redirect('/quiz/1')

@app.route('/quiz/<number>', methods=['GET'])
def displayQuestion(number):
	return render_template('quiz.html')

@app.route('/quiz/<number>', methods=['POST'])
def takeAnswer(number):
	session['q'+str(number)] = request.form['option']
	print (session['q'+str(number)])
	if(int(number) < session['NumberOfQuestions']):
		return redirect('/quiz/'+str(int(number)+1))
	elif(int(number) == session['NumberOfQuestions']):
		return redirect('/results')
	else:
		print ("error"+str(number))
		return False

@app.route('/results', methods=['GET'])
def results():
	users = open("app/static/users.csv","a")
	users.write(session['user_id'] + ",")
	for i in range(1,session['NumberOfQuestions']+1):
		users.write(session['q'+str(i)] + ",")
	users.write("\n")
	users.close()
	graph = facebook.GraphAPI(access_token=session['access_token'], version="2.7")
	friends = graph.get_connections(id=session['user_id'], connection_name='friends')
	print (friends)
	return False