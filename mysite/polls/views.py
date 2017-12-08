# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.template import loader

from django.shortcuts import get_object_or_404, render

from django.urls import reverse

from django.views import generic

from django.utils import timezone

from .models import Question, Choice

# Create your views here
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	try:
		selected_choice = question.choice_set.get(pk = request.Post['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(Request, 'polls/detail.html',{
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))

def resultData(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	choices = question.choice_set.all()
	votes = [choice.votes for choice in choices]
	return JsonResponse({ 'votes': votes })
