from django.test import TestCase
from django.urls import reverse
from authentication.models import UserBlog

class TestAuthViews(TestCase):
    def setUp(self):
        self.user_data = {
            'username' : 'testuser',
            'email' : 'test@test.com',
            'password1' : 'Testpass10', 
            'password2' : 'Testpass10'
        }

    def test_register_view_post(self):
        resp = self.client.post(reverse('register'), data=self.user_data, follow=True)
        self.assertEqual(resp.redirect_chain[0][1], 302)

    def test_register_view_post_invalid(self):
        self.user_data['password1'] = 'Te'
        rqst = reverse('register')
        resp = self.client.post(rqst, data=self.user_data)
        form = resp.context['form']
        self.assertEqual(resp.status_code, 200)
    
    def test_register_view_get(self):
        rqst = reverse('register')
        resp = self.client.get(rqst)
        form = resp.context['form']
        self.assertEqual(resp.status_code, 200)

    def test_password_change_view(self):
        user = UserBlog.objects.create_user(username=self.user_data['username'], email=self.user_data['email'], password=self.user_data['password1'])
        login = self.client.login(username='testuser', password='Testpass10')
        resp = self.client.post(reverse('password_change'), data={'old_password' : 'Testpass10', 'new_password1' : 'Testpass120', 'new_password2' : 'Testpass120'}, follow=True)
        self.assertEqual(resp.redirect_chain[0][1], 302)
        self.assertEqual(resp.status_code, 200)

    def test_update_user_info_view(self):
        self.user_data['username'] = 'testinguser'
        user = UserBlog.objects.create_user(username=self.user_data['username'], email=self.user_data['email'], password=self.user_data['password1'])
        self.client.login(username='testuser', password='Testpass10')
        resp = self.client.post(reverse('update_user_info'), data=self.user_data, follow=True)
        self.assertEqual(resp.redirect_chain[0][1], 302)
        self.assertEqual(resp.status_code, 200)

    def test_delete_user(self):
        user = UserBlog.objects.create_user(username=self.user_data['username'], email=self.user_data['email'], password=self.user_data['password1'])
        self.client.login(username='testuser', password='Testpass10')
        resp = self.client.post(reverse('delete_user', kwargs={'pk' : user.id}), follow=True)
        self.assertEqual(resp.redirect_chain[0][1], 302)
        self.assertEqual(resp.status_code, 200)