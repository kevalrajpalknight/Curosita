# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from groups.models import Group, GroupMember
from . import models 
# Create your views here.
class CreateGroup(LoginRequiredMixin, generic.CreateView):
	fields = ['name', 'description']

	model = Group

class SingleGroup(generic.DetailView):
	model = Group

class ListGroup(generic.ListView):
	model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		return reverse_lazy('groups:single', kwargs={'slug':self.kwargs.get('slug')})
	def get(self, request, *args, **kwargs):
		group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
		try:
			GroupMember.objects.create(user=self.request.user, group=group)
		except:
			messages.warning(self.request, 'warning already a member!')
		else:
			messages.success(self.request,"You are a member now")
		
		return super().get(self.request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
	def get_redirect_url(self, *agrs, **kwargs):
		return reverse_lazy('groups:single', kwargs={'slug':kwargs.get('slug')})

	def get(self, request, *args, **kwargs):
		try:
			membership = models.GroupMember.objects.filter(user = self.request.user,group__slug=self.kwargs.get('slug')).get()
		except models.GroupMember.DoesNotExist:
			messages.warning(self.request,"You are Not in the Group!")
		else:
			membership.delete()
			messages.success(self.request,'You have left the group!')
		return super().get(request, *args, **kwargs)