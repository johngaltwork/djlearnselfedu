from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    #paginate_by = 3 #кол-во элементов на одной странице для встроенного пагинатора в класс ListView
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Метод для формирования контекста для шаблона отображения'''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


# def index(request):
#     posts = Women.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'women/index.html', context=context)


def about(request):
    # пример как использовать пагинатор для функций представления:
    contact_list = Women.objects.all()  #читаем список всех женщин
    paginator = Paginator(contact_list, 3)  #создаем экземпляр класса Paginator

    page_number = request.GET.get('page')  # берем номер текущей страницы из GET запроса
    page_obj = paginator.get_page(page_number)  # формируем объект, который содержит список элементов текущей страницы
    return render(request, 'women/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})  # передаем page_obj в представление шаблон about.html
    #  return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Метод для формирования контекста для шаблона отображения'''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse('Обратная связь')


# def login(request):
#     return HttpResponse('Авторизация')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg = 'post_pk' если не используем слаг
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Метод для формирования контекста для шаблона отображения'''
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Метод для формирования контекста для шаблона отображения'''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug,
#     }
#
#     return render(request, 'women/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm  #  форма для регистрации новых пользователей
    template_name = 'women/register.html'  # ссылка на шаблон
    success_url = reverse_lazy('login')  # перенаправление на url адрес при успешной регистрации

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Метод для формирования контекста для шаблона отображения'''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))


    def form_valid(self, form):
        '''Метод вызывается при успешной проверке формы регистрации,
        сохраняет данные в базу данных и авторизоывает пользователя,
        перенаправляя на главную страницу'''
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'  # ссылка на шаблон

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Метод для формирования контекста для шаблона отображения'''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        '''Метод вызывается, если пользователь ввел правильно логин и пароль'''
        return reverse_lazy('home')


def logout_user(request):
    '''Функция вызывает стандартный django метод logout, для выхода пользователя из авторизации'''
    logout(request)
    return redirect('login')