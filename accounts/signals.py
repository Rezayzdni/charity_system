
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save,m2m_changed
# from accounts.models import Profile , Website

# @receiver(post_save,sender = User )
# def create_user_profile(sender , instance , created , **kwargs):
#     if created:
#         Profile.objects.create(user = instance)

# def update_bio(user):
#     websites = user.website_set.all()
#     urls = []
#     for web in websites:
#         urls.append(web.url)
#     sorted_urls = sorted(urls)
#     final_urls = '\n'.join(sorted_urls)
#     user_profile = Profile.objects.get(user = user)
#     user_profile.bio = final_urls
#     user_profile.save()

# @receiver(m2m_changed, sender=Website.users.through)
# def do_something(sender, instance, action, reverse, model, pk_set,**kwargs):
#     if pk_set:
#         user = None
#         if reverse:
#             user = instance
#             update_bio(user)
#         else:
#             for pik in pk_set: 
#                 user = User.objects.get(id = pik)
#                 update_bio(user)