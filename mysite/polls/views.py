from django.template import loader
from django.shortcuts import get_object_or_404, render, Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
# Create your views here.
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    #tries to get the question fitting to the request
    question = get_object_or_404(Question, pk=question_id)
    #tries to post the ID of the choice
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #If the choice was not correct it redisplays using detail.html
    #and sends an error message
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    #if the except is not raised, the choice count is incremented by on_delete
    #and saved to the database
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #Aside: user is redirected following the pattern for the polls app in results
        #saved in urls.py and the question.id is sent as an argument
        #it will redirect to an url like "'/polls/3/results/'"
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
