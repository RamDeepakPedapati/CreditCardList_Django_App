import django,os,sys
from django.forms import ModelForm
from django import forms
os.environ['DJANGO_SETTINGS_MODULE']="myproject.settings"
django.setup()
from myapp.models import *
from django.shortcuts import render, redirect, loader, get_object_or_404
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



class AddCard(ModelForm):
    class Meta:
        model=Customer
        exclude={'id','name_on_card'}

        # fields={'friendly_name','expiry_date','type_of_card','cvv','card_no'}

        widgets={
            'friendly_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter name of the card'}),
            'expiry_date':forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','placeholder':'Enter Date YYYY-MM-DD'}),
            'type_of_card': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter type of the card'}),
            'cvv': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter CVV'}),
            'card_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Card Number'})
        }


class CreateCardView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = '/login/'
    model = Customer
    form_class = AddCard
    template_name = 'customerForm.html'

    def has_permission(self):
        pk = self.kwargs['name_on_card_id']
        user_id = self.request.user.id
        # check_user = Customer.objects.get(pk=pk).name_on_card_id

        if not user_id == pk:
            self.raise_exception = True
            return False
        else:
            return True



    def get_context_data(self, **kwargs):
        context=super(CreateCardView,self).get_context_data(**kwargs)
        return context

    def post(self,request,*args,**kwargs):
        user_name = get_object_or_404(User,pk=kwargs['name_on_card_id'])
        customer_form = AddCard(request.POST)

        if customer_form.is_valid():
            customer = customer_form.save(commit=False)
            customer.name_on_card = user_name
            customer.save()


        return redirect('myapp:cards', self.kwargs.get('name_on_card_id'))




class UpdateCardView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Customer
    form_class = AddCard
    template_name = 'customerForm.html'
    def has_permission(self):
        pk = self.kwargs['pk']
        user_id = self.request.user.id
        check_user = Customer.objects.get(pk=pk).name_on_card_id
        if not user_id == check_user:
            self.raise_exception = True
            return False
        else:
            return True


    def get_context_data(self, **kwargs):
        context = super(UpdateCardView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(pk=kwargs.get('pk'))
        form = AddCard(request.POST, instance=customer)
        form.save()
        return redirect('myapp:cards', self.kwargs.get('name_on_card_id'))



class DeleteCardView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/login/'
    model=Customer
    template_name = 'ConfirmDeleteCollege.html'
    success_url = reverse_lazy('myapp:login')


    def has_permission(self):
        pk = self.kwargs['pk']
        user_id = self.request.user.id
        # import ipdb
        # ipdb.set_trace()
        check_user = Customer.objects.get(pk=pk).name_on_card_id

        if not user_id == check_user:
            self.raise_exception = True
            # success_url = reverse_lazy('creditsapp:cards')
            return False
        else:
            return True



    def get(self,request,*args,**kwargs):
         return self.post(request,args,kwargs)

    def post(self,request,*args,**kwargs):
        self.delete(request,args,kwargs)
        return redirect('myapp:cards', self.kwargs.get('name_on_card_id'))




class CustomerListView(LoginRequiredMixin,ListView):
    login_url='/login/'
    model = Customer
    context_object_name = 'customers'
    template_name = 'CardsList.html'




    def get_context_data(self, *args, object_list=None, **kwargs):

        context = super(CustomerListView, self).get_context_data(**kwargs)
        customer=self.request.user
        u=User.objects.get(username=customer)
        customer=context.get('customer')

        customers=list(Customer.objects.values().filter(name_on_card=u))
        context.update({
            'customers':customers,
            'user_permissions':self.request.user.get_all_permissions()
        })


        return context






















# class CustomerDetailView(DetailView):
#
#     template_name = 'CardsList.html'
#     model=Customer
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(User, **self.kwargs)
#
#     def get_context_data(self,**kwargs):
#         context=super(CustomerDetailView,self).get_context_data(**kwargs)
#         customer=self.request.user
#         u=User.objects.get(username=customer)
#         customer=context.get('customer')
#         context['customerID'] = customer.name_on_card_id
#         customers=list(Customer.objects.values().filter(name_on_card=u))
#         context.update({
#             'customers':customers,
#             'user_permissions':self.request.user.get_all_permissions()
#         })
#         return context
#
#
#         # import ipdb
#         # ipdb.set_trace()
