from django.db import models

from django.db import models



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 



class University(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Student(BaseModel):
    STUDENT_TYPES = [
        ('bakalavr', 'Bakalavr'),
        ('magister', 'Magistr'),
        ('phd', 'PhD'),
    ]

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20) 
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    need_amount = models.IntegerField()
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPES)

    def __str__(self):
        return self.full_name



class Sponser(BaseModel):
    PAYMENT_TYPES = [
        ("pul kochirish", "Pul ko'chirish"),
        ('plastik karta', 'Plastik karta'),
        ('naqd pul', 'Naqd Pul'),
    ]

    ROLES = [
        ('jismoniy shaxs', 'Jismoniy shaxs'),
        ('yurudik shaxs', 'Yuridik shaxs'),
    ]

    FILTER = [
        ("yangi","Yangi"),
        ('moderatsiyada',"Moderatsiyada"),
        ('tasdiqlangan','Tasdiqlangan'),
        ('bekor qilingan','Bekor qilingan')
    ]

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    amount = models.IntegerField()
    type_payment = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    description = models.TextField()
    role = models.CharField(max_length=20, choices=ROLES)
    filter = models.CharField(max_length=200,choices=FILTER)
    work_palce = models.CharField(max_length=300,null=True,blank=True)
    def __str__(self):
        return self.full_name


class Founder(BaseModel):
    application = models.ForeignKey('Sponser', on_delete=models.CASCADE,related_name='sponsers')
    amount = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='students')

    def __str__(self):
        return f"{self.application.full_name} -> {self.student.full_name}"



