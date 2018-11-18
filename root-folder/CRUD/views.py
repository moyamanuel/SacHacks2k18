from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from CRUD.firebase_config import firebase
from requests.exceptions import HTTPError
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from CRUD.sentiment import analyze

# Create your views here.

base_url = 'http://127.0.0.1:8000/'

auth = firebase.auth()
db = firebase.database()

def check_login_firebase(email, password):
    user_data = {'localId': ''}
    try:
        user_data = auth.sign_in_with_email_and_password(email, password)
        print('type of user_data: {}'.format(type(user_data)))
    except HTTPError as e:
        user_data = {'localId': ''}
    print('type of user_data: {}'.format(type(user_data)))
    print('user_data keys: {}'.format(user_data.keys()))
    print('user_data: {}'.format(user_data))
    return user_data

def gather_team_stats():
    return dict(db.child('team_stats').child('home').get().val())

def index(request):
    print('### AT INDEX ###')
    if request.GET.get('signin_button'):
        print('### PRESSED SIGNIN BUTTON ###')
        email = request.GET.get('username')
        password = request.GET.get('password')
        print('email: %s' % email)
        print('password: %s' % password)

        user_data = check_login_firebase(email, password)
        print('user_data:\n')
        print(user_data)

        if user_data['localId'] == '':
            print('### NOT A VALID USER ###')
        else:
            print('### A VALID USER ###')
            return HttpResponseRedirect(base_url + 'verify_user')
    return render(request, 'CRUD/index.html')

def team_analytics(request):
    print('### AT TEAM ANALYTICS ###')
    team_stats = gather_team_stats()
    points = team_stats['pts']
    threept_perc = team_stats['3p_perc']
    assists = team_stats['ast']
    rebounds = team_stats['reb']
    rebounds_defensive = team_stats['dreb']
    rebounds_offensive = team_stats['oreb']
    field_goals = team_stats['fg']
    field_goals_perc = team_stats['fg_perc']
    free_throw_perc = team_stats['ft_perc']
    steals = team_stats['stl']

def test(request):
    return HttpResponse("test!")

@csrf_exempt
def verify_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_data = auth.sign_in_with_email_and_password(email, password)
        except HTTPError as e:
            user_data = {'localId': ''}
        return HttpResponse(json.dumps(user_data))
    else:
        return HttpResponse('gucci')

@csrf_exempt
def user_info(request):
    if request.method == 'POST':
        user_id = request.POST['localId']
        user_info = db.child('users').child(user_id).get()
        return HttpResponse(json.dumps(user_info.val()))

@csrf_exempt
def post_comment(request):
    print('### POST_COMMENT ROUTE ###')
    if request.method == 'POST':
        print('request.POST: {}'.format(request.POST))
        comment_text = request.POST['comment_text']
        timestamp = datetime.now().isoformat()
        user_id = request.POST['localId']
        post_id = request.POST['post_id']
        print('comment_text: {}'.format(comment_text))
        sentiment_data = analyze(comment_text)
        print('sentiment_data: {}'.format(sentiment_data))
        db.child('comments').push({
            'comment_text': comment_text,
            'timestamp': timestamp,
            'user_id': user_id,
            'sentiment_data': sentiment_data['document_tone']['tones'],
            'post_id': post_id,
        })
        return HttpResponse(sentiment_data)

# def home_signin(request):
#     if request.GET.get('signin_button'):
#         email = request.GET.get('username')
#         password = request.GET.get('password')
#         print('email: %s' % email)
#         print('password: %s' % password)


# @csrf_exempt
# def make_post(request):
#     if request.method == 'POST':
#         filename = request.POST['filename']