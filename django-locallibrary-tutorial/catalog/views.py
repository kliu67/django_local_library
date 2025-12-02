from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


def index(request):
    """View function for home page of site."""

    #Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instacnes_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    #Render the HTML template index.html with the data in the context vairable

    return render(request, 'index.html', context=context)

def admin(request):
    return redirect('/admin')
# Create your views here.

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list'   # your own name for the list as a template variable
    queryset = Book.objects.filter(title__contains='') # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    context_object_name = 'author_list'
    queryset = Author.objects.all()
    template_name = 'authors/my_arbitrary_template_author_list.html'

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def get_context_data(self, **kwargs):
        #Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        #Add in a queryset of all the books
        context["book_list"] = Book.objects.filter(author=self.object.id)
        print(self.object.id)
        # import pdb; pdb.set_trace()
        return context


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )