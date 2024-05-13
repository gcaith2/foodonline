from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile



@receiver(post_save, sender=User)    
def post_save_create_profile_reciever(sender,instance, created, **kwargs):
        print(created)
        if created:
            UserProfile.objects.create(user=instance)
            print('user profile is created')
        else:
            try:
                profile= UserProfile.objects.get(user=instance)
                profile.save()
            except:
                #Create the userprofile if not exist
                UserProfile.objects.create(user=instance)
                print('Profile does not exist so created one')
            print('user profile is updated')

@receiver(pre_save, sender=User)
def pre_save_profile_reciever(sender, instance, **kwargs):
        print(instance.username,'this is being saved')
post_save.connect(post_save_create_profile_reciever, sender=User)

        
    #post_save.connect(post_save_create_profile_reciever, sender=User)

