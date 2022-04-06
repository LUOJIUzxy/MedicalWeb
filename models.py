
# Create your models here.
from django.db import models
from django.urls import reverse
class Department(models.Model):
    depart_id = models.IntegerField(max_length=10)#科室编号
    name = models.CharField(max_length= 10)
    describe = models.CharField(max_length=120,null=True)#部门简介
    def __str__(self):
        return self.name
    def get_next_url(self):
        return reverse('department',args=(self.id,))

class Doctor(models.Model):
    dor_id = models.IntegerField(max_length=20)#医生id
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    speciality = models.CharField(max_length=30,null=True)
    describe = models.CharField(max_length=200, null=True)
   # DocID = models.IntegerField()
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('doctor',args=(self.id,))

class Patient(models.Model):
   # PatId = models.IntegerField()
    tel_num = models.IntegerField(max_length=20)#电话号码
    name = models.CharField(max_length=30)
    idnumber = models.IntegerField(max_length=15)#身份证号
    gender = models.CharField(max_length=10)
    #MedcardID = models.ForeignKey(Medcard)
    MedcardID = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.tel_num
class Medcard(models.Model):
  #  MedcardID = models.IntegerField()
    PatID = models.ForeignKey(Patient,on_delete=models.CASCADE)
    medHistory = models.CharField(max_length=50)

class Reservation(models.Model):
  #  ResID = models.IntegerField()
    DocID = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    PatID = models.ForeignKey(Patient,on_delete=models.CASCADE)
    month = models.CharField(max_length=3)   #月
    day = models.CharField(max_length=3) #具体日期
    time = models.CharField(max_length=12)#详细时间，例如13：00-14:00

