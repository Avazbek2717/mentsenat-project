from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .models import Sponser, Founder,Student
from rest_framework import generics
from rest_framework.views import Response
from serializers import StudentSponsorSerializer,SponsorSerializer,StudentSponsorUpdateSerializer,SponsorListSerializer ,StudentSerializer,SponserSerializer,StudentCreateSerializer,StudentUpdateSerializer
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Sum,Count
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
from .permisson import CustomPermession


class SponsorListCreateAPIView(generics.ListCreateAPIView):
    filter_backends=[DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ( 'amount',)
    search_fields = ['full_name', 'phone']
    authentication_classes = [TokenAuthentication,SessionAuthentication]

    def get_queryset(self):
        return Sponser.objects.all()

    def get_serializer_class(self):
        return SponsorSerializer if self.request.method == 'POST' else SponsorListSerializer
    
    def get_permissions(self):
        if self.request.method  == 'POST':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [CustomPermession]
        return super().get_permissions()
    
    



class SponsorDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Sponser.objects.all()
    serializer_class = SponsorListSerializer




class StudentSponsorCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = StudentSponsorSerializer



class StudentSponsorUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = Founder.objects.all()
    serializer_class = StudentSponsorUpdateSerializer


class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SposorListAPIView(generics.ListAPIView):
    queryset = Sponser.objects.all()
    serializer_class  = SponserSerializer

class DashboadGraphAPIView(APIView):
    
    def get(self, request):
        this_year = timezone.now().year


        students_per_month = (
            Student.objects.filter(created_at__year = this_year).annotate(month = TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month') 
        )
        sponser_per_month = (
            Sponser.objects.filter(created_at__year = this_year).annotate(month = TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month') 
        )

        formatted_data_sponser = [
            {"month": entry["month"].strftime("%Y-%m-%d"), "count": entry["count"]}
            for entry in sponser_per_month
        ]

        formatted_data_student = [
            {"month": entry['month'].strftime("%Y-%m-%d"), "count": entry["count"]}
            for entry in students_per_month
        ]

        response_date= {
            "Sponser": formatted_data_sponser,
            "Student": formatted_data_student,
        }

        return Response(response_date)


class DashboardStatsAPIView(generics.ListAPIView):
        def get(self, request, *args, **kwargs):
        
            total_paid = Founder.objects.aggregate(total=Sum("amount"))["total"] or 0
            total_requested = Student.objects.aggregate(total=Sum("need_amount"))["total"] or 0
            total_remaining = total_requested - total_paid

            return Response({
                "total_paid": total_paid,
                "total_requested": total_requested,
                "total_remaining": total_remaining
            })





class StudentCreate(generics.ListCreateAPIView):
    queryset =  Student.objects.all()
    serializer_class = StudentCreateSerializer
    filter_backends=[DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('full_name', 'need_amount')
    search_fields = ['full_name', 'phone_number']


class StudentSponsor(APIView):
    def get(self,request,pk):
        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return Response(data={'error': 'Bunday foydalanuvchi mavjud emas'},status=400)
        founders = Founder.objects.filter(student=student) 

        sponsers = [founder.application for founder in founders]  

        return Response({
            "student": StudentSerializer(student).data,
            "sponsers": SponserSerializer(sponsers, many=True).data 
        })

class StudentUpdate(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    lookup_field = 'pk'
    