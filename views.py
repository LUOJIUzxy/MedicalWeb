from django.shortcuts import render
from django.http import HttpResponse
import http.client
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Doctor,Department,Reservation,Patient
from urllib import parse
import sys
import urllib
import urllib.request
import http.cookiejar
import hashlib
import logging
from time import time
import random
import json
nonce = ''
curTime = ''
class SendMsgTest(object):
    """网易云信 短信模板：
    • 短信由三部分构成：签名+内容+变量
    • 短信模板示例：尊敬的%s ，您的余额不足%s元，请及时缴费。"""
    #j = 4
    #nonce = ''.join(str(i) for i in random.sample(range(0, 9), j))
    #mobile = ''
    #mobiles = ''

    def printNonce(self):
        return self.yzm
    def __init__(self,mobile,):
        super(SendMsgTest, self).__init__()
        sys.stdout.flush()
        self.cookie = http.cookiejar.CookieJar()
        self.handler = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handler)
        urllib.request.install_opener(self.opener)
        self.mobile=mobile
        self.authcode = ''.join(str(i) for i in random.sample(range(0, 9), 4))
        self.yzm = ""

    def addHeaders(self, name, value):
        self.opener.addheaders.append((name, value))

    def doPost(self, url, payload=None):
        req = urllib.request.Request(url, data=payload)
        req = self.opener.open(req)
        return req

    def checkSum(self, appSecret, curTime):
        # SHA1(AppSecret + Nonce + CurTime),三个参数拼接的字符串，
        # 进行SHA1哈希计算，转化成16进制字符(String，小写)
        s1 = appSecret + self.authcode + curTime

        #   print(s1)
        m = hashlib.sha1(s1.encode(encoding = "utf-8"))


        #s1.update(s1.encode("utf-8"))
        upwd3 = m.hexdigest()
        #print(upwd3)
        return upwd3

    def send(self):
        appSecret = '10343edf9f08'
        #j = 4
        #nonce = []
        #nonce = ''.join(str(i) for i in random.sample(range(0, 9), 4))
        curTime = str(int(time()))

        self.addHeaders("AppKey", "c039ef269e309e7ea63950a1effe4aab")
        self.addHeaders("Nonce",str(self.authcode))
        self.addHeaders("CurTime", curTime)
        self.addHeaders("CheckSum", self.checkSum(appSecret,  curTime))
        self.addHeaders("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
        #self.addHeaders("mobile","15196262983")

        templateid = '4103196'  # 模板ID
        #mobiles = "['mobliess','15196262983']"

        #authCode = self.authcode
        params = self.authcode

        # mobiles = json.dumps(data)
        #params = json.dumps(params1)
        values = {'templateid': templateid, 'mobile': self.mobile, 'params': params,'authcode':self.authcode,}
        postData = urllib.parse.urlencode(values).encode(encoding='UTF-8')
        print(postData)
        postUrl = 'https://api.netease.im/sms/sendcode.action'
        try:
            req = self.doPost(postUrl, postData)
            if 200 == req.getcode():
                res = req.read()
                data1 = json.loads(res)
                self.yzm = data1["obj"]

                print (res)
                # 成功返回{"code":200,"msg":"sendid","obj":8}
                # 主要的返回码200、315、403、413、414、500
                # 详情：http://dev.netease.im/docs?doc=server&#code状态表
            else:
                print (req.getcode())

        except (Exception) as e:
            print (logging.exception(e))

class SendMsgTest2(object):
    API_URL = "https://sms.dun.163yun.com/v2/sendsms"
    VERSION = "v2"
    def __init__(self):
        """
        Args:
        secret_id (str) 产品密钥ID，产品标识
        secret_key (str) 产品私有密钥，服务端生成签名信息使用
        business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = "5f9007833c0aaf510e172d5b8f5f4182"
        self.secret_key = "68fce3435856a96250c27e831125a9a4"
        self.business_id = "17cb50d4e9de42ef99e4f7f0c2d4729c"
    def gen_singnature(self,params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff.encode('utf8')).hexdigest()
    def sned(self,params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        curTime = str(int(round(time() * 1000)))
        #curTime = str(int(time()*1000))
        params["timestamp"] = curTime
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = self.gen_singnature(params)

        try:
            params = urllib.parse.urlencode(params).encode(encoding='UTF8')
            request = urllib.request.Request(self.API_URL, params)
            content = urllib.request.urlopen(request, timeout=1).read()
            return json.loads(content)
        except (Exception) as ex :
            print("调用API接口失败:",str(ex))



def home(request):
    departments = Department.objects.all()
    if 'islogined' in request.session:
        islogined = request.session.GET['islogined']
    else:
        islogined = False
    return render(request,'home.html',{'departments':departments,'islogined':islogined,})
def doctor_list(request,department_id):
    department_ = Department.objects.get(depart_id = department_id)
    doctors = Doctor.objects.filter(department=department_)
    return render(request, 'departmentview.html', {'doctors':doctors,'department':department_,})
def doctor_detail(request,doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    id = str(doctor.dor_id)
    imgurl = "/static/images/doc"+id+".jpg"
    return render(request, 'reservation.html', {'doctor':doctor,'imgurl':imgurl,})
def reservation(request):
    if not request.user.is_authenticated:
        result="您还没有登录，请先登录"
        return render(request, 'nologin.html', {'result': result, })
    else:
        doc_id=request.GET['dor_id']
        doctor = Doctor.objects.get(dor_id=doc_id)
        thetime = request.GET['thetime']
        month = thetime[5:8]
        day = thetime[8:11]
        time = thetime[12:15]
        tel_num = request.user.username
        try:
            Reservation.objects.get(DocID=doctor,month=month,day=day,time=time)
            result = "该时间段已被预约！请重新选择时间"
            return render(request,'fa_result.html',{'result':result,'doctor':doctor,})
        except Reservation.DoesNotExist:
            reservation = Reservation()
            reservation.DocID = doctor
            reservation.PatID = Patient.objects.get(tel_num=tel_num)
            reservation.month=month
            reservation.day=day
            reservation.time=time
            reservation.save()
            result = "预约成功！"
            return render(request, 're_result.html', {'result': result, })
def search(request):             #搜索视图
    if 'text' in request.GET and request.GET['text']:
        q = request.GET['text']
        doctor = Doctor.objects.get(name=q)
        id=str(doctor.id)
        url="/doctors/"+id
        return HttpResponseRedirect(url)
    else:
        return render(request,'home.html')

def yanzheng(request):
    """"
    tel_num= request.GET['tel_num']
    sendTest = SendMsgTest(str(tel_num))
    sendTest.send()
    zyz = sendTest.printNonce()
    print("&&&&7"+zyz)
    return render(request,'register.html',{'telnum':tel_num,'tel_num':tel_num,'zyz':zyz})
    """
    tel_num = request.GET['tel_num']
    api = SendMsgTest2()
    code = ''.join(str(random.choice(range(10))) for _ in range(5))
    zyz = code
    params = {
        "needUp": "false",
        "mobile": str(tel_num),
        "templateId": "10183",
        "params": "code=%s"%code
    }
    ret = api.sned(params)
    if ret is not None:
        if ret["code"] == 200:
            taskId = ret["data"]["result"]
            print("taskId = %s" % taskId)
        else:
            print("ERROE:ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
    return render(request, 'register.html', {'telnum': tel_num, 'tel_num': tel_num, 'zyz': zyz})

def register(request):
    # realname = request.GET['username1']
        tel_num = request.GET['telnum']
        yz_num = request.GET['yz_num']
        print ("$$$$" + yz_num)
        nonce = request.GET['zyz']
        print ("#####" + nonce)
        if yz_num == nonce:
            idnumber = request.GET['idnumber']
            password = request.GET['password']
            realname = request.GET['realname']
            gender = request.GET['gender']
            User.objects.create_user(username=tel_num, password=password)
            user = auth.authenticate(username=tel_num, password=password)
            auth.login(request, user)
            patient = Patient()
            patient.name = realname
            patient.tel_num = tel_num
            patient.idnumber = idnumber
            patient.gender = gender
            patient.save()
            result = "注册成功！"
            return  render(request,'register_re.html',{'result':result})

        else:
            return HttpResponse('验证码错误')
def text(request):
    return render(request,'register.html')

def login(request):
    return  render(request,'log.html')
def loginsend(request):
    tel_num= request.GET['tel_num']
    sendTest = SendMsgTest(str(tel_num))
    sendTest.send()
    zyz = sendTest.printNonce()
    print("&&&&7"+zyz)
    return render(request,'log.html',{'telnum':tel_num,'tel_num':tel_num,'zyz':zyz})
def loginsend2(request):
    tel_num = request.GET['tel_num']
    api = SendMsgTest2()
    code = ''.join(str(random.choice(range(10))) for _ in range(5))
    params = {
        "needUp": "false",
        "mobile": str(tel_num),
        "templateId": "10183",
        "params": "code=%s" % code
    }
    ret = api.sned(params)
    if ret is not None:
        if ret["code"] == 200:
            taskId = ret["data"]["result"]
            print("taskId = %s" %taskId)
        else:
            print("ERROE:ret.code=%s,msg=%s"%(ret['code'],ret['msg']))
    return render(request, 'log.html', {'telnum': tel_num, 'tel_num': tel_num, 'zyz': code})

def fastlogin(request):
        tel_num = request.GET['telnum']
        nonce = request.GET['zyz']
        yz_num=request.GET['yz_num']
        if yz_num==nonce:
            user = User.objects.get(username=tel_num)
            auth.login(request, user)
            request.session['iglogined'] = True
            return  render(request, 'home.html')
        else:
            request.session['iglogined'] = False
            result ="验证码错误！"
            return render(request, 'login_result.html', {'result': result, })
def normallogin(request):
     tel_num = request.GET['tel_num']
     password = request.GET['password']
     user = auth.authenticate(username=tel_num, password=password)
     if user is not None:
        auth.login(request,user)
        request.session['iglogined']=True
        return render(request,'home.html')
     else:
         request.session['iglogined'] = False
         result = '用户名或密码错误'
         return render(request, 'login_result.html', {'result': result, })
def logout(request):
    auth.logout(request)
    return HttpResponse('已登出')

def person(request):

    if not request.user.is_authenticated:
        result="您还没有登录，请先登录"
        return render(request, 'nologin.html', {'result': result, })
    else:
       #tel = request.GET['username']
       tel = request.user.username
       patient = Patient.objects.get(tel_num=tel)
       try:
          reservations =  Reservation.objects.filter(PatID=patient)
          return render(request, 'personal.html', {'user': patient, 'reservations': reservations, })
       except Reservation.DoesNotExist:
           re = None
           return render(request, 'personal.html', {'user': patient, 're': re, })


