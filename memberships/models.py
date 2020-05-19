from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
import stripe

# stripe.api_key = settings.STRIPE_SECRET_KEY

MEMBERSHIP_CHOICES = {
    ('Enterprise','ent'),
    ('Professional','pro'),
    ('Free','free')
}

class Membership(models.Model):
    slug = models.SlugField(max_length = 50)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default="free", max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length = 150)

    class Meta:
        verbose_name = ("membership")
        verbose_name_plural = ("memberships")

    def __str__(self):
        return self.membership_type

    # def get_absolute_url(self):
    #     return reverse("membership_detail", kwargs={"pk": self.pk})


class UserMembershhip(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length = 50)
    membership = models.ForeignKey( Membership, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = ("usermembershhip")
        verbose_name_plural = ("usermembershhips")

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("usermembershhip_detail", kwargs={"pk": self.pk})

def post_save_usermembership_create(sender,instance,created,*args, **kwargs):
    if created:
        UserMembershhip.objects.get_or_create(user=instance)
    user_membership,created = UserMembershhip.objects.get_or_create(user=instance)

    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id =="":
        new_customer_id = stripe.Customer.create(email=instance.email)
        user_membership.stripe_customer_id = new_customer_id['id']
        user_membership.save()

post_save.connect(post_save_usermembership_create, sender=settings.AUTH_USER_MODEL)


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembershhip, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField( max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username


