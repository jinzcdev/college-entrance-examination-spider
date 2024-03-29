from abc import abstractmethod


class IProgress:

    @abstractmethod
    def get_progress(self):
        pass

    @abstractmethod
    def save_progress(self):

        pass
