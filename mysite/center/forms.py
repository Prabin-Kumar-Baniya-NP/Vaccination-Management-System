from django.forms import ModelForm
from center.models import Center, Storage


class CreateCenterForm(ModelForm):
    """
    Form to create new center
    """

    def __init__(self, *args, **kwargs):
        super(CreateCenterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Center
        fields = "__all__"


class UpdateCenterForm(ModelForm):
    """
    Form to update the center
    """

    def __init__(self, *args, **kwargs):
        super(UpdateCenterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Center
        fields = "__all__"


class CreateStorageForm(ModelForm):
    """
    Form to create new storage for given center
    """

    def __init__(self, center_id, *args, **kwargs):
        super(CreateStorageForm, self).__init__(*args, **kwargs)
        self.fields["center"].queryset = Center.objects.filter(id=center_id)
        self.fields['center'].disabled = True
        self.fields['booked_quantity'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Storage
        fields = "__all__"


class UpdateStorageForm(ModelForm):
    """
    Form to update the storage for given center
    """

    def __init__(self, center_id, *args, **kwargs):
        super(UpdateStorageForm, self).__init__(*args, **kwargs)
        self.fields["center"].queryset = Center.objects.filter(id=center_id)
        self.fields['center'].disabled = True
        self.fields['vaccine'].disabled = True
        self.fields['booked_quantity'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Storage
        fields = "__all__"
