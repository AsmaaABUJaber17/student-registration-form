import re
from django import forms
from django.core.validators import FileExtensionValidator
from .models import Student

class StudentForm(forms.ModelForm):
    # التحقق من أن الصورة jpg أو png فقط
    image = forms.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
        label='Image (JPG or PNG)'
    )

    class Meta:
        model = Student
        fields = [
            'name', 'university_id', 'id_number', 
            'mobile_number', 'address', 'date_of_birth', 'image',
        ]
        # أسماء الحقول اللي بتظهر للمستخدم
        labels = {
            'name': 'Full Name',
            'university_id': 'University ID',
            'id_number': 'ID Number',
            'mobile_number': 'Mobile Number',
            'address': 'Address',
            'date_of_birth': 'Date of Birth',
            'image': 'Image (JPG or PNG)',
        }
        # 
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'university_id': forms.NumberInput(attrs={'placeholder': '9 digits'}),
            'id_number': forms.NumberInput(attrs={'placeholder': '9 digits'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': '059 or 056'}),
            'address': forms.TextInput(attrs={'placeholder': 'Your address'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}), # عشان يظهر تقويم
        }

    # التحقق من الاسم: حروف ومسافات فقط (عربي وإنجليزي)
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not re.fullmatch(r"[A-Za-z\u0621-\u063A\u0641-\u064A\u066E-\u066F\u0671-\u06D3\u06FA-\u06FC ]+", name):
            raise forms.ValidationError('Name must contain letters and spaces only.')
        return name

    # التحقق من الرقم الجامعي
    def clean_university_id(self):
        university_id = self.cleaned_data['university_id']
        value = str(university_id) # حولناه لنص عشان نقدر نفحص الطول والرقم الأول

        if len(value) != 9 or value[0] not in '12':
            raise forms.ValidationError('University ID must contain 9 digits and start with 1 or 2.')
        return university_id

    #  التحقق من رقم الهوية
    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']
        value = str(id_number)

        if len(value) != 9 or value[0] not in '984':
            raise forms.ValidationError('ID Number must contain 9 digits and start with 9, 8, or 4.')
        return id_number

    # التحقق من رقم الجوال
    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number'].strip()
        # 05 ثم 9 أو 6 ثم 7 أرقام أخرى (المجموع 10)
        if not re.fullmatch(r'05[96][0-9]{7}', mobile):
            raise forms.ValidationError('Mobile number must be 10 digits and start with 059 or 056.')
        return mobile

    # التحقق من طول العنوان
    def clean_address(self):
        address = self.cleaned_data['address'].strip()
        if len(address) > 150:
            raise forms.ValidationError('Address must not exceed 150 characters.')
        return address