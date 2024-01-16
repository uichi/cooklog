from django.views import generic

class Contact(generic.TemplateView):
    template_name = 'contact/contact.html'