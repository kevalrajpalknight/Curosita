from django.views.generic import TemplateView, ListView
from groups.models import Group
from django.shortcuts import render
from django.db.models import Q

def search(request):
	if request.method == 'GET':
		query= request.GET.get('query')
		submitbutton= request.GET.get('submit')
		if query is not None:
			lookups= Q(name__icontains=query) | Q(description__icontains=query)
			results= Group.objects.filter(lookups).distinct()
			print(results)
			context={'results': results,'submitbutton': submitbutton, 'Group':Group.objects.all()}
			return render(request, 'search.html', context)
		else:
			return render(request, 'search.html',{})
	else:
		return render(request, 'search.html',{})


class HomePage(ListView):
	model = Group
	template_name = 'index.html'
	paginate_by = 10
	queryset = Group.objects.all()


class TestPage(TemplateView):
	template_name = 'test.html'


class ThanksPage(TemplateView):
	template_name = 'thanks.html'