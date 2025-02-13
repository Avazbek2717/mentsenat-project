from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import University, Student, Sponser, Founder

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ['-created_at',]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'university', 'need_amount', 'student_type', 'created_at')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('student_type', 'university')
    ordering = ['-created_at']

    # Admin panelga chart qo'shish uchun funksiya
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('chart/', self.admin_site.admin_view(self.chart_view), name="chart-view"),
        ]
        return custom_urls + urls

    def chart_view(self, request):
        students_count = Student.objects.count()
        sponsors_count = Sponser.objects.count()
        return render(request, "admin/chart_admin.html", {
            "students_count": students_count,
            "sponsors_count": sponsors_count,
        })

@admin.register(Sponser)
class SponserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'amount', 'type_payment', 'filter', 'role', 'created_at')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('type_payment', 'role')
    ordering = ['-created_at',]

@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'amount', 'student', 'created_at')
    search_fields = ('application__full_name', 'student__full_name')
    list_filter = ('application',)
    ordering = ['-created_at',]





