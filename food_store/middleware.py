from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_routes = ['/cart/', '/checkout/', '/my-orders/', '/add-to-cart/']
        
        if not request.user.is_authenticated:
            current_path = request.path
            if any(current_path.startswith(route) for route in protected_routes):
                messages.warning(request, 'Vui lòng đăng nhập để tiếp tục.')
                login_url = reverse('food_store:login')
                return redirect(f'{login_url}?next={current_path}')
        
        response = self.get_response(request)
        return response 