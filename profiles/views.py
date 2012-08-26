# Create your views here.
"""
Views for creating, editing and viewing site-specific user profiles.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from models import UserProfile
from profiles import utils



def edit_profile(request, username, form_class=None, success_url=None,
                 template_name='profiles/edit_profile.html',
                 extra_context=None):
    user = get_object_or_404(User, username=username)
    try:
        profile_obj = user.get_profile()
        print user.get_profile().avatar
    except ObjectDoesNotExist:
        raise Http404

    if success_url is None:
        success_url = reverse('profiles_edit_profile',
                              kwargs={ 'username': request.user.username })
    if form_class is None:
        form_class = utils.get_profile_form()
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            if form.cleaned_data['password1']<>'':
                tek_user = User.objects.get(pk = request.user.pk)
                tek_user.set_password(form.cleaned_data['password1'])
                tek_user.save()

            return HttpResponseRedirect(success_url)
    else:
        form = form_class(instance=profile_obj)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              { 'form': form,
                                'profile': profile_obj, },
                              context_instance=context)

edit_profile = login_required(edit_profile)

def profile_detail(request, username, public_profile_field=None,
                   template_name='profiles/profile_detail.html',
                   extra_context=None):
    user = get_object_or_404(User, username=username)
    try:
        profile_obj = user.get_profile()
    except ObjectDoesNotExist:
        raise Http404
    if public_profile_field is not None and \
       not getattr(profile_obj, public_profile_field):
        profile_obj = None

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              { 'profile': profile_obj },
                              context_instance=context)

