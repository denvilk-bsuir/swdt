from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class UserContestMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            contest = self.get_contest(kwargs['id'])
            if request.user.profile != contest.author \
                and request.user.profile not in contest.users.all():
                messages.error(request, _("NoContestAccess"))
                return redirect('index')
        return super().dispatch(request, *args, **kwargs)