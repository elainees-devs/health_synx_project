# users/views.py
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models import User
from users.permissions import RolePermission
from departments.models import Department
from pharmacy.models import Medicine
from patients.models import DoctorQueue, Prescription
from billing.models import BillingRecord
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserSerializer,
)


# -------------------------------
# Redirect after login
# -------------------------------
@login_required
def redirect_after_login(request):
    """
    Redirect users after login based on their role.
    """
    user = request.user
    role = user.role.lower()
    
    if role == 'nurse':
        return redirect('nurse_dashboard')
    elif role == 'doctor':
        return redirect('doctor_dashboard')
    elif role == 'hospital_admin':
        return redirect('hospital_admin_dashboard')
    elif role == 'patient':
        return redirect('patient_dashboard')
    else:
        return redirect('login')  # fallback
    
@csrf_exempt
def logout_view(request):
    """Allow GET logout for Swagger UI convenience."""
    logout(request)
    return redirect('/swagger/')

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Login and obtain JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="JWT token pair",
                examples={
                    "application/json": {
                        "refresh": "<refresh_token>",
                        "access": "<access_token>",
                        "user": {"id": 1, "username": "doctor1", "email": "doctor@example.com"}
                    }
                }
            ),
            401: "Invalid credentials"
        }
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {"id": user.id, "username": user.username, "email": user.email}
        })


# -------------------------------
# Register a new user
# -------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user via API"""
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": f"Account {user.username} created successfully!"
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# Login user
# -------------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Authenticate user by username or email"""
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username_or_email = serializer.validated_data['username']
    password = serializer.validated_data['password']

    # Try username
    user = authenticate(request, username=username_or_email, password=password)

    # Try email
    if user is None:
        try:
            user_obj = User.objects.get(email=username_or_email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass

    if user is None:
        return Response({"error": "Invalid username/email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    login(request, user)
    return Response({"message": "Login successful", "user": UserSerializer(user).data})


# -------------------------------
# Logout user
# -------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logout current user"""
    logout(request)
    return Response({"message": "Logged out successfully"})


# -------------------------------
# Doctor Dashboard
# -------------------------------
class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    @swagger_auto_schema(
        operation_summary="Get Doctor Dashboard",
        responses={200: openapi.Response(
            description="Doctor dashboard data",
            examples={
                "application/json": {
                    "total_patients": 5,
                    "queue": [{"id": 1, "patient__name": "John Doe", "status": "waiting"}]
                }
            }
        )}
    )
    def get(self, request):
        request.allowed_roles = ['doctor']
        queue = DoctorQueue.objects.filter(status__in=['waiting', 'with_doctor']).order_by('created_at')

        queue_list = [
        {  
            "id": q.id,
            "patient_name": f"{q.patient.first_name} {q.patient.last_name}" if q.patient.   first_name else q.patient.username,
            "status": q.status,
            "created_at": q.created_at
        }
            for q in queue
    ]

        return Response({
        "total_patients": queue.count(),
        "queue": queue_list
    })



# -------------------------------
# Nurse Dashboard
# -------------------------------
class NurseDashboardView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    @swagger_auto_schema(
        operation_summary="Get Nurse Dashboard",
        responses={200: "Welcome Nurse! Dashboard ready."}
    )
    def get(self, request):
        request.allowed_roles = ['nurse']
        return Response({"message": "Welcome Nurse! Dashboard ready."})


# -------------------------------
# Hospital Admin Dashboard
# -------------------------------
class HospitalAdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    @swagger_auto_schema(
        operation_summary="Get Hospital Admin Dashboard",
        responses={200: "Departments and staff counts"}
    )
    def get(self, request):
        request.allowed_roles = ['hospital_admin']
        return Response({
            "departments": Department.objects.count(),
            "staff_count": User.objects.count()
        })

# -------------------------------
# Hospital Admin: Register Patient
# -------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated, RolePermission])
def register_patient(request):
    """
    Allow only Hospital Admins to register new patients.
    """
    request.allowed_roles = ['hospital_admin']  # RolePermission ensures access

    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        # Force the role to 'patient' regardless of input
        serializer.save(role='patient')
        return Response({"message": "Patient registered successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------
# Pharmacy Dashboard
# -------------------------------
class PharmacyDashboardView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    @swagger_auto_schema(
        operation_summary="Get Pharmacy Dashboard",
        responses={200: "Pharmacy stock and pending prescriptions"}
    )
    def get(self, request):
        request.allowed_roles = ['pharmacist']
        
        medicines = Medicine.objects.all()
        low_stock = medicines.filter(stock__lte=10).count()
        expired = [med.name for med in medicines if med.is_expired()]
        
        prescriptions = Prescription.objects.filter(status='pending').order_by('-date_issued')
        
        pending_prescriptions = [
            {
                "id": p.id,
                "patient_name": f"{p.patient.first_name} {p.patient.last_name}" if p.patient.first_name else p.patient.username,
                "status": p.status,
                "date_issued": p.date_issued
            }
            for p in prescriptions
        ]
        
        return Response({
            "total_medicines": medicines.count(),
            "low_stock": low_stock,
            "expired_medicines": expired,
            "pending_prescriptions": pending_prescriptions
        })



# -------------------------------
# Billing Dashboard
# -------------------------------
class BillingDashboardView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    @swagger_auto_schema(
        operation_summary="Get Billing Dashboard",
        responses={200: "Billing summary"}
    )
    def get(self, request):
        request.allowed_roles = ['admin', 'billing']

        total_bills = BillingRecord.objects.count()
        total_pending = BillingRecord.objects.filter(paid=False).count()
        total_collected = BillingRecord.objects.filter(paid=True).aggregate(Sum('amount'))['amount__sum'] or 0

        recent_bills_qs = BillingRecord.objects.order_by('-created_at')[:5]

        recent_bills = [
            {
                "id": bill.id,
                "patient_name": f"{bill.patient.first_name} {bill.patient.last_name}" if bill.patient.first_name else bill.patient.username,
                "amount": bill.amount,
                "paid": bill.paid,
                "created_at": bill.created_at
            }
            for bill in recent_bills_qs
        ]

        return Response({
            "total_bills": total_bills,
            "total_pending": total_pending,
            "total_collected": total_collected,
            "recent_bills": recent_bills
        })



# -------------------------------
# Admin Dashboard
# -------------------------------
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, RolePermission]

    @swagger_auto_schema(
        operation_summary="Get Admin Dashboard",
        responses={200: "Admin welcome message"}
    )
    def get(self, request):
        request.allowed_roles = ['admin']
        return Response({"message": "Welcome Admin! Dashboard data loaded."})
