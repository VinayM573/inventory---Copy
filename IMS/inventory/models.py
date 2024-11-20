from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager



UType = (
        ("User", "User"),
        ("Admin", "Admin"),
    )
ProcessName=(
        ("Finance","Finance"),
        ("Operation","Operation"),
        ("Associate","Associate"),
        ("IT","IT"),
        ("HR","HR")
)
Loaction=(
        ("Gurgoan","Gurgoan"),
        ("Noida","Noida")
    )

CATEGORY = (
    ("NMC", "NMC"),
    ("LFP", "LFP"),
    ("LCO", "LCO"),
)
CATEGORY1 = (
    ("EV", "EV"),
    ("Portable", "Portable"),
    ("Industrial", "Industrial"),
)
CATEGORY2 = (
    ("KG", "KG"),
    ("Gram", "Gram"),
    ("Unit", "Unit"),
)

CATEGORY4 = (
    ("Regular", "Regular"),
    ("Contract", "Contract"),
)
CATEGORY5 = (
     ("Onboarding", "Onboarding"),
    ("Active", "Active"),
    ("Inactive", "Inactive"),
)   
CATEGORY6 = (
     ("Two Wheeler", "Two Wheeler"),
    ("Three Wheeler", "Three Wheeler"),
    ("Four Wheeler", "Four Wheeler"),
    ("Portable", "Portable"),

)  
STATUS=(
     ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Denied", "Denied"),
)
TCS=(
     ("Y", "Yes"),
    ("N", "No"),
)
MODE=(
     ("Buyer", "Buyer"),
    ("Seller", "Seller"),
)
PAYMENTM=(
     ("Advance", "Advance"),
    ("Upon Dispatch", "Upon Dispatch"),
    ("Balance", "Balance"),
)


class CustomUser(AbstractUser):
    username=None
    phone=models.CharField(max_length=10,unique=True)
    email=models.EmailField(max_length=100,unique=True,null=False)
    name=models.CharField(max_length=40)
    user_pic=models.ImageField(upload_to="user_pic",null=True)
    user_Type = models.CharField(max_length=40,choices=UType, null=True)
    department = models.CharField( max_length=40,choices=ProcessName,null=True)
    location = models.CharField(max_length=40,choices=Loaction,null=True)
    

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    objects=UserManager()
    
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if self.user_Type == 'Admin':
            self.is_staff=True
            self.is_active=True
            self.is_superuser = True
        elif self.user_Type == 'User':
            self.is_staff = False
            self.is_active = True
            self.is_superuser = False
        super().save(*args, **kwargs)


class ClientProfile(models.Model):
    cid =models.IntegerField(primary_key=True, auto_created=True)
    client_Name=models.CharField(max_length=40, null=True)
    business_Name=models.CharField(max_length=40, null=True)
    email = models.EmailField(max_length=40, null=True)
    contact=models.CharField(max_length=12, null=True)
    pan_Card=models.CharField(max_length=10, null=True)
    pan_Image=models.ImageField(upload_to="Pictures")
    aadhar_Card=models.CharField(max_length=12, null=True)
    adhar_Image=models.ImageField(upload_to="Pictures")
    address=models.CharField(max_length=40, null=True)
    assign_Person=models.CharField(max_length=40, null=True)
    industies_Type=models.CharField(max_length=20, choices=CATEGORY1, null=True)
    account_Type=models.CharField(max_length=20, choices=CATEGORY4, null=True)
    status=models.CharField(max_length=20, choices=CATEGORY5, null=True)
    def __str__(self):
        return str(self.client_Name)
    

class Product(models.Model):
    product = models.CharField(max_length=40, null=True)
    types_of_Battery=models.CharField(max_length=100, choices=CATEGORY6, null=True)
    cell_Chemistry = models.CharField(max_length=100, choices=CATEGORY, null=True)
    Industry_Type = models.CharField(max_length=20, choices=CATEGORY1, null=True)
    UOM = models.CharField(max_length=10,choices=CATEGORY2, null=True)
    # price=models.PositiveIntegerField(null=True) 
    HSN_Code= models.PositiveIntegerField(null=True) 

    def __str__(self):
        return str(self.product)

class CRFQ(models.Model):
    rfqid = models.CharField(max_length=10, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE,null=True)
    valid = models.DateTimeField(max_length=100, null=True)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    # desc = models.CharField(max_length=100, null=True)
    # order_quantity = models.PositiveIntegerField(null=True)
    # uom = models.CharField(max_length=10,choices=CATEGORY2, null=True)
    # price = models.IntegerField(null=True)
    # tax = models.IntegerField(null=True)
    # total = models.IntegerField(null=True)
    # taxval = models.IntegerField(null=True)
    # taxamt = models.IntegerField(null=True)
    # tcs = models.CharField(max_length=10,choices=TCS, null=True)
    # tcsval = models.IntegerField(null=True)
    # subtotal = models.IntegerField(null=True)
    transportation=models.CharField(max_length=100, choices=MODE, null=True)
    Packaging=models.CharField(max_length=100, choices=MODE, null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True)
    payment = models.CharField(max_length=100, choices=PAYMENTM, null=True)
    notes= models.CharField(max_length=400, null=True)
    created_by = models.ForeignKey(CustomUser, models.CASCADE, null=True)
    def __str__(self):
        return self.rfqid
    
class Rfq(models.Model):
    crfq = models.ForeignKey(CRFQ, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    order_quantity = models.PositiveIntegerField()
    uom = models.CharField(choices=CATEGORY2,max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"RFQ {self.id}: {self.product} - {self.desc}"