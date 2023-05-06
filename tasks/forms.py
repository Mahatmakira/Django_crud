from django import forms
from .models import Task

##se crean los formulario basandose en los modelos de las tablas
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "descripcion", "important"]
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 
                                            'placeholder': 'Escriba titulo de la tarea'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control',
                                          'placeholder': 'Escriba descripción de la tarea'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input'})
        }