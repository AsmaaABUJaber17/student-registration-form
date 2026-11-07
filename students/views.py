from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentForm
from .models import Student

# دالة إضافة طالب جديد
def add_student(request):
    # لو الطلب من نوع POST، يعني المستخدم ضغط على زر الحفظ
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES) # request.FILES ضرورية عشان الصور
        if form.is_valid():
            form.save()
            messages.success(request, 'Student has been added successfully.')
            return redirect('student_list') # توجيه لصفحة الجدول بعد الحفظ
    else:
        # لو الطلب GET، اعرض فورم فارغة
        form = StudentForm()

    return render(request, 'students/student_form.html', {'form': form})

# دالة عرض قائمة الطلاب
def student_list(request):
    # جلب كل الطلاب من قاعدة البيانات وترتيبهم أبجدياً حسب الاسم
    students = Student.objects.all().order_by('name')
    return render(request, 'students/student_list.html', {'students': students})