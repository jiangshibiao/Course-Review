import numpy as np
import math


class BinaryDecisionTree:
    '''Binary Decision Tree Classifier.
    '''

    def __init__(self,
                 max_depth,
                 min_samples_leaf):
        '''Initialize the classifier.

        Args:
            max_depth (int): the max depth for the decision tree. This parameter is
                a trade-off between underfitting and overfitting.
            min_samples_leaf (int): the minimal samples in a leaf. This parameter is a trade-off
                between underfitting and overfitting.
            
        '''
        self._tree = None
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf

    def _calculate(self, y):
        if len(y) == 0: return 0.0
        return np.sum((y - np.mean(y)) ** 2)

    def criterion(self, X, y, index, value):
        left_index = list(X.T[index] <= value)
        right_index = list(X.T[index] > value)
        return self._calculate(y[left_index]) + self._calculate(y[right_index])
    
    def _calc_leaf(self, y, res):
        numerator = np.sum(res)
        denominator = np.sum((y - res) * (1 - y + res))
        #print (y, res, numerator / denominator)
        if abs(denominator) <= 1e-10: 
            denominator = 1e-10 if denominator >= 0 else -1e-10
        return numerator / denominator

    def fit(self, X, y, res):
        """Build the decision tree according to the training data.

        Args:
            X: (pd.Dataframe) training features, of shape (N, D). Each X[i] is a training sample.
            y: (pd.Series) vector of training labels, of shape (N,). y[i] is the label for X[i], and each y[i] is
            an integer in the range 0 <= y[i] <= C. Here C = 1.
        """

        feature_names = X.columns.tolist()
        X = np.array(X)
        y = np.array(y)
        #print (X, y)
        self._tree, new_f = self._build_tree(X, y, res, feature_names, depth=1)
        #print ("new_f", new_f)
        return new_f

    def _choose_best_feature(self, X, y):
        """Choose the best feature to split according to criterion.

        Args:
            X: training features, of shape (N, D).
            y: vector of training labels, of shape (N,).

        Returns:
            (int): the index for the best feature
            (int): the value for the best feature
        """
        best_feature_idx, best_feature_value = 0, 1e100
        D = X.shape[1]
        for idx in range(D):
            valuelist = np.unique(X.T[idx])
            valuelist = [valuelist[0]] + valuelist
            best_value = min([(value, self.criterion(X, y, idx, value)) for value in valuelist], key = lambda x: x[1])[0]
            if best_value < best_feature_value:
                best_feature_value = best_value
                best_feature_idx = idx
        return best_feature_idx, best_feature_value
    
    def _totally_same(self, X):
        for i in range(1, X.shape[0]):
            if not (X[0] == X[i]).all():
                return False
        return True

    def _build_tree(self, X, y, res, feature_names, depth):
        """Build the decision tree according to the data.

        Args:
            X: (np.array) training features, of shape (N, D).
            y: (np.array) vector of training labels, of shape (N,).
            feature_names (list): record the name of features in X in the original dataset.
            depth (int): current depth for this node.

        Returns:
            (dict): a dict denoting the decision tree. 
            (numpy): the value for each leaf. 
            Example:
                mytree = {
                    'titile': {
                        0: subtree0,
                        1: {
                            'pclass': {
                                0: majority_vote([1, 1, 1, 1]) # which is 1, majority_label
                                1: majority_vote([1, 0, 1, 1]) # which is 1
                                'value': value
                            }
                        }
                        'value': value
                    }
                }
        """
        '''print ("--------------------------Sub problem------------------------")
        print (X)
        print (y)
        print (feature_names)
        print (depth)'''

        if len(set(y)) == 1 or self._totally_same(X) or X.shape[0] < self.min_samples_leaf or depth > self.max_depth:
            c = self._calc_leaf(y, res)
            return c, np.full(y.shape[0], c)            
        
        mytree = dict()
        best_index, best_value = self._choose_best_feature(X, res)
        mytree[feature_names[best_index]] = {}
        new_feature_names = feature_names.copy()
        # delete this feature name
        del new_feature_names[best_index] 

        # split data
        l_data, r_data = X.T[best_index] <= best_value, X.T[best_index] > best_value
        l_X, l_y, l_res = np.delete(X[l_data], best_index, axis = 1), y[l_data], res[l_data]
        r_X, r_y, r_res = np.delete(X[r_data], best_index, axis = 1), y[r_data], res[r_data]

        # new_f will be reunioned
        new_f = np.zeros(X.shape[0])
        mytree[feature_names[best_index]][0], new_f[l_data] = self._build_tree(l_X, l_y, l_res, new_feature_names, depth + 1)
        mytree[feature_names[best_index]][1], new_f[r_data] = self._build_tree(r_X, r_y, r_res, new_feature_names, depth + 1)
        mytree[feature_names[best_index]]['value'] = best_value

        return mytree, new_f

    def predict(self, X):
        """Predict classification results for X.

        Args:
            X: (pd.Dataframe) testing sample features, of shape (N, D).

        Returns:
            (np.array): predicted testing sample labels, of shape (N,).
        """
        if self._tree is None:
            raise RuntimeError("Estimator not fitted, call `fit` first")

        def _classify(tree, x):
            """Classify a single sample with the fitted decision tree.

            Args:
                x: ((pd.Dataframe) a single sample features, of shape (D,).

            Returns:
                (int): predicted testing sample label.
            """
            # YOUR CODE HERE
            # begin answer
            if type(tree) == dict:
                feature_name, content = list(tree.items())[0]
                now_value = x[feature_name].values[0]
                if now_value <= content['value']:
                    return _classify(content[0], x)
                else:
                    return _classify(content[1], x)
            else:
                return tree
            # end answer

        # YOUR CODE HERE
        # begin answer
        predict = []
        for i in range(X.shape[0]):
            predict.append(_classify(self._tree, X[i:i+1]))
        return np.array(predict)
        # end answer

    def show(self):
        """Plot the tree using matplotlib
        """
        if self._tree is None:
            raise RuntimeError("Estimator not fitted, call `fit` first")

        import tree_plotter
        tree_plotter.createPlot(self._tree)
