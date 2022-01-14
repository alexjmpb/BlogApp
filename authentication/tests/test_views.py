from django.test import TestCase
from django.urls import reverse
from authentication.models import UserBlog
from authentication.views import login_user, register_user

user_data = {
    'username' : 'testuser',
    'email' : 'test@test.com',
    'password1' : 'Testpass10', 
    'password2' : 'Testpass10'
}

class TestAuthViews(TestCase):
    def test_register_view_post(self):
        rqst = reverse('register')
        resp = self.client.post(rqst, data=user_data)
        form = resp.context.get('register_form')
        user = None
        if form.is_valid():
            form.save()
            user = UserBlog.objects.get(username='testuser')
            self.assertEqual(user, form.save())
        self.assertEqual(resp.status_code, 200)

    def test_register_view_post_invalid(self):
        user_data['password1'] = 'Te'
        rqst = reverse('register')
        resp = self.client.post(rqst, data=user_data)
        form = resp.context['form']
        self.assertEqual(resp.status_code, 200)
    
    def test_register_view_get(self):
        rqst = reverse('register')
        resp = self.client.get(rqst)
        form = resp.context['form']
        self.assertEqual(resp.status_code, 200)

    def test_password_change_view(self):
        user = UserBlog.objects.create_user(username=user_data['username'], email=user_data['email'], password=user_data['password1'])
        login = self.client.login(username='testuser', password='Testpass10')
        rqst = self.client.post('/user/password_change/', data={'old_password' : 'Testpass10', 'new_password1' : 'Testpass120', 'new_password2' : 'Testpass120'})
        resp = self.client.get(rqst.url, change_successful=True)
        print(resp.__dir__(), resp.context)


        