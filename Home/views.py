from django.shortcuts import render, redirect, redirect, get_object_or_404
from functools import wraps
from Home.models import SignupData, Events, Students, Booking
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse


# Custom login_required decorator using session
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('logged_in'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Create your views here.
def index(request):
    return render(request, 'index.html')

# User login view
def login(request):
    if request.session.get('logged_in'):
        return redirect("index")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        password = request.POST.get("password")

        try:
            user_instance = Students.objects.get(first_name=first_name)

            if check_password(password, user_instance.password):
                request.session['logged_in'] = True
                request.session['username'] = user_instance.first_name
                messages.success(request, "Login Successful")
                return redirect("index")
            else:
                messages.error(request, "Invalid Password!")
        except Students.DoesNotExist:
            messages.error(request, "User does not exist. Please try again.")
    return render(request, "login.html")


@login_required
def student(request):
    first_name = request.session.get('username')
    student_instance = Students.objects.filter(first_name=first_name).first()

    if not student_instance:
        messages.error(request, "Student not found.")
        return redirect("login")

    query_name = request.GET.get("event", "").strip()
    query_date = request.GET.get("start_date", "").strip()
    student_class = str(student_instance.class_level)

    events = Events.objects.filter(for_class__icontains=student_class)
    if query_name:
        events = events.filter(event__icontains=query_name)
    if query_date:
        events = events.filter(start_date=query_date)

    # Get already booked event IDs
    booked_event_ids = set(Booking.objects.filter(student=student_instance).values_list("event_id", flat=True))

    return render(request, "student.html", {
        'first_name': first_name,
        'student': student_instance,
        'items': events,
        'query_name': query_name,
        'query_date': query_date,
        'booked_event_ids': booked_event_ids
    })

def logout(request):
    request.session.flush()
    return redirect('/')

@login_required
@csrf_exempt
def book_event(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        student = Students.objects.filter(first_name=request.session.get('username')).first()
        event = Events.objects.filter(id=event_id).first()

        if student and event:
            # Save booking only if not already booked
            if not Booking.objects.filter(student=student, event=event).exists():
                Booking.objects.create(student=student, event=event)
        return HttpResponse("")
    return HttpResponse("")    

@login_required
@csrf_exempt
def cancel_event(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        student_instance = Students.objects.filter(first_name=request.session.get('username')).first()
        if student_instance:
            Booking.objects.filter(student=student_instance, event_id=event_id).delete()
            return JsonResponse({"status": "cancelled"})
        else:
            return JsonResponse({"status": "student_not_found"}, status=404)
    return JsonResponse({"status": "error"}, status=400)