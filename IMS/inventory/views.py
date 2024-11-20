# inventory/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import update_session_auth_hash
from inventory.forms import RegistrationForm, ProductForm,CRFQForm,ClientRegistry,ClientProfileForm,CustomAuthenticationForm,UserProfileForm,ProfileImageForm,RfqFormSet
from inventory.models import Product,CRFQ,ClientProfile,CustomUser,Rfq
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView


# def user_login(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('dash')
#             else:
#                 messages.error(request, 'Incorrect password')
#         else:
#             messages.error(request, 'Email is not registered')
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'inventory/login.html', {'form': form})

@login_required
def index(request):
    orders_user = CRFQ.objects.all()
    users = CustomUser.objects.all()[:2]
    client = ClientProfile.objects.all()[:2]
    client_adm = ClientProfile.objects.all()[:2]
    products = Product.objects.all()[:2]
    reg_users = len(CustomUser.objects.all())
    reg_client = len(ClientProfile.objects.all())
    all_prods = len(Product.objects.all())
    all_orders = len(CRFQ.objects.all())
    # user_name=request.user.name
    context = {
        "title": "Home",
        "orders": orders_user,
        "client_adm": client_adm,
        "users": users,
        "client": client,
        "products": products,
        "count_users": reg_users,
        "count_client": reg_client,
        "count_products": all_prods,
        "count_orders": all_orders,
        # 'user_name': user_name
    }
    return render(request, "inventory/index.html", context)


@login_required
def products(request):
    products = Product.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Item Added Successfully..')
            return redirect("products")
    else:
        form = ProductForm()
    context = {"title": "Products", "products": products, "form": form}
    return render(request, "inventory/products.html", context)

@permission_required('auth.view_user', raise_exception=True)
@login_required
def users(request):
    users = CustomUser.objects.all()
    context = {"title": "Users", "users": users}
    return render(request, "inventory/users.html", context)


@login_required
def user(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('user')  # Replace 'user' with the URL name of the user profile page
    else:
        form = ProfileImageForm(instance=request.user)
    context = {"profile": "User Profile",'form': form}
    return render(request, "inventory/user.html", context)

@login_required
@permission_required('auth.view_user', raise_exception=True)
def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully!')
            return redirect('register')  # Redirect to a success page after successful form submission
    else:
        form = RegistrationForm()
    return render(request,'inventory/register.html', {'form': form})

@login_required
@permission_required('auth.view_user', raise_exception=True)
def client(request):
    if request.method == "POST":
        form = ClientRegistry(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client registered successfully!')
            return redirect("client")
    else:
        form = ClientRegistry()
    context = {"client": "Client", "form": form}
    return render(request, "inventory/client.html", context)

@login_required
@permission_required('auth.view_user', raise_exception=True)
def clients(request):
    clients = ClientProfile.objects.all()
    context = {"title": "Clients", "clients": clients}
    return render(request, "inventory/clients.html", context)

@login_required
def crfq(request):
    if request.method == "POST":
        form = CRFQForm(request.POST)
        formset = RfqFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            instance = form.save()
            rfqid = form.cleaned_data['rfqid']
            for form in formset:
                if form.cleaned_data:
                    quantity = form.cleaned_data['order_quantity']
                    price = form.cleaned_data['price']
            # total_price = quantity * price
    
            # Save the calculated total price to the form instance
            # form.instance.total = total_price
            # instance = form.save()
            instance.created_by = request.user
            instance.save()
            context={
                'rfqid': rfqid,
                'quantity':quantity,
                'price':price,
                # 'total_price':total_price,
            }
            # messages.success(request, 'Rfq Added successfully..')
            return render(request, 'inventory/view_rfq.html', context)
    else:
        form = CRFQForm()
        formset = RfqFormSet()
    context = {"title": "CRFQ", "crfq": crfq, "form": form,'formset': formset}
    return render(request, "inventory/crfq.html", context)

@login_required
def clear_data(request):
    # Add logic to delete or clear data
    crfq = CRFQ.objects.all()
    if request.method == 'POST':
        crfq.delete()  # Example: Deletes all records in the model
        messages.success(request, 'All data cleared successfully')
        return redirect("orders")  # Redirect to a specific page after deletion
    return render(request, 'inventory/orders.html')

@login_required
def orders(request):
    crfqs = CRFQ.objects.all() 
    # for crfq in crfqs:
    #     crfq.total_price = crfq.calculate_total_price()
    return render(request, 'inventory/orders.html', {"title": "Purchase",'crfqs': crfqs})
   
@login_required
def product(request):
    product = Product.objects.all()
    return render(request, 'inventory/product.html', {"title": "All Item",'product': product})

@login_required
def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')  # Get the item ID from the form data
        if item_id:  # Check if the item ID is not empty
            item = get_object_or_404(Product, pk=item_id)
            item.delete()
            messages.success(request, f'"Item {item.product}" deleted successfully.')
            return redirect("product")
    return render(request, 'inventory/product.html')

@login_required
def update_item(request, id):
    product = Product.objects.get(id=id)  # Retrieve the existing client profile
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)  # Bind form to existing instance
        if form.has_changed():  # Check if form data has changed
            if form.is_valid():
                form.save()
                messages.success(request, f'Item {product.product} successfully updated')  # Update success message with client's name
                return redirect('product')  # Redirect to the clients page after update
        else:
            messages.info(request, f'No changes were made to the item data for {product.product}.')  # Display info message if no changes were made
            return redirect('product')
    else:
        form = ProductForm(instance=product)  # Bind form to existing instance
    return render(request, 'inventory/update_item.html', {"update": "Update Item",'form': form, 'product': product})

@login_required
def generate_pdf(request):
    selected_rows = request.POST.getlist('selected_rows')
    selected_objects = CRFQ.objects.filter(id__in=selected_rows)
    # selected_objects = CRFQ.objects.all()  # Retrieve all CRFQ objects

    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="example.pdf"'
    p = canvas.Canvas(response)
    
    y_coordinate = 800  # Starting y-coordinate for writing
    p.drawString(200, 800, "BatX Energies")
    y_coordinate -= 20

    for crfqs in selected_objects:
        y_coordinate -= 20
        p.drawString(100, y_coordinate, f"Product Name: {crfqs.product}")
        y_coordinate -= 20  # Move to the next line
        p.drawString(100, y_coordinate, f"Created By: {crfqs.created_by}")
        y_coordinate -= 20  # Move to the next line
        p.drawString(100, y_coordinate, f"Date: {crfqs.date}")
        y_coordinate -= 40  # Move to the next block
    
    p.showPage()
    p.save()
    return response

@login_required
@permission_required('auth.view_user', raise_exception=True)
def delete_client(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')  # Assuming you have a hidden input field with the client id in your form
        client = get_object_or_404(ClientProfile, pk=cid)
        client.delete()
        messages.success(request, f'Client "{client.client_Name}" deleted successfully.')
        return redirect("clients")
    return render(request, 'inventory/clients.html')

@login_required
@permission_required('auth.view_user', raise_exception=True)
def delete_user(request):
    if request.method == 'POST':
        id = request.POST.get('id')  # Assuming you have a hidden input field with the client id in your form
        user = get_object_or_404(CustomUser, pk=id)
        current_user = request.user
        if current_user == user:
            messages.error(request, "You cannot delete your own account.")
            return redirect('users')
        else:
            user.delete()
            messages.success(request, f'User "{user.name}" deleted successfully.')
            return redirect("users")
    return render(request, 'inventory/users.html')

@login_required
@permission_required('auth.view_user', raise_exception=True)
def update_client(request, cid):
    client = ClientProfile.objects.get(cid=cid)  # Retrieve the existing client profile
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, request.FILES, instance=client)  # Bind form to existing instance
        if form.has_changed():  # Check if form data has changed
            if form.is_valid():
                form.save()
                messages.success(request, f'Client Data for {client.client_Name} successfully updated')  # Update success message with client's name
                return redirect('clients')  # Redirect to the clients page after update
        else:
            messages.info(request, f'No changes were made to the client data for {client.client_Name}.')  # Display info message if no changes were made
            return redirect('clients')
    else:
        form = ClientProfileForm(instance=client)  # Bind form to existing instance
    return render(request, 'inventory/update_client.html', {"update": "Update Client",'form': form, 'client': client})

@login_required
@permission_required('auth.view_user', raise_exception=True)
def update_user(request, id):
    user = get_object_or_404(CustomUser, id=id)  # Retrieve the existing user
    if user and not request.user.is_superuser:
        # Return an error response or redirect to an unauthorized page
        return HttpResponse("Unauthorized", status=401)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)  # Bind form to existing instance
        if form.is_valid():
            form.save()
            if form.has_changed():  # Check if form data has changed
                messages.success(request, f'User data for {user.name} successfully updated')
            else:
                messages.info(request, f'No changes were made to the user data for {user.name}.')
            return redirect('users')  # Redirect to the users page after update
    else:
        form = UserProfileForm(instance=user)  # Bind form to existing instance
        if request.user == user:
            # Disable the user_Type field for the current user
            form.fields['user_Type'].disabled = True
    return render(request, 'inventory/update_user.html', {"update": "Update User", 'form': form, })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')  # Replace 'profile' with the URL name of the profile page
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'inventory/change_password.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = CustomUser.objects.get(email=email)  # Use CustomUser model
        except CustomUser.DoesNotExist:
            messages.error(self.request, 'Email is not registered with us. Please contact to Admin..')
            return redirect('reset_password')

        if user.is_active:
            super().form_valid(form)
            input_value = self.request.POST.get('email')
            context = {
                'input_value': input_value,
            }
            return render(self.request, 'inventory/reset.html', context)

# def view_rfq(request):
#     return render(request, 'inventory/view_rfq.html')


# def view_rfq(request):
#     def form_valid(self, form):
#         rfqid = form.cleaned_data['rfqid']
#         id = CRFQForm.objects.get(rfqid=rfqid)  # Use CustomUser mod
#         form_valid(form)
#         id = self.request.POST.get('email')
#         context = {
#                 'id': id,
#             }
#         return render(self.request, 'inventory/view_rfq.html', context)
    # def form_valid(self, form):
    #     super().form_valid(form)
    #     input_value = self.request.POST.get('email')
    #     return render(request, 'inventory/view_rfq.html')