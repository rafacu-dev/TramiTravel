
import json
import random
import threading

from django.conf import settings
from django.shortcuts import HttpResponse, redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import View
from django.contrib.auth import logout,authenticate,login
from django.core.mail import send_mail

from apps.user.models import ConfirmCode, UserAccount, RecreatePassword as RecreatePsw

class Login(View):
    def post(self,request,*args,**kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            request.user = user
            csrf = str(render(request,"csrf.html").content).replace('''b'<input type="hidden" name="csrfmiddlewaretoken" value="''',"").replace("""">'""","")

            data = json.dumps({
                "login":"success",
                "csrf":csrf,
                "user":user.__str__()
                })
            return HttpResponse(data,"application/json")
        else:
            data =json.dumps({"login":"error"})
            return HttpResponse(data,"application/json")

class Register(View):
    def post(self,request,*args,**kwargs):
        email = request.POST['email']
        password = request.POST['password']

        userexist = UserAccount.objects.filter(email=email)
        if len(userexist) > 0:
            data =json.dumps({"register":"user-exists"})
            return HttpResponse(data,"application/json")


        userRegister = UserAccount.objects.create_user(email=email, password=password)
        userRegister.is_active = False
        userRegister.save()

        user = authenticate(request, email=email, password=password)

        if userRegister is not None:
            confirmCodes = ConfirmCode.objects.filter(email=email)
            for code in confirmCodes:
                code.delete()

            
            code = f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
            t = threading.Thread(target=lambda:send_email_code(code,email))
            t.start()
            
            ConfirmCode.objects.create(email=email, code=code)

            data = json.dumps({
                "register":"success",
                })
            return HttpResponse(data,"application/json")
        else:
            data =json.dumps({"register":"error"})
            return HttpResponse(data,"application/json")

class RecreatePassword(View):
    def post(self,request,*args,**kwargs):
        try:
            email = request.POST['email']
            password = request.POST['password']

            userRegister = UserAccount.objects.filter(email=email)
            if not userRegister.exists():
                data =json.dumps({"recreate":"user-no-registered"})
                return HttpResponse(data,"application/json")

            else:
                userRegister = userRegister[0]
                confirmCodes = RecreatePsw.objects.filter(user=userRegister)
                for code in confirmCodes:
                    code.delete()

                code = f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
                t = threading.Thread(target=lambda:send_email_code(code,email))
                t.start()
                
                rp = RecreatePsw.objects.create(user=userRegister, code=code, password=password)
                rp.save()

                data = json.dumps({
                    "recreate":"success",
                    })
                return HttpResponse(data,"application/json")
        except:
            data =json.dumps({"recreate":"error"})
            return HttpResponse(data,"application/json")

class RegisterConfirm(View):
    def post(self,request,*args,**kwargs):
        email = request.POST['email']
        code = request.POST['code']
        
        confirmCode = ConfirmCode.objects.filter(email=email,code=code)
        if not confirmCode.exists():
            if ConfirmCode.objects.filter(email=email).exists():
                confirmCode = ConfirmCode.objects.get(email=email)
                
                if confirmCode.failures == 2:
                    confirmCode.delete()
                    UserAccount.objects.get(email=email).delete()
                    data =json.dumps({"register":"many-failures"})
                    return HttpResponse(data,"application/json")

                confirmCode.failures += 1
                confirmCode.save()


            data =json.dumps({"register":"error-code"})
            return HttpResponse(data,"application/json")
        
        else:
            confirmCode.delete()

        user = UserAccount.objects.get(email=email)

        if user is not None:
            user.is_active = True
            user.save()
            login(request, user)

            request.user = user
            csrf = str(render(request,"csrf.html").content).replace('''b'<input type="hidden" name="csrfmiddlewaretoken" value="''',"").replace("""">'""","")

            data = json.dumps({
                "register":"success",
                "csrf":csrf,
                "user":user.__str__()
                })
            return HttpResponse(data,"application/json")
        else:
            data =json.dumps({"register":"error"})
            return HttpResponse(data,"application/json")

class RecreateConfirm(View):
    def post(self,request,*args,**kwargs):
        try:
            email = request.POST['email']
            code = request.POST['code']
            
            user = UserAccount.objects.get(email=email)
            
            confirmCode = RecreatePsw.objects.filter(user=user,code=code)
            if not confirmCode.exists():
                if RecreatePsw.objects.filter(user=user).exists():
                    confirmCode = RecreatePsw.objects.filter(user=user)
                    
                    if confirmCode.failures == 2:
                        confirmCode.delete()
                        data =json.dumps({"register":"many-failures"})
                        return HttpResponse(data,"application/json")

                    confirmCode.failures += 1
                    confirmCode.save()


                data =json.dumps({"register":"error-code"})
                return HttpResponse(data,"application/json")
            
            else:

                user.set_password(confirmCode[0].password)
                user.save()
                login(request, user)
                confirmCode.delete()

                request.user = user
                csrf = str(render(request,"csrf.html").content).replace('''b'<input type="hidden" name="csrfmiddlewaretoken" value="''',"").replace("""">'""","")
                

                data = json.dumps({
                    "register":"success",
                    "csrf":csrf,
                    "user":user.__str__()
                    })
                return HttpResponse(data,"application/json")

        except:
            data =json.dumps({"register":"error-code"})
            return HttpResponse(data,"application/json")

class Logout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return  redirect("index")
    


def send_email_code(code,email):

    subject = 'Confirmaci??n de registro'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    
    # Contenido HTML del correo electr??nico
    context = {
        'code': code
        }
    html_content = render_to_string('emails/email_template.html', context)
    message = strip_tags(html_content)        
    send_mail(subject, message, email_from, recipient_list)