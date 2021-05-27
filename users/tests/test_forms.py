from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from users import forms


class TestUserRegisterForm:

    # def test_UserRegisterForm(self, user1):
    #     data = {
    #         "username":user1.username,
    #         "email":user1.email,
    #         "password1":password,
    #         "password2":password
    #         }
    #     form = forms.UserRegisterForm(data=data)
    #     assert form.is_valid()

    def test_UserUpdateForm(self, user1):
        data = {
            "email": "email@email.com",
        }
        form = forms.UserUpdateForm(data=data)
        assert form.is_valid()

    def test_ProfileUpdateForm(self, profile):
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        data = {
            "display_name": "jeffrey",
            "image": image,
            "bio": "this is a bio",
            "location": "UK",
            "website": "https://google.com",
        }
        form = forms.ProfileUpdateForm(data=data)
        assert form.is_valid()
