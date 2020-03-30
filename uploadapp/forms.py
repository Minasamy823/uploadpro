from django import forms

from uploadapp.models import Image


class ImageForm(forms.ModelForm):
    url = forms.CharField(label='Image url',
                          widget=forms.URLInput(attrs={
                            'placeholder': 'Your link'})
                          , required=False)

    class Meta:
        model = Image
        exclude = ['hash', ]

    def clean(self):
        url = self.cleaned_data.get('url')
        image = self.cleaned_data.get('image')

        if url and image:
            raise forms.ValidationError('Only one field is required')

        if url == '' and image is None:
            raise forms.ValidationError('At least one field should be filled')


class ParamsForm(forms.Form):
    width = forms.IntegerField(label='Ширина',
                               required=False,
                               widget=forms.NumberInput())
    height = forms.IntegerField(label='Высота',
                                required=False,
                                widget=forms.NumberInput())
    size = forms.IntegerField(label='Макс. размер в байтах',
                              required=False,
                              widget=forms.NumberInput())
