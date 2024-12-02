from abc import ABC, abstractmethod

class BaseEngine(ABC):

    @abstractmethod
    def run(self, jobId, projectName, conceptBlob, conceptCode, conceptPath, node, dType):
        pass
