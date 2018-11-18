from django.shortcuts import render
from django.http import HttpResponse
import json
from CRUD.firebase_config import firebase
from requests.exceptions import HTTPError
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

auth = firebase.auth()
db = firebase.database()

def index(request):
    return render(request, 'CRUD/index.html')

def test(request):
    return HttpResponse("test! ")

@csrf_exempt
def verify_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_data = auth.sign_in_with_email_and_password(email, password)
        except HTTPError as e:
            user_data = {'localID': ''}
        return HttpResponse(json.dumps(user_data))
    else:
        return HttpResponse('gucci')

@csrf_exempt
def user_info(request):
    if request.method == 'POST':
        user_id = request.POST['localID']
        user_info = db.child('users').child(user_id).get()
        return HttpResponse(json.dumps(user_info.val()))

@csrf_exempt
def make_post(request):
    if request.method == 'POST':
        filename = request.POST['filename']
        






@csrf_exempt
def post_comment(request):
    if request.method == 'POST':
        comment_text = request.POST['comment_text']
        timestamp = request.POST['timestamp']
        user_id = request.POST['localID']
        # TODO fix this now 