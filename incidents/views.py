from django.shortcuts import get_object_or_404, render, redirect
from .models import Incident
from .forms import IncidentForm

def home(request):
    incidents = Incident.objects.all().order_by('-reported_at')
    
    severity_filter = request.GET.get('severity')
    
    if severity_filter:
        incidents = incidents.filter(severity=severity_filter)
    
    context = {
        'incidents': incidents,
        'current_filter': severity_filter 
    }
    return render(request, 'incidents/home.html', context)


def create(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save() # Guarda en la base de datos PostgreSQL
            return redirect('incidents:home') 
    else:
        form = IncidentForm() 
        
    return render(request, 'incidents/create.html', {'form': form})


def detail(request, pk):

    incident = get_object_or_404(Incident, pk=pk)
    
    return render(request, 'incidents/detail.html', {'incident': incident})



def update(request, pk):
    
    incident = get_object_or_404(Incident, pk=pk)
    
    if request.method == 'POST':
        
        form = IncidentForm(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            
            return redirect('incidents:detail', pk=incident.pk)
    else:
        
        form = IncidentForm(instance=incident)
        
    return render(request, 'incidents/update.html', {'form': form, 'incident': incident})


def delete(request, pk):
    incident = get_object_or_404(Incident, pk=pk)
    
    if request.method == 'POST':
        incident.delete() 
        return redirect('incidents:home') 
        
    return render(request, 'incidents/confirm_delete.html', {'incident': incident})