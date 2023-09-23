import re
from django.shortcuts import render, redirect
from .admin import CustomUserCreationForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        cpf = request.POST['cpf']
        password = request.POST['password']
        cpf_format = re.sub(r'[^0-9]', '', cpf)
        print(cpf)
        print(password)
        user = authenticate(request, cpf=cpf_format, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print('entrou aqui')
            # Autenticação bem-sucedida, redirecione para a página de sucesso ou faça o que for necessário
            messages.success(request, 'Bem Vindo (a) '+ user.first_name)
            return redirect('mysite')
        else:
            # Autenticação falhou, lide com isso de acordo
            messages.debug(request, 'Ops! Aconteceu algum erro.') 
    # Renderize o formulário de login
    return render(request, 'login.html')

# Create your views here.
def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('mysite')

        else:
            print('invalid registration details')
            
    return render(request, "registration/register.html",{"form": form})
