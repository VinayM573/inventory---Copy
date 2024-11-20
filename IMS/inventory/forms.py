# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser
from inventory.models import Product,CRFQ,ClientProfile,CustomUser,Rfq
from django.forms import inlineformset_factory


class CustomAuthenticationForm(AuthenticationForm):
    pass

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['user_Type','department', 'name','phone', 'email','location','user_pic','password1'] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_pic'].required = False


class ClientRegistry(forms.ModelForm):  
    class Meta:
        model = ClientProfile
        fields = [
            "client_Name",
            "business_Name",
            "email",
            "contact",
            "pan_Card",
            "pan_Image",
            "aadhar_Card",
            "adhar_Image",
            "address",
            "assign_Person",
            "industies_Type",
            "account_Type",
            "status",
        ]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product","types_of_Battery","cell_Chemistry", "Industry_Type","UOM","HSN_Code"]

class CRFQForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and not self.initial.get('rfqid'):
            latest_instance = CRFQ.objects.order_by('-id').first()
            if latest_instance:
                latest_custom_id = latest_instance.rfqid
                numeric_part = int(latest_custom_id[3:]) + 1
                new_custom_id = f'rfq{numeric_part:03d}'
            else:
                new_custom_id = 'rfq001'
            self.initial['rfqid'] = new_custom_id
    class Meta:
        model = CRFQ
        fields = ['rfqid',"client","valid",'transportation','Packaging','status','payment','notes',]
        # fields = ['rfqid',"client","valid","product","desc","order_quantity",'uom','price','tax','total','taxval','taxamt','tcs','tcsval','subtotal','transportation','Packaging','status','payment','notes',]
        
        widgets = {
            'rfqid': forms.TextInput(attrs={'class': 'form-control form-control-sm rounded-0 field','readonly': 'readonly'}),
            'product': forms.Select(attrs={'class': 'form-control item_id ui-autocomplete-input','style':"color: black;"}),
            'client': forms.Select(attrs={'class': 'form-control form-control-sm rounded-0 field','style':"color: black;"}),
            'valid': forms.DateInput(attrs={'class': 'form-control form-control-sm field','id':'validityDate','type':'date'}),
            # 'product': forms.Select(attrs={'class': 'form-control item_id ui-autocomplete-input','style':"color: black;"}),   
            # 'desc': forms.TextInput(attrs={'class': 'form-control'}),
            # 'order_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'uom': forms.Select(attrs={'class': 'form-control','style':"color: black;"}),
            # 'price': forms.NumberInput(attrs={'class': 'form-control','placeholder':'0'}),
            # 'tax': forms.NumberInput(attrs={'class': 'form-control','placeholder':'0'}),
            # 'total': forms.NumberInput(attrs={'class': 'form-control','placeholder':'0'}),
            # 'taxval': forms.NumberInput(attrs={'class': 'form-control','placeholder':'0'}),
            # 'taxamt': forms.NumberInput(attrs={'class': 'form-control','placeholder':'0'}),
            # 'tcs': forms.Select(attrs={'class': 'form-control rounded-0','style':"color: black;"}),
            # 'tcsval': forms.NumberInput(attrs={'class': 'form-control','placeholder':'0'}),
            # 'subtotal': forms.NumberInput(attrs={'class': 'form-control','placeholder':'0'}),
            'transportation': forms.Select(attrs={'class': 'form-control rounded-0','style':"color: black;"}),
            'Packaging': forms.Select(attrs={'class': 'form-control rounded-0','style':"color: black;"}),
            'status': forms.Select(attrs={'class': 'form-control rounded-0','style':"color: black;"}),
            'payment': forms.Select(attrs={'class': 'form-control rounded-0','style':"color: black;"}),
            'notes': forms.Textarea(attrs={'class': 'form-control rounded-0', 'style':'height: 100px;','cols': '10', 'rows': '4'}),
        }
class RfqForm(forms.ModelForm):
    class Meta:
        model = Rfq
        fields = ['product', 'desc', 'order_quantity', 'uom', 'price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control item_id ui-autocomplete-input','style':"color: black;"}),   
            'desc': forms.TextInput(attrs={'class': 'form-control'}),
            'order_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'uom': forms.Select(attrs={'class': 'form-control','style':"color: black;"}),
            'price': forms.NumberInput(attrs={'class': 'form-control','placeholder':'0'}),
        }

RfqFormSet = inlineformset_factory(CRFQ, Rfq, form=RfqForm, extra=1)
    
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','user_Type','department', 'name','phone','location','user_pic']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_pic'].required = False

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['user_pic']
