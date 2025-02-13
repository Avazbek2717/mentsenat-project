from rest_framework import serializers
from app.models import Founder,Sponser,Student,University

from django.db.models import Sum
import re

class StudentSponsorUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Founder
        fields = ("application", 'amount')

    def update(self, instance, validated_data):
        student = instance.student
        student_total_received = student.students.aggregate(total=Sum('amount'))['total'] or 0

        if "amount" in validated_data and "application" in validated_data: 
            if validated_data['application'] == instance.application and validated_data['amount'] != instance.amount:
                sponsor_amount = instance.application.amount
                allocated_amount = instance.application.sponsers.aggregate(total=Sum('amount'))['total'] or 0 - instance.amount
                if sponsor_amount - allocated_amount < validated_data['amount']:
                    raise serializers.ValidationError({
                        'error': f"Bu homiyda {sponsor_amount - allocated_amount} so'm qoldiq mavjud"
                    })
                if student.need_amount - student_total_received - instance.amount < validated_data['amount']:
                    raise serializers.ValidationError({
                        'error': f"Bu talabaga {student.need_amount - student_total_received - instance.amount} so'm berish mumkin"
                    })

            elif validated_data['application'] != instance.application and validated_data['amount'] == instance.amount:
                application = validated_data['application']
                application_spent_amount = application.sponsers.aggregate(total=Sum('amount'))['total'] or 0
                if application.amount - application_spent_amount < instance.amount:
                    raise serializers.ValidationError({
                        'error': f"Bu homiyda {application.amount - application_spent_amount} so'm  mavjud"
                    })
                    
            elif validated_data['application'] != instance.application and validated_data['amount'] != instance.amount:
                application = validated_data['application']
                application_spent_money = application.sponsers.aggregate(total=Sum('amount'))['total'] or 0

                if application.amount - application_spent_money < validated_data['amount']:
                    raise serializers.ValidationError({
                        'error': f"Bu homiyda {application.amount - application_spent_money} so'm  mavjud"
                    })

                if student.need_amount - (student_total_received - instance.amount) < validated_data['amount']:
                    raise serializers.ValidationError({
                        'error': f"Bu talabaga {student.need_amount - (student_total_received - instance.amount)} so'm  berish mumkin"
                    })

        return super().update(instance, validated_data)

class StudentSponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Founder
        fields = "__all__"

    def validate(self, attrs):
        student = attrs.get('student')
        sponsor = attrs.get('application')
        amount = attrs.get('amount')

        # studentga ortiqcha pul berish holati 
        student_received_money = student.students.aggregate(total=Sum('amount'))['total'] or 0
        diff = student.need_amount - student_received_money
        if diff < amount:
            raise serializers.ValidationError({
                'error': f"Bu ta'labaga maksimal miqdorda {diff} so'm pul ajrata olasiz"
            })

        # va sponsorda pul yetishmasligi
        sponsor_spent_money = sponsor.sponsers.aggregate(total=Sum('amount'))['total'] or 0
        diff = sponsor.amount - sponsor_spent_money 
        if diff < amount:
            raise serializers.ValidationError({
                'error': f"Bu homiyada {diff} so'm miqdorida pul qo'lgan"
            })
        return super().validate(attrs)

class SponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponser
        fields = ('full_name', 'phone_number', 'amount', 'work_palce', 'role')

    # post, putch, put
    def validate(self, attrs):
        type = attrs.get('role')
        org_name = attrs.get('work_palce')
        if type == 'jismoniy shaxs' and org_name:
            raise serializers.ValidationError({
                'error': "Jismoniy shahslar uchun organizatsiya nomi kiritish mumkin emas"
            }, code=400)

        if type == 'yurudik shaxs' and not org_name:
            raise serializers.ValidationError({
                'error': "Yuridik  shahslar uchun organizatsiya nomi kiritish majburiy"
            }, code=400)
        return super().validate(attrs)



class SponsorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponser 
        fields = '__all__'  


class StudentSerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(source='university.name', read_only=True)
    allocated_amount = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'student_type', 'university_name', 'need_amount', 'allocated_amount']

    def get_allocated_amount(self, obj):
        total_amount = Founder.objects.filter(student=obj).aggregate(total=Sum('amount'))['total']
        return total_amount if total_amount else 0



class SponserSerializer(serializers.ModelSerializer):
    allocated_amount = serializers.SerializerMethodField()

    class Meta:
        model = Sponser
        fields = ['id', 'full_name', 'phone_number', 'amount', 'filter', 'allocated_amount']

    def get_allocated_amount(self,obj):
        total_amount = Founder.objects.filter(application = obj).aggregate(total=Sum('amount'))['total']
        return total_amount if total_amount else 0
    


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate(self, attrs):
        full_name  = attrs.get('full_name')
        phone_number = attrs.get('phone_number')
        pattern = r"^\+998\d{9}$"
        if not str(full_name).isalpha():
            raise serializers.ValidationError({"error": "Ism faqatgina harflar orqali ifodalang"})
        elif not re.fullmatch(pattern,phone_number):
            raise serializers.ValidationError({'error': "Telefon raqam notori kiritilgan"})
        return super().validate(attrs)
    

class StudentSponserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Founder
        fields =  '__all__'

    
class StudentUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = '__all__'

    def validate(self, attrs):
        full_name = attrs.get('full_name')
        phone_number = attrs.get('phone_number')
        amount = attrs.get('need_amount')
        pattern = r"^\+998\d{9}$"
        if not str(full_name).isalpha():
            raise serializers.ValidationError({"error": "Ism faqatgina harflar orqali ifodalang"})
        elif not re.fullmatch(pattern,phone_number):
            raise serializers.ValidationError({'error': "Telefon raqam notori kiritilgan"})
    
        return super().validate(attrs)
        