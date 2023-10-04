from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

def project_manager_required(function=None):
    '''
    Decorator for views that checks that the logged-in user is a project manager,
    redirects to the task listing page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_project_manager,
        login_url=reverse_lazy('task-listing'),
        # redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
