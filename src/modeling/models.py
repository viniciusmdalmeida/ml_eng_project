#modelos
#Modelos de regressão Sklearn
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

#Imports para classe abstrada
from abc import ABC, abstractmethod
 

class AbstractModel(ABC):
    @abstractmethod
    def fit(self, X, y):
        pass
    
    @abstractmethod
    def predict(self, X):
        return self._decision_function(X)

    @abstractmethod
    def get_parmns():
        pass
    
class ConcretModel(AbstractModel):
    def fit(self,x,y):
        pass
    
    def predict(self,x):
        pass
    
    def get_parmns():
        pass