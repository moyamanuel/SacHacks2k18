from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from CRUD.firebase_config import firebase
from requests.exceptions import HTTPError
from django.views.decorators.csrf import csrf_exempt

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

        for k, v in user_data.items():
            print(k,':',v)

        if user_data['localId'] == '':
            print('### NOT A VALID USER ###')
        else:
            print('### A VALID USER ###')
            return HttpResponseRedirect(base_url + 'verify_user')
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
            user_data = {'localId': ''}
        return HttpResponse(json.dumps(user_data))
    else:
        return HttpResponse('gucci')

@csrf_exempt
def user_info(request):
    if request.method == 'POST':
        user_id = request.POST['localID']
        user_info = db.child('users').child(user_id).get()
        return HttpResponse(json.dumps(user_info.val()))



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







# @csrf_exempt
# def post_comment(request):
#     if request.method == 'POST':
#         comment_text = request.POST['comment_text']
#         timestamp = request.POST['timestamp']
#         user_id = request.POST['localID']
#         # TODO fix this now 