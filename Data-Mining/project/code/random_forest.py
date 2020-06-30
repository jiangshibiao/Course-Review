import copy
import numpy as np

import multiprocessing
from collections import Counter


class RandomForest:
    '''Random Forest Classifier.

    Note that this class only support binary classification.
    '''

    def __init__(self,
                 base_learner,
                 n_estimator,
                 is_parallel = False,
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
        self.is_parallel = is_parallel

    def _get_bootstrap_dataset(self, X, y):
        """Create a bootstrap dataset for X.

        Args:
            X: training features, of shape (N, D). Each X[i] is a training sample.
            y: vector of training labels, of shape (N,).

        Returns:
            X_bootstrap: a sampled dataset, of shape (N, D).
            y_bootstrap: the labels for sampled dataset.
        """
        # YOUR CODE HERE
        # TODO: re‐sample N examples from X with replacement
        # begin answer
        chosen_data = np.random.choice(np.arange(0, X.shape[0]), X.shape[0], replace=True)
        return X[chosen_data], y[chosen_data]
        # end answer

    def fit(self, X, y):
        """Build the random forest according to the training data.

        Args:
            X: training features, of shape (N, D). Each X[i] is a training sample.
            y: vector of training labels, of shape (N,).
        """
        # YOUR CODE HERE
        # begin answer
        for estimator in self._estimators:
            estimator.fit(X, y)
        # end answer
        return self
    
    def parallel_vote(self, idx, idy, y_pred_origin, y_pred):
        number, times = Counter(y_pred_origin.T[idx]).most_common(1)[0]
        y_pred[idx] = number
    
    def parallel_predict(self, idx, idy, y_pred_origin, X):
        print (idx)
        for i in range(idx, idy):
            y_pred_origin[i] = self._estimators[i].predict(X)

    def predict(self, X):
        """Predict classification results for X.

        Args:
            X: testing sample features, of shape (N, D).

        Returns:
            (np.array): predicted testing sample labels, of shape (N,).
        """
        N = X.shape[0]
        y_pred = np.zeros(N)
        y_pred_origin = np.zeros((self.n_estimator, N))
        # YOUR CODE HERE
        # begin answer
        print (self.is_parallel)

        if not self.is_parallel:
            for idx in range(self.n_estimator):
                y_pred_origin[idx] = self._estimators[idx].predict(X)
        else:
            parts = 4
            number = (self.n_estimator + parts - 1) // parts
            for idx in range(0, N, number):
                idy = min(idx + number, N)
                p = multiprocessing.Process(target = self.parallel_predict, args = (idx, idy, y_pred_origin, X))
                p.start()

        print (self.is_parallel)
        #if not self.is_parallel:
        for idx in range(N):
            number, times = Counter(y_pred_origin.T[idx]).most_common(1)[0]
            y_pred[idx] = number
        else:   
            for idx in range(0, N, number):
                idy = min(idx + number, N)
                p = multiprocessing.Process(target = self.parallel_vote, args = (idx, idy, y_pred_origin, y_pred))
                p.start()

            
        # end answer
        return y_pred
