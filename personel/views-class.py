from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.core.urlresolvers import reverse

from django import forms
import forms 
from django.views.generic.edit import FormView


'''
Contact
'''
from .models import Contact
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

#R(1:N)
class EditContactAddressView(UpdateView):

    model = Contact
    template_name = 'edit_addresses.html'
    form_class = forms.ContactAddressFormSet

    def get_success_url(self):

        # redirect to the Contact view.
        return self.get_object().get_absolute_url()



#E
class CreateContactView(CreateView):

    model = Contact
    #fields='__all__'
    template_name = 'edit_contact.html'
    #2.
    form_class = forms.ContactForm
    
    def get_success_url(self):
        return reverse('contacts-list')


    def get_context_data(self, **kwargs):

        context = super(CreateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-new')

        return context


class UpdateContactView(UpdateView):

    model = Contact
    #fields='__all__'
    template_name = 'edit_contact.html'
    #2.
    form_class = forms.ContactForm

    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):

        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-edit',
                                    kwargs={'pk': self.get_object().id})

        return context


class DeleteContactView(DeleteView):

    model = Contact
    template_name = 'delete_contact.html'

    def get_success_url(self):
        return reverse('contacts-list')

 
 
class ContactView(DetailView):

    model = Contact
    template_name = 'contact.html'


class ListContactView(ListView):

    model = Contact
    template_name = 'contact_list.html'







'''
XXXX
class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)

'''

'''
class AccountCreateView(CreateView):

    model = Account

    def get_success_url(self):
        return self.object.account_activated_url()

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminAccountForm
        return AccountForm

    def get_form_kwargs(self):
        kwargs = super(AccountCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def form_valid(self, form):
        send_activation_email(self.request.user)
        return super(AccountCreateView, self).form_valid(form)

'''

#from personel.models import *

# Create your views here.
def home(request):
    return render(request, 'personel/home.html', {'msg': 'Hello'})


class MyView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')


class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)



def detail(request, t_id):
    try:
        t = Teacher.objects.get(pk=t_id)
    except Teacher.DoesNotExist:
        raise Http404("Teacher does not exist")
    return render(request, 'teacher/detail.html', {'teacher': t})




#FORM-VIEW 
def post_form_upload(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        # A POST request: Handle Form Upload
        form = PostForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            content = form.cleaned_data['content']
            created_at = form.cleaned_data['created_at']
            #post = m.Post.objects.create(content=content, created_at=created_at)
            #return HttpResponseRedirect(reverse('post_detail', kwargs={'post_id': post.id}))
            return HttpResponseRedirect(reverse('myview',
                                                kwargs={'content': content, 'cleaned_data': form.cleaned_data, }))


    return render(request, 'post_form_upload.html', {
        'form': form,
    })



