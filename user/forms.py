from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import widgets
from .models import Position

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='姓名或身份证号',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入姓名或身份证号'})
    )
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=30,
        min_length=3,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位用户名'})
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'})
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'})
    )
    password_again = forms.CharField(
        label='再输入一次密码',
        min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输入一次密码'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断验证码
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(
        label='新的昵称',
        max_length=20,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的昵称'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError("新的昵称不能为空")
        return nickname_new

class BindEmailForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'请输入正确的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')

        # 判断用户是否已绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧的密码',
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入旧的密码'}
        )
    )
    new_password = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的密码'}
        )
    )
    new_password_again = forms.CharField(
        label='请再次输入新的密码',
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请再次输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证新的密码是否一致
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        return old_password

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'请输入绑定过的邮箱'}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )
    new_password = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        # 判断验证码
        code = self.request.session.get('forgot_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code


class UserModifyForm(forms.Form):
    ps = Position.objects.all()
    posit = []
    for p in ps:
        posit.append((p.position, p.position))
    username = forms.CharField(
        label='姓名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓名'})
    )
    type = forms.CharField(
        label='职位',
        widget=forms.Select(choices=posit)
    )
    gender = forms.ChoiceField(
        label='性别',
        initial='male',
        widget=widgets.RadioSelect,
        choices=(('male', '男'), ('female', '女'))
    )
    age = forms.CharField(
        label='年龄',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入年龄'})
    )
    home = forms.CharField(
        label='籍贯',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入籍贯'})
    )
    nationality = forms.CharField(
        label='民族',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入民族'})
    )
    phone = forms.CharField(
        label='电话',
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入11位电话'})
    )
    id_card = forms.CharField(
        label='身份证号',
        max_length=18,
        min_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入18位身份证号'})
    )
    start_time = forms.CharField(
        label='入职时间',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入入职时间'})
    )
    salary_pre_hour = forms.CharField(
        label='时薪',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入时薪'})
    )
    password = forms.CharField(label='密码',
                               required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))


class UserAppendForm(forms.Form):
    ps = Position.objects.all()
    posit = []
    for p in ps:
        posit.append((p.position, p.position))
    username = forms.CharField(
        label='姓名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓名'})
    )
    type = forms.CharField(
        label='职位',
        widget=forms.Select(choices=posit),
    )
    gender = forms.ChoiceField(
        label='性别',
        initial='male',
        widget=widgets.RadioSelect,
        choices=(('male','男'),('female','女'))
    )
    age = forms.CharField(
        label='年龄',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入年龄'})
    )
    home = forms.CharField(
        label='籍贯',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入籍贯'})
    )
    nationality = forms.CharField(
        label='民族',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入民族'})
    )
    phone = forms.CharField(
        label='电话',
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入11位电话'}),
    )
    id_card = forms.CharField(
        label='身份证号',
        max_length=18,
        min_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入18位身份证号'})
    )
    salary_pre_hour = forms.CharField(
        label='时薪',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入时薪'})
    )
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))


class StaffTypeForm(forms.Form):
    position = forms.CharField(
        label='职位',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入职位'})
    )


class AttendenceForm(forms.Form):
    staff_name= forms.CharField(
        label='姓名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓名'})
    )
    flag_leave=  forms.ChoiceField(
        label='请假',
        initial='False',
        widget=widgets.RadioSelect,
        choices=(('False', '否'), ('True', '是'))
    )
    flag_business= forms.ChoiceField(
        label='出差',
        initial='False',
        widget=widgets.RadioSelect,
        choices=(('False','否'),('True','是'))
    )
    supplement= forms.CharField(
        label='说明',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入说明'})
    )


class UserSelectForm(forms.Form):
    keyword = forms.CharField(
        label='关键字段',
        widget=forms.Select(choices=((1,'姓名'),(2,'职位'),(3,'性别'),(4,'年龄'),(5,'籍贯'),(6,'民族'),(7,'电话'),
                                     (8,'身份证号'),(9,'入职时间'),(10,'时薪')))
    )
    valueword = forms.CharField(
        label='内容',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查询内容'})
    )

class UserNormalSelectForm(forms.Form):
    keyword = forms.CharField(
        label='关键字段',
        widget=forms.Select(choices=((1,'姓名'),(2,'职位'),(3,'性别'),(4,'年龄'),(5,'籍贯'),(6,'民族'),(7,'电话')))
    )
    valueword = forms.CharField(
        label='内容',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查询内容'})
    )


class AttendenceSelectForm(forms.Form):

    keyword = forms.CharField(
        label='关键字段',
        widget=forms.Select(choices=((1,'姓名'),(2,'日期')))
    )
    valueword = forms.CharField(
        label='内容',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查询内容'})
    )


class AttendenceNormalSelectForm(forms.Form):

    keyword = forms.CharField(
        label='时间',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入时间'})
    )



class SalarySelectForm(forms.Form):

    keyword = forms.CharField(
        label='关键字段',
        widget=forms.Select(choices=((1,'姓名'),(2,'日期'),(3,'出勤天数'),(4,'请假天数'),(5,'旷班天数'),(6,'出差天数'),
                                     (7,'迟到天数'),(8,'加班时长'),(9,'基础工资'),(10,'加班工资'),(11,'扣款'),(12,'补贴'),
                                     (13,'应发'),(14,'个人所得税'),(15,'实发')))
    )
    flag = forms.CharField(
        label='符号',
        widget=forms.Select(choices=((1,'等于'),(2,'大于等于'),(3,'小于等于')))
    )
    valueword = forms.CharField(
        label='内容',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查询内容'})
    )


class SalaryNormalSelectForm(forms.Form):

    valueword = forms.CharField(
        label='日期',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入查询日期'})
    )