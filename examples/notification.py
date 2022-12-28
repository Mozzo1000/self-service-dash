import platform

class NotificationTest:
    def __init__(self, parent):
        self.parent = parent

    def onClick(self):
        if self.parent.get_notification_state():
            self.parent.set_notification_pending(False)
        else:
            self.parent.set_notification_pending(True)