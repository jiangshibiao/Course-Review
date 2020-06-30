import copy
import numpy as np
import math


class GBDT:
    '''GBDT Classifier.

    Note that this class only support binary classification.
    '''

    def __init__(self,
                 base_learner,
                 n_estimator,
                 learning_rate,
                 seed=2020):
        '''Initialize the classifier.

        Args:
            base_learner: the base_learner should provide the .fit(), .predict() and .calc_leaves(learning_rate) interface.
            n_estimator (int): The number of base learners in RandomForest.
            learning_rate(float): learning_rate
            seed (int): random seed
            
        '''
        np.random.seed(seed)
        self.base_learner = base_learner
        self.n_estimator = n_estimator
        self._estimators = [copy.deepcopy(self.base_learner) for _ in range(self.n_estimator)]
        self.learning_rate = learning_rate
        self.f = [0] * (self.n_estimator+1)

    def fit(self, X, y):
        """Build the Adaboost according to the training data.

        Args:
            X: training features, of shape (N, D). Each X[i] is a training sample.
            y: vector of training labels, of shape (N,).
        """
        N = X.shape[0]
        y = np.array(y)
        positive = np.sum(y) / N
        self.f[0] = np.full(N, math.log(positive / (1 - positive)))
        for idx in range(self.n_estimator):
            res = y - 1 / (1 + np.exp(-self.f[idx]))
            dt = self._estimators[idx]
            new_f = dt.fit(X, y, res)
            self.f[idx+1] = self.f[idx] + self.learning_rate * new_f
            
        return self

    def predict(self, X):
        """Predict classification results for X.

        Args:
            X: testing sample features, of shape (N, D).

        Returns:
            (np.array): predicted testing sample labels, of shape (N,).
        """
        N = X.shape[0]
        y_pred = np.zeros(N)
        y_real = np.zeros(N)
        # YOUR CODE HERE
        # begin answer
        for i in range(N):
            F = self.f[0][0] + self.learning_rate * sum([dt.predict(X[i:i+1])[0] for dt in self._estimators])
            
            val = 1.0 / (1.0 + math.exp(-F))
            y_real[i] = val
            y_pred[i] = 1 if val >= 0.5 else 0
            #print (F, val, y_pred[i])
        # end answer
        return y_pred, y_real
