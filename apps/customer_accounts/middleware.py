from django_multitenant.utils import set_current_tenant, unset_current_tenant


class MultitenantMiddleware:
    '''
    currently Middlware forces every user to have current tenant
    tenant is read from user.profile.account
    '''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.is_authenticated:
            current_tenant = request.user.profile.account
            set_current_tenant(current_tenant)
        response = self.get_response(request)

        """
        The following unsetting of the tenant is essential because of how webservers work
        Since the tenant is set as a thread local, the thread is not killed after the request is processed
        So after processing of the request, we need to ensure that the tenant is unset
        Especially required if you have public users accessing the site

        This is also essential if you have admin users not related to a tenant (not possible in actual citus env)
        """
        unset_current_tenant()

        return response
