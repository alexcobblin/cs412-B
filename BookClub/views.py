# File: views.py
# Author: Alex Cobb
# Description: Views for the BookClub application

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, TemplateView
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import Reader, Book, Comment, Review
from .forms import (
    CreateReaderForm,
    UpdateReaderForm,
    CreateCommentForm,
    CreateReviewForm,
)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    '''Require login and provide helper methods.'''

    def get_login_url(self):
        return reverse('login')

    def get_logged_in_reader(self):
        return Reader.objects.get(user=self.request.user)


# ------------------------------------------------------------------
# Authentication Views
# ------------------------------------------------------------------

class RegisterView(CreateView):
    '''Display and process forms to create a User and Reader.'''

    model = Reader
    form_class = CreateReaderForm
    template_name = 'BookClub/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()
            login(
                self.request,
                user,
                backend='django.contrib.auth.backends.ModelBackend'
            )

            form.instance.user = user
            return super().form_valid(form)

        return self.form_invalid(form)

    def get_success_url(self):
        return reverse('books')


class LoginView(View):
    '''Handle user login.'''

    template_name = 'BookClub/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('books')

        return render(
            request,
            self.template_name,
            {'error': 'Invalid credentials'}
        )


class LogoutView(View):
    '''Handle user logout.'''

    def post(self, request):
        logout(request)
        return redirect('books')


# ------------------------------------------------------------------
# Book Views
# ------------------------------------------------------------------

class BookListView(ListView):
    '''Display all books.'''

    model = Book
    template_name = 'BookClub/show_all.html'
    context_object_name = 'books'

    def get_queryset(self):
        search = self.request.GET.get('search', '')

        if search:
            return (
                Book.objects.filter(book_name__icontains=search)
                | Book.objects.filter(author__icontains=search)
            )

        return Book.objects.all()


class AddBookView(CustomLoginRequiredMixin, CreateView):
    '''Create a new Book.'''

    model = Book
    template_name = 'BookClub/add_book.html'
    fields = [
        'book_name',
        'author',
        'description',
        'image_file',
    ]

    success_url = reverse_lazy('books')


class BookDetailView(DetailView):
    '''Display the details for a single Book.'''

    model = Book
    template_name = 'BookClub/show_book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book = self.get_object()
        search = self.request.GET.get('page_search', '')

        context['pages'] = [
            (page, book.get_comments_by_pgnum(page))
            for page in book.get_unique_page_nums()
            if search in str(page)
        ]

        context['search'] = search
        context['comment_form'] = CreateCommentForm()
        context['review_form'] = CreateReviewForm()

        if self.request.user.is_authenticated:
            try:
                reader = Reader.objects.get(user=self.request.user)

                context['reader'] = reader
                context['reader_has_review'] = Review.objects.filter(
                    reader=reader,
                    book=book
                ).exists()

            except Reader.DoesNotExist:
                context['reader'] = None
                context['reader_has_review'] = False

        return context


# ------------------------------------------------------------------
# Comment Views
# ------------------------------------------------------------------

class CreateCommentView(CustomLoginRequiredMixin, CreateView):
    '''Create a Comment on a Book.'''

    form_class = CreateCommentForm

    def form_valid(self, form):
        book = Book.objects.get(pk=self.kwargs['book_pk'])

        form.instance.book = book
        form.instance.reader = self.get_logged_in_reader()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'book',
            kwargs={'pk': self.kwargs['book_pk']}
        )


class DeleteCommentView(CustomLoginRequiredMixin, TemplateView):
    '''Delete a Comment.'''

    def dispatch(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs['pk'])

        if comment.reader.user == request.user:
            comment.delete()

        return redirect(
            'book',
            pk=comment.book.pk
        )


# ------------------------------------------------------------------
# Review Views
# ------------------------------------------------------------------

class CreateReviewView(CustomLoginRequiredMixin, CreateView):
    '''Create a Review on a Book.'''

    form_class = CreateReviewForm

    def form_valid(self, form):
        book = Book.objects.get(pk=self.kwargs['book_pk'])

        form.instance.book = book
        form.instance.reader = self.get_logged_in_reader()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'book',
            kwargs={'pk': self.kwargs['book_pk']}
        )

class EditReviewView(CustomLoginRequiredMixin, UpdateView):
    '''Update an existing Review.'''

    model = Review
    form_class = CreateReviewForm
    template_name = 'BookClub/edit_review.html'

    def form_valid(self, form):
        '''Handle the form submission.'''

        print(
            f'EditReviewView.form_valid(): '
            f'form.cleaned_data={form.cleaned_data}'
        )

        return super().form_valid(form)

    def get_success_url(self):
        '''Return to the Book page after updating.'''

        return reverse(
            'book',
            kwargs={'pk': self.object.book.pk}
        )


class DeleteReviewView(CustomLoginRequiredMixin, TemplateView):
    '''Delete a Review.'''

    def dispatch(self, request, *args, **kwargs):

        review = Review.objects.get(pk=self.kwargs['pk'])

        if review.reader.user == request.user:
            review.delete()

        return redirect(
            'book',
            pk=review.book.pk
        )


# ------------------------------------------------------------------
# Reader Views
# ------------------------------------------------------------------

class ReaderDetailView(DetailView):
    model = Reader
    template_name = 'BookClub/reader.html'
    context_object_name = 'reader'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reader = self.get_object()
        reader_reviews = Review.objects.filter(reader=reader)
        print(f"Reader: {reader}")
        print(f"Reviews found: {reader_reviews}")
        context['reader_reviews'] = reader_reviews
        return context


class UpdateReaderView(CustomLoginRequiredMixin, UpdateView):
    '''Update a Reader profile.'''

    model = Reader
    form_class = UpdateReaderForm
    template_name = 'BookClub/update_reader.html'

    def form_valid(self, form):
        print(
            f'UpdateReaderView.form_valid(): '
            f'{form.cleaned_data}'
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'reader',
            kwargs={'pk': self.object.pk}
        )
