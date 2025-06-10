from abc import ABC, abstractmethod

class BaseEngine(ABC):

    @abstractmethod
    def run(self, jobId, projectName, input, conceptCode, conceptPath, host, jobType):
        pass
