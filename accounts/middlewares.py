# from .models import Profile
# #from django.http.response import HttpResponse

# class RequestProfileMiddleware:

#     def __init__(self , get_response):
#         self.get_response = get_response

#     def __call__(self, request):

#         request.profile = None
#         if request.user.is_authenticated:
#             try:
#                 request.profile = Profile.objects.get(user=request.user)
#             except:
#                 request.profile = None
        
#         response = self.get_response(request)
#         return response