# from django.shortcuts import redirect
# from django.urls import reverse
# from django.contrib import messages
#
#
# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.excluded_paths = [
#             reverse('login'),
#             reverse('apps_list'),
#             reverse('homepage'),
#             reverse('list_currencies'),
#             reverse('get_currency_data'),
#         ]
#
#     def __call__(self, request):
#         if request.path not in self.excluded_paths and not request.user.is_authenticated:
#             messages.warning(request, 'You need to log in to access this page.')
#             return redirect('login')
#
#         response = self.get_response(request)
#         return response
#
