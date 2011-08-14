from django import forms
from django.forms.models import ModelForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from expenses.models import Transaction, Household, Person, Invited

__author__ = 'jackdreilly'


class HouseholdTransactionForm(ModelForm):

    household = forms.ModelChoiceField(widget=forms.HiddenInput(),queryset=Household.objects.all())
    class Meta:
        model = Transaction

    def __init__(self,*args,**kwargs):
        try:
            super(HouseholdTransactionForm,self).__init__(*args, **kwargs)
            if self.instance:
                persons = self.instance.household.persons
            elif self.initial.has_key('household'):
                persons  = self.initial['household'].persons
            else:
                persons = Person.objects.all()
            self.fields['transactor'].queryset = persons
        except:
            "you suck" 

    

class InviteToHouseholdForm(ModelForm):

    household = forms.ModelChoiceField(widget=forms.HiddenInput(),queryset=Household.objects.all())
    invited_user = forms.CharField(max_length=100, label='username')
    
    class Meta:
        model = Invited
        exclude = ('user',)
    
    def save(self, commit=True):
# don't really get this, just copied it from stackoverflow
		m = super(InviteToHouseholdForm, self).save(commit=False)
		m.user = User.objects.get(username=str(invited_user))
		if commit:
			m.save()
		
		return m
    
    


    
