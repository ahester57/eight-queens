"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect

from .forms import QueenPositionsForm


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

# def contact(request):
#     """Renders the contact page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/contact.html',
#         {
#             'title':'Contact',
#             'message':'Your contact page.',
#             'year':datetime.now().year,
#         }
#     )

# def about(request):
#     """Renders the about page."""
#     assert isinstance(request, HttpRequest)
#     return render(
#         request,
#         'app/about.html',
#         {
#             'title':'About',
#             'message':'Your application description page.',
#             'year':datetime.now().year,
#         }
#     )

def chessboard_view(request, queen_positions='12345678'):
    """Renders the chessboard page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = QueenPositionsForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/chessboard/' + form.cleaned_data['queen_positions'])
    else:
        form = QueenPositionsForm()

    chromosome = ''
    try:
        chromosome = queen_positions
    except KeyError:
        print('Positions not provided.')

    if len(chromosome) != 8 or not chromosome.isnumeric():
        print('Invalid position provided.')
        chromosome = '12345678'

    # Convert queen_positions to a 2D array to make it easier to work with in the template
    board = [['.' for _ in range(8)] for _ in range(8)]
    for col, row_str in enumerate(chromosome):
        row = int(row_str) - 1
        board[row][col] = 'Q'

    context = {
        'title': chromosome,
        'chessboard': board,
        'year': datetime.now().year,
        'form': form,
    }
    return render(request, 'app/chessboard.html', context)
