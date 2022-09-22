from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import Women, Category
from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm, WomenUpdateForm
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.cache import cache_page


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    # object_list = context_object_name
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):  # для внесения динамических данных
        context = super().get_context_data(**kwargs)
        # context['menu'] = [{'title': "О сайте", 'url_name': 'about'},
        #                    {'title': "Добавьте статью", 'url_name': 'add_page'},
        #                    {'title': "Обратная связь", 'url_name': 'contact'},
        #                    {'title': "Войти", 'url_name': 'login'}
        #                    ]
        # context['title'] = 'Главное меню'
        # context['cat_selected'] = 0
        c_def = self.get_user_context(title='Главное меню')
        context = dict(list(context.items()) + list(c_def.items()))

        return context

    def get_queryset(self):  # для выбора данных из модели
        return Women.objects.filter(is_published=1).select_related('cat')


# def index(request):
#     women = Women.objects.all()
#
#     context = {
#         'posts': women,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


def about(request):
    queryset = Women.objects.all()
    paginator = Paginator(queryset, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': queryset,
        'menu': menu,
        'title': 'О странице',
        'page_obj': page_obj
    }
    return render(request, 'women/about.html', context=context)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    #  login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#     return render(request, 'women/add_page.html', context={'form': form, 'menu': menu, 'title': 'Добавление статьи'})


class ContactFormView(DataMixin, FormView):  # Formview - форма, которая не привязана к модели
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def contact(request):
    return HttpResponse("Обратная связь")


# def login(request):
#     return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['menu'] = menu
        # context['title'] = context['post'].title
        # context['cat_selected'] = context['post'].id
        c_def = self.get_user_context(title=context['post'].title, cat_selected=context['post'].id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': 1
#     }
#
#     return render(request, 'women/post.html', context=context)


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['menu'] = menu
        # context['title'] = 'Отображение по рубрикам'
        # context['cat_selected'] = context['posts'][0].cat_id
        c_def = self.get_user_context(title='Отображение по рубрикам', cat_selected=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


# def show_category(request, cat_slug):
#     cats = Category.objects.filter(slug=cat_slug)
#
#     posts = Women.objects.filter(cat_id=cats[0].id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cats[0].id
#     }
#
#     return render(request, 'women/index.html', context=context)


# def categories(request, cat_id):
#     if request.GET:
#         print(request.GET)
#
#     elif cat_id == 1:
#         return redirect('home')
#
#     elif cat_id == 2:
#         raise Http404()
#
#     elif cat_id == 3:
#         return redirect('home', permanent=False)
#
#     return HttpResponse(f"<h1>Статьи по категориям</h1><p>{cat_id}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена крыса</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация пользователей')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class DeletePost(DataMixin, DeleteView):
    model = Women
    template_name = 'women/delete.html'
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Удаление поста', cat_selected=context['post'].id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class WomenUpdate(DataMixin, LoginRequiredMixin, UpdateView):
    model = Women
    template_name = 'women/update.html'
    form_class = WomenUpdateForm
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение поста', cat_selected=context['post'].id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context

