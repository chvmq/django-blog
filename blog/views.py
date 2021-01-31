from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginFrom
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout


# from


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'SUCCESS')
            return redirect('home')
        else:
            messages.error(request, 'Fail')
    else:
        form = UserRegisterForm()

    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginFrom(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginFrom()

    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


# PAGINATION
# def test(request):
#     ob = ['qwecqwc', 'qcwe', 'qbqzaa', 'bsda', 'qwecqwc3', 'qcw2e', 'qbqz14aa', 'bsda', 'qwec2qw4c', 'qc21we',
#           'qb123qzaa', 'bsaxcbda']
#     paginator = Paginator(ob, 2)
#     page_num = request.GET.get('page', 1)
#     page_objects = paginator.get_page(page_num)
#     return render(request, 'blog/test.html', {'page_obj': page_objects})

class CreateNews(LoginRequiredMixin, CreateView):
    """Просто связываем с формой"""
    form_class = NewsForm
    template_name = 'blog/add_news.html'
    raise_exception = True
    # login_url = reverse_lazy('home')
    # success_url = reverse_lazy('home') get_absolute_url по умолчанию тут стоит, тоесть редиректнит на объект


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # pk_url_kwarg = 'news_id'
    # template_name = 'news_detail.html'


class HomeNews(MyMixin, ListView):
    model = News  # обязательное поле
    template_name = 'blog/home_news_list.html'
    # object_list передаётся в шаблон по умолчанию
    context_object_name = 'news'
    mixin_prop = 'hello world'
    paginate_by = 5

    # extra_context = {'title': "Главная"}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = Category
    template_name = 'blog/home_news_list.html'
    context_object_name = 'news'
    # extra_context = {'title': 'somethign'}
    allow_empty = False
    mixin_prop = 'hello pycharm'

    def get_queryset(self):
        return News.objects.filter(
            category_id=self.kwargs['category_id'],
            is_published=True).select_related('category')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

# ЗАМЕНЕНО LISTVIEW
# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id).select_related('category')
#     category = Category.objects.get(pk=category_id)
#
#     return render(request, 'blog/category.html', {'news': news, 'category': category})


# ЗАМЕНЕНО LISTVIEW
# def index(request):
#     news = News.objects.order_by('-created_at').filter(is_published=True)
#     context = {
#         'news': news,
#         'title': 'List of news',
#     }
#     # print(dir(request))
#     return render(request, 'blog/index.html', context)


# ЗАМЕНЕНО КЛАССОМ DETAILVIEW
# def view_news(request, news_id):
#     # try:
#     #     news_item = News.objects.get(pk=news_id)
#     #     return render(request, 'blog/view_news.html', {"news_item": news_item})
#     # except News.DoesNotExist:
#     #     raise Http404('Qwencqwec')
#
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'blog/view_news.html', {"news_item": news_item})


# ЗАМЕНЕНО КЛАССОМ CREATEVIEW
# def add_news(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'blog/add_news.html', {'form': form})
