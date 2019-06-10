from django.contrib import admin
from .models import Profile, Salary, Attendance,Position
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'id', 'staff_type', "staff_gender", "staff_age", "staff_home", "staff_nationality",
                    "staff_tel", "email", "start_time", "id_card", "salary_pre_hour", 'is_staff', 'is_active', 'is_superuser')

    def staff_type(self, obj):
        return obj.profile.staff_type
    staff_type.short_description = '职位'

    def staff_gender(self, obj):
        if obj.profile.staff_gender == 'male':
            return '男'
        return '女'
    staff_gender.short_description = '性别'

    def staff_age(self, obj):
        return obj.profile.staff_age
    staff_age.short_description = '年龄'

    def staff_home(self, obj):
        return obj.profile.staff_home
    staff_home.short_description = '籍贯'

    def staff_nationality(self, obj):
        return obj.profile.staff_nationality
    staff_nationality.short_description = '民族'

    def staff_tel(self, obj):
        return obj.profile.staff_tel
    staff_tel.short_description = '联系电话'

    def start_time(self, obj):
        return obj.profile.start_time
    start_time.short_description = '入职时间'

    def id_card(self, obj):
        return obj.profile.id_card
    id_card.short_description = '身份证号'

    def salary_pre_hour(self, obj):
        return obj.profile.salary_pre_hour
    salary_pre_hour.short_description = '时薪'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', "staff_gender", "staff_age", "staff_home", "staff_nationality", "staff_tel", "start_time")


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ("current_time", "staff_name", "attend_days", "leave_days", "absent_days", "business_days", "late_days",
                    "overtime", "base_salary", "overtime_salary", "kouchu",
                    "allowance", "should_pay", "tax", "actual_pay")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("current_time", "staff_name", "flag_leave", "flag_business", "start_time", "end_time", "supplement")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "position")
