from django import forms


class AddCardForm(forms.Form):

    card_name = forms.CharField(label='Card Name', max_length=144, required=True)
    card_set_name = forms.CharField(label='Set Name', max_length=144, required=True)
    card_condition = forms.CharField(label='Condition', max_length=2, required=True)
    card_is_foil = forms.BooleanField(label='Foil', required=False, initial=False)
    card_quantity = forms.IntegerField(label='Quantity', required=True)