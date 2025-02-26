import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, Referral

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def update_referral_status(sender, instance, created, **kwargs):
    # Log when the signal is triggered
    logger.info(f"Signal triggered for user: {instance.username}")

    if created and instance.referred_by:
        logger.info(f"New user created: {instance.username} with referrer {instance.referred_by.username}")

        # Looking for a reference record for this user
        referral = Referral.objects.filter(referred_user=instance).first()
        if referral:
            logger.info(f"Referral found for user: {instance.username}")
            referral.status = Referral.SUCCESSFUL
            referral.reward_earned = 10
            referral.save()
            logger.info(f"Referral status updated to 'successful'")
        else:
            logger.warning(f"No referral found for user: {instance.username}")


