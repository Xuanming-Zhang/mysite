from django.shortcuts import render
from django.views.generic.base import View
from apps.organizations.models import CourseOrg


# Create your views here.
class OrgView(View):
    def get(self, request, *args, **kwargs):
        all_orgs = CourseOrg.objects.all()
        return render(request, "org-list.html", {
            "all_orgs": all_orgs,
        })
