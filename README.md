# Django Autenticação (Simples)
 
 
Partindo desse repositório aqui: 
[Configuração Default Simples](https://github.com/djangomy/config-default-simple)
 
Documentação: 
[https://docs.djangoproject.com/en/4.2/topics/auth/customizing/](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/) 
 
 
**Adiconar campo CPF no formulário de Registro**

 ```jsx
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.username
```

```jsx
AUTH_USER_MODEL = 'accounts.CustomUser'
```

```jsx
python manage.py makemigrations && python manage.py migrate
```

accounts/admin.py

```jsx
from django.contrib import admin 

admin.site.register(CustomUser)
```

**CPF como parametro padrão de autenticação**

```jsx
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class CPFAuth(ModelBackend):
    def authenticate(self, request, cpf=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(cpf=cpf)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
```

```jsx
AUTHENTICATION_BACKENDS = ['myapp.auth_backends.CPFAuth']
```

```jsx
from django.contrib import messages
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        cpf = request.POST['cpf']
        password = request.POST['password']
        print(cpf)
        print(password)
        user = authenticate(request, cpf=cpf, password=password)
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
    return render(request, 'registration/login.html')
```

```jsx
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js"></script>
```

login.html

**Adiciona uma mask**

```jsx
{% block scripts %}
<script>
    $(document).ready(function () {
        $('input[name="cpf"]').mask('000.000.000-00', {reverse: true});
    });
</script> 
{% endblock scripts %}
```

**Adiciona botão ok**

```jsx
{% block scripts %}
<script>
    $(document).ready(function () {
        var cpfInput = $('input[name="cpf"]');
        var cpfOkButton = $('#cpf_ok');

        cpfInput.mask('000.000.000-00', {reverse: true});

        cpfInput.keyup('input', function () {
            var cpfValue = cpfInput.val().replace(/[^0-9]/g, '');
            console.log(cpfValue)
            if (cpfValue.length === 11) {
                cpfOkButton.removeAttr('hidden');
            } else {
                cpfOkButton.attr('hidden', 'hidden');
            }
        });
    });
</script>
{% endblock scripts %}
```