import copy
import numpy as np
import math


class Adaboost:
    '''Adaboost Classifier.

    Note that this class only support binary classification.
    '''

    def __init__(self,
                 base_learner,
                 n_estimator,
                 seed=2020):
        '''Initialize the classifier.

        Args:
            base_learner: the base_learner should provide the .fit() and .predict() interface.
            n_estimator (int): The number of base learners in RandomForest.
            seed (int): random seed
        '''
        np.random.seed(seed)
        self.base_learner = base_learner
        self.n_estimator = n_estimator
        self._estimators = [copy.deepcopy(self.base_learner) for _ in range(self.n_estimator)]
        self._alphas = [1 for _ in range(n_estimator)]

    def fit(self, X, y):
        """Build the Adaboost according to the training data.

        Args:
            X: training features, of shape (N, D). Each X[i] is a training sample.
            y: vector of training labels, of shape (N,).
        """
        # YOUR CODE HERE
        # begin answer
        N = X.shape[0]
        sample_weights = np.full(N, 1.0 / N)
        for idx in range(self.n_estimator):
            dt = self._estimators[idx]
            dt.fit(X, y, sample_weights)
            pred = dt.predict(X)
            err = np.sum(sample_weights[pred != y])
            #print (pred, err)
            self._alphas[idx] = 0.5 * math.log((1 - err) / err, 2)
            sample_weights[pred == y] *= np.exp(-self._alphas[idx])
            sample_weights[pred != y] *= np.exp(self._alphas[idx])
            sample_weights /= np.sum(sample_weights)
            #print (idx, sample_weights)
        #print (self._alphas)
        # end answer
        return self

    @staticmethod
    def calc_times(y, sample_weights):
        label2number = {}
        for l, w in zip(y, sample_weights):
            if not l in label2number:
                label2number[l] = 0.0
            label2number[l] += w
        return label2number

    def predict(self, X):
        """Predict classification results for X.

        Args:
            X: testing sample features, of shape (N, D).

        Returns:
            (np.array): predicted testing sample labels, of shape (N,).
        """
        N = X.shape[0]
        y_pred = np.zeros(N)
        # YOUR CODE HERE
        # begin answer
        for i in range(N):
            now_pred = [dt.predict(X[i:i+1])[0] for dt in self._estimators]
            label2number = self.calc_times(now_pred, self._alphas)
            y_pred[i] = max(label2number, key = label2number.get)
        # end answer
        return y_pred
