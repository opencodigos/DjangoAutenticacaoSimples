# Django Autenticação (Simples)

Nesse tutorial vou mostrar para vocês uma configuração simples de autenticação com Django. Vamos utilizar a biblioteca nativa do Django *contrib.auth.* Com base na documentação vamos fazer de maneira mais simples onde praticamente customizar os templates. Agora a views, urls, models será tudo padrão do Django. Essa configuração eu indico para projetos que não tem um foco complexo ou muita customização na parte de autenticação. 

Partindo desse repositório aqui: 
[Configuração Default Simples](https://github.com/djangomy/config-default-simple)

Vamos lá, 

Primeiro vamos fazer uma configuração no ***core/settings.py*** e adicionar o **EMAIL_BACKEND** do Django, para simular um envio de e-mail para reset de senha.

`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

Documentação: 
[https://docs.djangoproject.com/en/4.1/topics/auth/default/](https://docs.djangoproject.com/en/4.1/topics/auth/default/)
[https://docs.djangoproject.com/en/4.1/topics/auth/customizing/](https://docs.djangoproject.com/en/4.1/topics/auth/customizing/)

Vamos configurar a autenticação da maneira mais simples que conheço com Django.

Então com base na documentação, vamos praticamente importar rotas ***“accounts”***  

Primeiro vamos registrar essas urls no nosso projeto.

```python
urlpatterns = [
		...
    path("accounts/", include("django.contrib.auth.urls")),  # accounts
]
```

Isso inclui todos esses padrões de URL.

```
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
```

Com isso já conseguimos testar. Rode a aplicação e tenta acessar qualquer uma dessas rotas.

Cada comportamento dessas Urls ira redirecionar para admin do django. Isso por que está utilizando o **template da view padrão do accounts**.

```python
# --- Login Logout User --- # 
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

Mas podemos criar nosso template e customizar, de maneira simples. 

Vamos criar um app novo para salvar esses templates de autenticação. 

```python
python manage.py startapp accounts
```

Agora precisamos registrar nossa aplicação. Tem que ser registrado em primeiro. Senão o Django busca o template padrão e não o que vamos criar.

``` 
INSTALLED_APPS = [ 
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     
    'myapp',
]
``` 

Dentro desse app criar uma pasta “**templates/registration**”

- login.html
- password_reset_complete.html
- password_reset_confirm.html
- password_reset_done.html
- password_reset_form.html
- register.html

Criar todos esses templates. Tem que ser exatamente esses nomes.

Se vocês acessar a views que chama esses templates padrão do django.
`from django.contrib.auth import views`

Verifica que na documentação a view está chamando **template_name.** 

São exatamente esses nomes. E para aproveitar essa views que já existe do próprio Django vamos apenas apontar o template nosso.

<details><summary><b>Login</b></summary>

- **Login** 
    ***accounts/templates/registration/login.html***
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Login{% endblock %}
    
    {% block content %}
    
    <div class="col-md-4">
        <form method="post">
            {% csrf_token %}
    
            <div class="mb-3">
                <label class="form-label" for="id_username">Usuário:</label>
                <input type="text" name="username" class="form-control">
            </div>
            
            <div class="mb-3">
                <label class="form-label" for="id_password">Senha:</label>
                <input type="password" name="password" class="form-control">
            </div>
    
            <button class="btn btn-warning" type="submit">Entrar</button>
        </form>
        
        <a href="{% url 'password_reset' %}">Esqueci minha senha</a>
    </div>
    
    {% endblock %}
    ```

</details> 

<details><summary><b>Password Reset Form</b></summary>

- **Password Reset Form**
    
    ***accounts/templates/registration/password_reset_form.html***
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Resetar Senha{% endblock %}
    
    {% block content %}
    <div class="col-md-4">
    	<h1>Resetar Senha</h1>  
            <form method="post">
            {% csrf_token %}
            <div class="mt-3">
                <label class="form-label" for="id_email">Email:</label>
                <input type="email" name="email" class="form-control" id="id_email">
            </div>
            <button class="btn btn-warning mt-3" type="submit">Resetar</button>
        </form>
    </div>
    {% endblock %}
    ```

</details>

<details><summary><b>Password Reset Confirm</b></summary>

- **Password Reset Confirm**
    
    ***accounts/templates/registration/password_reset_confirm.html***
    
    ```html
    {% extends 'base.html' %}
    {% block title %}Formulário Reset Senha{% endblock %}
    {% block content %}
    <div class="col-md-4">
        {% if validlink %}
        <p>Entre com sua nova senha para resetar.</p>
        <form action="" method="post">
            {% csrf_token %}
            <div class="mt-3">
                {{ form.new_password1.errors }}
                <label class="form-label" for="id_new_password1">Nova Senha:</label>
                <input type="password" name="new_password1" class="form-control" id="id_new_password1"> 
            </div>
            <div class="mt-3">
                {{ form.new_password2.errors }}
                <label class="form-label" for="id_new_password2">Confirmação de senha:</label>
                <input type="password" name="new_password2" class="form-control" id="id_new_password2"> 
            </div>
            <button type="submit" class="btn btn-warning mt-3">Alterar Senha</button>
        </form>
        {% else %}
        <h1>Falha na redefinição de senha</h1>
        <p>O link de redefinição de senha era inválido, possivelmente porque já foi usado. Solicite uma nova redefinição de senha.</p>
        {% endif %}
    </div>
    {% endblock %}
    ```

</details>

<details><summary><b>Password Reset Done</b></summary>

- **Password Reset Done**
    
    ***accounts/templates/registration/password_reset_done.html***
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Reset Ok{% endblock %}
    
    {% block content %}
    <div class="col-md-4">
        <h2>Solicitação de Senha Nova</h2>
        <p>Enviamos um e-mail com instruções para definir sua senha. Se eles não chegarem em alguns minutos, verifique sua pasta de spam.</p>
    </div>
    {% endblock %}
    ```

</details>

<details><summary><b>Password Reset Complete</b></summary>

- **Password Reset Complete**
    
    ***accounts/templates/registration/password_reset_complete.html***
    
    ```html
    {% extends 'base.html' %}
    {% block title %}Reset de Senha Completo{% endblock %}
    {% block content %}
    <div class="col-md-4">
      <h3>Sua senha foi alterada com sucesso!</h3>
      <p><a href="{% url 'login' %}">Fazer Login</a></p>
    </div>
    {% endblock %}
    ```

</details> 

<details><summary><b>Register</b></summary>

- **Register** 
    
    *accounts/admin.py*
    
    ```python
    from django.contrib.auth.models import User
    from django.contrib.auth import forms
    
    # Register your models here.
    class CustomUserCreationForm(forms.UserCreationForm):
        class Meta(forms.UserCreationForm.Meta):
            model = User
            fields = forms.UserCreationForm.Meta.fields + ('email','first_name','last_name',)
            
        def __init__(self, *args, **kwargs): # Adiciona 
            super().__init__(*args, **kwargs)  
            for field_name, field in self.fields.items():   
                field.widget.attrs['class'] = 'form-control'
    ```
    
    *accounts/views.py*
    
    ```python
    from django.shortcuts import render, redirect
    from .admin import CustomUserCreationForm
    from django.contrib import messages
    
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
                    return redirect('index')
    
                else:
                    print('invalid registration details')
                    
            return render(request, "registration/register.html",{"form": form})
    
    ```
    
    *core/urls.py*
    
    ```python
    from accounts import views
    
    urlpatterns = [
    	  ...
        path('register/', views.register, name='register'),
    		...
    ] 
    ```
    
    *accounts/templates/register.html*
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Registrar{% endblock %}
    
    {% block content %} 
    <div class="col-md-4">
        <h4>Criar uma conta</h4>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button class="btn btn-warning mt-3" type="submit">Registrar</button>
        </form>
    </div>
    {% endblock %}
    ```
</details>

Esses templates que to colocando podem ser customizados como você quiser. Só ficar atento nos identificadores dos formulários que não podem mudar.

Feito isso, Podemos testar. Basta adicionar as rotas no seu template HTML para chamar a view.

Estou em um projeto teste então eu adicionei esses botões

```python
<a class="btn btn-outline-danger" href="{% url 'logout' %}">Sair</a>
<a class="btn btn-outline-primary" href="{% url 'login' %}">Entrar</a>
<a class="btn btn-success" href="{% url 'register' %}">Registrar</a>
<a href="{% url 'password_reset' %}">Esqueci minha senha</a>
```

<details><summary><b>Base</b></summary>

- **Base**
    
    ```html
    {% load static %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
    	<meta charset="UTF-8">
    	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    	<title>{% block title %}{% endblock %}</title>
    	
    	<!-- CSS -->
    	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    	
    	<link rel="stylesheet" href="{% static 'css/style.css' %}">
    	
    </head>
    <body>  
    	
    	{% include 'navbar.html' %}
     
    	
    	<div class="container"> 
    	 
    		{% if user.is_authenticated %}
    			<h1>Olá, {{user.username}}</h1>  
    		{% endif %} 
    			 
    		{% block content %}{% endblock %} 
    	</div>
    
    	<!-- JS-->
    	<script src="https://code.jquery.com/jquery-3.6.1.min.js" integrity="sha256-o88AwQnZB+VDvE9tvIXrMQaPlFFSUTR+nldQm1LuPXQ=" crossorigin="anonymous"></script>
    
    	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
    	
    	<script src="{% static 'js/scripts.js' %}"></script>
    
    	{% block scripts %}{% endblock scripts %} 
    
    </body>
    </html>
    ```
</details>

<details><summary><b>Navbar</b></summary>

- **Navbar**
    
    Tenho uma navbar.html para adicioanr no projeto base.
    
    ```html
    <nav class="navbar navbar-expand-lg border-bottom">
    
        <div class="container-fluid">
    
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo03"
                aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
    
            <a class="navbar-brand" href="#">Myapp</a>
    
            <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
    
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
    
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/">Inicio</a>
                    </li> 
    
                    <li class="nav-item">
                        <a class="nav-link disabled">Desativado</a>
                    </li>
    
                </ul>
    
                <div class="d-flex gap-3 align-items-center">
                    {% if user.is_authenticated %}
                        <span class="nav-text">
                            {{user.username}}
                        </span>
                        <a class="btn btn-outline-danger" href="{% url 'logout' %}">Sair</a>
                    {% else %}
                        <a class="btn btn-outline-primary" href="{% url 'login' %}">Entrar</a>
                        <a class="btn btn-success" href="{% url 'register' %}">Registrar</a>
                    {% endif %} 
    
                </div>
               
            </div>
    
        </div>
    
    </nav>
    ```
</details>    

**Esse é um jeito simples**. Se você precisa de algo Customizável ai pode ser utilizado o exemplo completo que tem na documentação do Django. De criar as views, forms, customizar os fields.
