from .models import Notification

def notifications_toutes(request):
    notifications_ordinaire = Notification.objects.all().order_by('date_notification', 'heure_notification')
    
    # Filtrez les notifications pour s'assurer qu'elles ont les champs nécessaires
    notifications = [notification for notification in notifications_ordinaire if hasattr(notification, 'date_notification')]
    
    # Triez les notifications
    notifications = sorted(notifications, key=lambda x: (x.date_notification))

    return {'notifications_toutes': notifications}
