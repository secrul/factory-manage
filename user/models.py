from django.db import models
from django.contrib.auth.models import User


class Position(models.Model):
    position = models.CharField(max_length=100)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')), default='male',
                                    verbose_name='性别')
    staff_age = models.PositiveIntegerField(verbose_name="年龄")
    staff_home = models.CharField(max_length=100, verbose_name="籍贯")
    staff_nationality = models.CharField(max_length=20, verbose_name="民族")  # 民族
    staff_tel = models.BigIntegerField(verbose_name="电话")
    start_time = models.DateField(auto_now_add=True, verbose_name="入职时间")  # 入职时间
    id_card = models.CharField(max_length=20,verbose_name="身份证")  # 身份证号
    staff_type = models.CharField(max_length=100,verbose_name="职位", null=True)  # 职位

    salary_pre_hour = models.IntegerField(verbose_name="时薪")  # 时薪


    class Meta:
        ordering = ['-start_time']


class Attendance(models.Model):#考勤
    current_time = models.DateField(auto_now_add=True, verbose_name="日期")
    staff_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="姓名")
    flag_leave = models.BooleanField(default=False, verbose_name="请假")
    flag_business = models.BooleanField(default=False, verbose_name="出差")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="上班时间")
    end_time = models.DateTimeField(verbose_name="下班时间",auto_now=True)
    supplement = models.CharField(max_length=100, verbose_name="补充", null=True, default='无',blank=True)

    class Meta:
        ordering = ['-current_time']


class Salary(models.Model):#工资
    current_time = models.DateField(auto_now_add=True, verbose_name="时间")
    staff_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="姓名")
    attend_days = models.IntegerField(verbose_name="出勤", default=0)
    leave_days = models.IntegerField(verbose_name="请假", default=0)
    absent_days = models.IntegerField(verbose_name="旷班", default=0)
    business_days = models.IntegerField(verbose_name="出差", default=0)
    zaotui_days = models.IntegerField(verbose_name="早退", default=0)
    late_days = models.IntegerField(verbose_name="迟到", default=0)
    overtime = models.IntegerField(verbose_name="加班时长", default=0)
    base_salary = models.IntegerField(verbose_name="基础工资", default=0)
    overtime_salary = models.IntegerField(verbose_name="加班工资", default=0)
    kouchu = models.IntegerField(verbose_name="应扣", default=0)
    allowance = models.IntegerField(verbose_name="补贴", default=0)
    should_pay = models.IntegerField(verbose_name="应发", default=0)
    tax= models.IntegerField(verbose_name="个人所得税", default=0)
    actual_pay = models.IntegerField(verbose_name="实发", default=0)

    class Meta:
        ordering = ['-current_time']


def get_staff_gender(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        if profile.staff_gender == 'male':
            return '男'
        else:
            return '女'
    else:
        return '性别'

def set_staff_gender(self,gender):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        profile.staff_gender = gender

def get_staff_age(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.staff_age
    else:
        return ''


def set_staff_age(self,age):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        profile.staff_age = age


def get_staff_home(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.staff_home
    else:
        return ''


def set_staff_home(self, home):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        profile.staff_home = home


def get_staff_nationality(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.staff_nationality
    else:
        return ''


def set_staff_nationality(self, nation):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        profile.staff_nationality=nation


def get_staff_tel(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.staff_tel
    else:
        return ''


def set_staff_tel(self, tel):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        profile.staff_tel=tel


def get_start_time(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.start_time
    else:
        return ''


def set_start_time(self, time):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        profile.start_time=time


def get_id_card(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.id_card
    else:
        return ''


def set_id_card(self, id):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        profile.id_card=id


def get_salary_pre_hour(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.salary_pre_hour
    else:
        return ''


def set_salary_pre_hour(self, salary):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        profile.salary_pre_hour=salary


def get_staff_type(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.staff_type
    else:
        return ''


def set_staff_type(self,type):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        profile.staff_type=type


User.get_staff_age = get_staff_age
User.get_staff_gender = get_staff_gender
User.get_staff_type = get_staff_type
User.get_staff_home = get_staff_home
User.get_staff_nationality = get_staff_nationality
User.get_staff_tel = get_staff_tel
User.get_start_time = get_start_time
User.get_id_card = get_id_card
User.get_salary_pre_hour = get_salary_pre_hour

User.set_staff_age = set_staff_age
User.set_staff_gender = set_staff_gender
User.set_staff_type = set_staff_type
User.set_staff_home = set_staff_home
User.set_staff_nationality = set_staff_nationality
User.set_staff_tel = set_staff_tel
User.set_start_time = set_start_time
User.set_id_card = set_id_card
User.set_salary_pre_hour = set_salary_pre_hour
