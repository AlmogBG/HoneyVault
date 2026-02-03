from abc import ABC, abstractmethod

class IVaultState(ABC):
    def handle_lock(self,context):
        pass

    def handle_unlock(self,context,password):
        pass

    def hanle_arm(self,context):
        pass

    def handle_intrusion(self, context):
        pass
    