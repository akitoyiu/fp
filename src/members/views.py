from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordForm, EditUserProfileForm
from familypost.models import UserProfile
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

class RegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class ListProfileView(generic.ListView):
    model = User
    template_name = "registration/ListProfile.html"
    paginate_by = 30 # for pagination
    context_object_name = 'users' # for pagination

    #def get_context_data(self, *args, **kwargs):
    #    cat_menu = Category.objects.all().values('name', 'slug')
    #   context = super(HomeView, self).get_context_data(*args, **kwargs)
    #    context["cat_menu"] = cat_menu
    #    return context

#class EditProfileView(generic.UpdateView):    
#    form_class = EditProfileForm
#    #fields = '__all__'
#    template_name = 'registration/edit_profile.html'
#    success_url = reverse_lazy('Home')
#    
#    def get_object(self):
#        if self.request.user.is_authenticated:       
#            uid = int(self.kwargs['pk'])
#            return get_object_or_404(User, id=uid)
#        else:
#            return None

def EditProfileView (request, uid):
    user = User.objects.get(id=uid)
    if request.method == 'POST': #If form has been submitted
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid(): #All good. Validation passed
            form.save()
            return HttpResponseRedirect(reverse_lazy('list_profile')) # Redirect after POST
    else:
            form = EditProfileForm(instance=user) # Unbound form

    return render(request, 'registration/edit_profile.html', {'form': form})
   

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'registration/password_success.html')


class ShowProfileView(generic.DetailView):
    model = UserProfile
    template_name = "registration/user_profile.html"

    def get_context_data(self, *args, **kwargs):

        pageuser = get_object_or_404(UserProfile, id=self.kwargs['pk'])
        
        context = super(ShowProfileView, self).get_context_data(*args, **kwargs)
        context["pageuser"] = pageuser
        return context


class EditUserProfileView(generic.UpdateView):
    form_class = EditUserProfileForm

    template_name = 'registration/edit_userprofile.html'
    success_url = reverse_lazy('Home')

    def get_object(self):
        if self.request.user.is_authenticated:            
            return self.request.user.userprofile
        else:
            return None
        
