from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm
from accounts.forms import SignUpForm
from django.shortcuts import render, redirect


class SubmittableLoginView(LoginView):
    template_name = 'accounts/form.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('index')


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm
    return render(request, 'accounts/form.html', {'form': form})
