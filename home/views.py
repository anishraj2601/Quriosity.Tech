from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.models import problem, topic, userProblemData, myfaq, account_verification, like
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404 
import json
import uuid
from django.utils.safestring import mark_safe

# HTML pages
def index(request):
  # return render(request,'dashboard.html')
  return redirect('dashboard')

def base(request):
  at = topic.objects.all()
  # print(at)
  context={'at':at}
  return render(request,'base.html',context)

def base_copy(request):
  return render(request,'base_copy.html')

def signup(request):
  return render(request,'signup.html')

def log_in(request):
  return render(request,'login.html')

def activity(request):
  alltopic = topic.objects.all()
  prob = userProblemData.objects.filter(user=request.user).all().order_by('-last_updated_at')
  context = {'alltopic':alltopic,'prob':prob}
  return render(request,'activity.html',context)

def dashboard(request):
  messages.info(request,"More Topics & Problems are being added...")
  alltopic = topic.objects.all().order_by('priority')
  # print(alltopic)
  context = {'alltopic':alltopic}
  return render(request,'dashboard.html',context)

def faq(request):
  alltopic = topic.objects.all()
  allfaq = myfaq.objects.all()
  print(allfaq)
  context = {'alltopic':alltopic, 'allfaq':allfaq}
  return render(request,'faqs.html',context)

def profile(request):
  return render(request,'profile.html')

def settings(request):
  return render(request,'settings.html')

def search(request):
  return render(request,'search.html')

def page404(request):
  return render(request,'404.html')

def problems(request,slug):
  # if the user is anonymous then redirect view problems
  if request.user.is_anonymous:
    return redirect('/view/'+slug)
  if request.user.id == None:
    # messages.warning(request,"Please Signup/Login to view")
    messages.info(request, mark_safe("Please <a href='/signup'>Signup</a>/<a href='/log_in'>Login</a> to access all the features. Currently you have restricted access."))
    return redirect('dashboard')
  messages.info(request, mark_safe("Please make sure that you have <strong><a href='https://auth.geeksforgeeks.org/'>login</a></strong> to your <a href='https://auth.geeksforgeeks.org/'>geeksforgeeks</a> account in the same browser so that you can view the problems."))
  alltopic = topic.objects.all()
  top = topic.objects.filter(slug=slug).first()
  # if the slug is empty return 404
  if top is None:
    # messages.error(request,"Invalid Request !")
    return redirect('404')
  # if the topic is not active return 404
  if top.active is False:
    # messages.error(request,"This topic is currently not active")
    return redirect('404')
  prob = problem.objects.filter(topic=top).all().order_by('priority')
  total_problem = problem.objects.filter(topic=top).count()
  problem_solved = problem.objects.filter(topic=top,completed=request.user).count()
  problem_unsolved = total_problem - problem_solved
  userProbData = userProblemData.objects.filter(user = request.user).all()
  user = request.user
  # print(userProbData)
  # print(top)
  # print(prob)
  # print(userProbData)
  # print(problem_unsolved)
  context = {
    'alltopic':alltopic,
    'top':top,
    'prob':prob,
    'slug':slug,
    'userProbData':userProbData,
    'total_problem':total_problem,
    'problem_solved':problem_solved,
    'problem_unsolved':problem_unsolved,
    'user':user,

  }
  # messages.info(request,"Topic --> "+top.title)
  return render(request,'problems.html',context)

# Authentication APIs
def handleSignup(request):
  if(request.method=='POST'):
    # get the post parameters
    username = request.POST['username']
    fname = request.POST['fname']
    # mname = request.POST['mname']
    lname = request.POST['lname']
    email = request.POST['email'] 
    pass1 = request.POST['pass1']
    pass2 = request.POST['pass2']
    terms = request.POST['terms']

    # ------ validating all the user data ------
    # ------ validating fname -------
    if len(fname)>30:
      messages.error(request,"first name max lenght 30 char")
      return redirect('signup')
    if len(fname)==0:
      messages.error(request,"Enter first name")
      return redirect('signup')
    # check wheather the fname does not have any special characters
    if not fname.isalpha():
      messages.error(request,"first name should contain characters only")
      return redirect('signup')
    


    # ------ validating lname -------
    if len(lname)>30:
      messages.error(request,"last name max lenght 30 char")
      return redirect('signup')
    if len(lname)==0:
      messages.error(request,"Enter last name")
      return redirect('signup')
    # check wheather the lname does not have any special characters
    if not lname.isalpha():
      messages.error(request,"Last name should contain characters only")
      return redirect('signup')
    


    # --------- validating username -----------
    if len(username)>15:
      messages.error(request,"username max lenght 15 char")
      return redirect('signup')
    if len(username)<8:
      messages.error(request,"username min lenght 8 char")
      return redirect('signup')
    # check wheather the username is taken by some other user or not
    if not username.isalnum():
      messages.error(request,"username should be alphanumeric")
      return redirect('signup')
    if User.objects.filter(username=username).exists():
      messages.error(request,"username already taken")
      return redirect('signup')
    


    # ------ validating email -------
    if len(email)>64:
      messages.error(request,"Email max lenght 64 char")
      return redirect('signup')
    if len(email)==0:
      messages.error(request,"Enter your email")
      return redirect('signup')
    # check wheather the email does not have any special characters
    if User.objects.filter(email=email).exists():
      messages.error(request,"Account with this email already exists")
      return redirect('signup')



    # ------ validating pass1 -------
    if len(pass1)>24:
      messages.error(request,"Password max lenght 24 char")
      return redirect('signup')
    if len(pass1)==0:
      messages.error(request,"Enter your password")
      return redirect('signup')
    if len(pass1)<8:
      messages.error(request,"Password max lenght 8 char")
      return redirect('signup')
    # check wheather the pass1 does not have any special characters


    # ------ validating pass2 -------
    if len(pass2)>24:
      messages.error(request,"Password max lenght 24 char")
      return redirect('signup')
    if len(pass2)==0:
      messages.error(request,"Confirm your password")
      return redirect('signup')
    if pass1 != pass2:
      messages.error(request,"Passwords didn't match")
      return redirect('signup')


    # ------ validating terms -------
    if len(terms)==0:
      messages.error(request,"Please accept T&C")
      return redirect('signup')
    if terms != "True":
      messages.error(request,"Please accept the T&C")
      return redirect('signup')
    


    # Create the user
    myuser = User.objects.create_user(username,email,pass1)
    myuser.first_name = fname
    myuser.last_name = lname
    myuser.save()

    # now adding data in account_verification model
    auth_token = str(uuid.uuid4())
    # change the verification link after uploding on the server
    verification_link = 'https://quriosity.tech/verify/'+auth_token
    verify_obj = account_verification.objects.create(user = myuser, auth_token = auth_token, verification_link = verification_link)
    verify_obj.save()

    # sending the verification mail
    send_mail_after_registration(email,auth_token,fname,username)

    messages.success(request,"Your Account has been successfully created")
    messages.info(request,"A verification email has been send. Please verify your account")
    return redirect('signup')
  else:
    # return HttpResponse('404 - Not Found (Unauthorised access)')
    return render(request,'404.html')

def handleLogin(request):
  if request.method == 'POST':
    #get the post parameters
    loginusername = request.POST['loginusername']
    # loginemail = request.POST['loginemail']
    loginpass = request.POST['loginpass']
    # loginrem = request.POST['loginrem']
    loginrem = request.POST.get('loginrem', 'False')

    # validating all the data from the login form
    if len(loginusername)==0:
      messages.error(request,"Enter Username")
      return redirect('log_in')

    if not loginusername.isalnum():
      messages.error(request,"username should be alphanumeric")
      return redirect('log_in')

    if len(loginpass)==0:
      messages.error(request,"Enter Password")
      return redirect('log_in')

    # validating the user by username and password
    user = authenticate(username = loginusername, password = loginpass)
    if user is not None:
      # checking if the user has verified its email id or not and it account is blocked or not
      verify_obj = account_verification.objects.filter(user = user).first()
      # checking if the user account is blocked or not
      if not verify_obj.account_status:
        messages.error(request,"Your account has been blocked. Contact us at 'contact@quriosity.tech'")
        return redirect('log_in')
      #  if the user has verified his email then do login else tell him to verify his email id
      if verify_obj.verification_status:
        login(request, user)
        messages.success(request,"Successfully Logged In")
        return redirect('dashboard')
      else:
        messages.warning(request,"Please verify your email id")
        # send verification mail again
        user_obj_for_verify = User.objects.get(username = loginusername)
        send_mail_after_registration(user_obj_for_verify.email, verify_obj.auth_token, user_obj_for_verify.first_name, user_obj_for_verify.username)
        messages.info(request,"Verification email has been send to you email id")
        return redirect('log_in')
    else:
      messages.error(request,"Invalid Credentials, try again")
      return redirect('log_in')
  else:
    return render(request,'404.html')

# for logging out of the system (handleLogin)
def log_out(request):
  logout(request)
  messages.success(request,"Successfully Logged Out")
  return redirect('log_in')

# def sendEmail(request):
#   # I will send the email here
#   send_mail(
#     'Subject Test',
#     'Here is the test message.',
#     'noreply@quriosity.tech',
#     ['quriosity.tech@gmail.com'],
#     fail_silently=False,
#   )
#   return render(request,'email.html')

def forgotUsername(request):
  # return render(request,'forgot-username.html')
  return redirect('404')

def forgotPassword(request):
  # return render(request,'forgot-password.html')
  return redirect('404')



def likePost(request):
  # print("i am here")
  #check if the user is anonymous then display the message to login
  if request.method == 'POST':
    user = request.user
    problem_id = request.POST.get('post_id')
    slug_id = request.POST.get('slug_id')
    problem_obj= problem.objects.get(id=problem_id)

    if user in problem_obj.liked.all():
      # user has already liked it before but is clicking the like button again
      problem_obj.liked.remove(user)
    else:
      problem_obj.liked.add(user)
    like_obj, created = like.objects.get_or_create(user=user,problem_id=problem_id).first()
    if not created:
      if like_obj.value == 'Like':
        like_obj.value = 'Unlike'
      else:
        like_obj.value = 'Like'
    like_obj.save()

  # return redirect(problems,slug_id)
  html = "<html><body>Hello World</body></html>"
  return HttpResponse(html)



def ProblemLike(request, pk):
  post = get_object_or_404(problem, id=request.POST.get('problem_id'))
  if post.liked.filter(id=request.user.id).exists():
    post.liked.remove(request.user)
  else:
    # print("i am here")
    post.liked.add(request.user)

  return redirect(request.META.get('HTTP_REFERER'))



def ProblemMark(request, pk):
  post = get_object_or_404(problem, id=request.POST.get('problem_id'))
  if post.completed.filter(id=request.user.id).exists():
    post.completed.remove(request.user)
  else:
    # print("i am here")
    post.completed.add(request.user)

  return redirect(request.META.get('HTTP_REFERER'))



# def send mail after registration
def send_mail_after_registration(email,token,fname,username):
  subject ='Email address verification of Quriosity account'
  # change the verification link after uploding on the server
  message = 'Hi '+fname+',\n\n Your account has been created sucessfully with Quriosity.tech with following credentials - \n Username : '+username+'\n Email id - '+email+'\n\n Please, verify your Quriosity account by opening this link in your web browser -  https://quriosity.tech/verify/'+token+'\n\n Thank You\n\n Best Regards,\n Quriosity '
  email_from = 'noreply@quriosity.tech'
  recipient_list = [email]
  send_mail(subject, message, email_from, recipient_list,fail_silently=False)


#  function to verify the account
def verify(request, auth_token):
  try:
    received_obj = account_verification.objects.filter(auth_token = auth_token).first()
    if received_obj:
      # checking if the account is already verified
      if received_obj.verification_status:
        messages.info(request,'Your account is already verified. You can login now.')
        return redirect('log_in')
      # if the account is already not verified the do this
      received_obj.verification_status = True
      received_obj.save()
      messages.success(request,'Your account has been verified. You can login now.')
      return redirect('log_in')
    else:
      messages.error(request,'Invalid Request! Such requests will block your IP addess from Quriosity.tech!')
      return redirect('404')
  except Exception as e:
    messages.error(request,e)
  return redirect('404')


def view(request,slug):
  if request.user.id == None:
    messages.info(request, mark_safe("Please <a href='/signup'>Signup</a>/<a href='/log_in'>Login</a> to access all the features. Currently you have restricted access."))
    # return redirect('dashboard')
  # print("I am in problems view for anonymous users")
  messages.warning(request, mark_safe("Please make sure that you have <strong><a href='https://auth.geeksforgeeks.org/'>login</a></strong> to your <a href='https://auth.geeksforgeeks.org/'>geeksforgeeks</a> account in the same browser so that you can view the problems."))
  alltopic = topic.objects.all()
  top = topic.objects.filter(slug=slug).first()
  # if the slug is empty return 404
  if top is None:
    messages.error(request,"Invalid Request !")
    return redirect('404')
  # if the topic is not active return 404
  if top.active is False:
    messages.error(request,"This topic is currently not active")
    return redirect('404')
  prob = problem.objects.filter(topic=top).all().order_by('priority')
  total_problem = problem.objects.filter(topic=top).count()
  problem_solved = "NA"
  problem_unsolved = "NA"
  # print(userProbData)
  # print(top)
  # print(prob)
  # print(userProbData)
  # print(problem_unsolved)
  context = {
    'alltopic':alltopic,
    'top':top,
    'prob':prob,
    'slug':slug,
    'total_problem':total_problem,
    'problem_solved':problem_solved,
    'problem_unsolved':problem_unsolved,
  }
  # messages.info(request,"Topic --> "+top.title)
  return render(request,'view.html',context)




