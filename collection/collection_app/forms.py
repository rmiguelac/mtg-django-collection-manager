from django import forms


class AddCardForm(forms.Form):

    name = forms.CharField(label='Card Name', max_length=144, required=True)
    set_name = forms.CharField(label='Set Name', max_length=144, required=True)
    condition = forms.CharField(label='Condition', max_length=2, required=True)
    is_foil = forms.BooleanField(label='Foil', required=False, initial=False)
    quantity = forms.IntegerField(label='Quantity', required=True)
