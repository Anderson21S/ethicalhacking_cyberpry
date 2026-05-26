from django import forms
from .models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        # Definimos los campos que el usuario podrá llenar
        fields = ['title', 'description', 'severity', 'resolved']
        
    # El documento pide validar que título y descripción no estén vacío
    # Django ya lo hace por defecto con ModelForm porque en models.py no pusimos blank=True,
    # pero podemos agregar clases CSS aquí para que se vea mejor en HTML.
    def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'