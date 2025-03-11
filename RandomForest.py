import numpy as np
from collections import Counter
from joblib import Parallel, delayed
# from scipy.stats import entropy

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def is_leaf_node(self):
        return self.value is not None

class DecisionTree:
    def __init__(self, min_samples_split=2, max_depth=10, n_features=None):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.root = None

    def fit(self, X, y):
        self.n_features = X.shape[1] if not self.n_features else min(X.shape[1], self.n_features)
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_labels = X.shape[0], len(np.unique(y))
        if depth >= self.max_depth or n_labels == 1 or n_samples < self.min_samples_split:
            return Node(value=self._most_common_label(y))

        feat_idxs = np.random.choice(X.shape[1], self.n_features, replace=False)
        best_feature, best_thresh, best_split = self._best_split(X, y, feat_idxs)

        if best_feature is None:
            return Node(value=self._most_common_label(y))

        left_idxs, right_idxs = best_split
        left = self._grow_tree(X[left_idxs], y[left_idxs], depth + 1)
        right = self._grow_tree(X[right_idxs], y[right_idxs], depth + 1)

        return Node(best_feature, best_thresh, left, right)

    def _best_split(self, X, y, feat_idxs):
        best_gain = -1
        split_idx, split_threshold = None, None
        best_split = None

        for feat_idx in feat_idxs:
            X_column = X[:, feat_idx]
            thresholds = np.unique(X_column)

            for thr in thresholds:
                left_idxs = np.where(X_column <= thr)[0]
                right_idxs = np.where(X_column > thr)[0]

                if len(left_idxs) == 0 or len(right_idxs) == 0:
                    continue

                gain = self._information_gain(y, left_idxs, right_idxs)
                if gain > best_gain:
                    best_gain = gain
                    split_idx = feat_idx
                    split_threshold = thr
                    best_split = (left_idxs, right_idxs)

        return split_idx, split_threshold, best_split

    def _information_gain(self, y, left_idxs, right_idxs):
        parent_entropy = self._entropy(y)
        n = len(y)
        n_l, n_r = len(left_idxs), len(right_idxs)
        e_l, e_r = self._entropy(y[left_idxs]), self._entropy(y[right_idxs])
        return parent_entropy - (n_l/n) * e_l - (n_r/n) * e_r

    def _entropy(self, y):
        hist = np.bincount(y)
        ps = np.divide(hist, len(y), dtype=np.float32)
        return -np.sum(ps * np.log2(ps, where=(ps > 0)))  # Faster entropy calculation
    
    # def _entropy(self, y):
    #     hist = np.bincount(y)
    #     ps = hist / hist.sum()
    #     return entropy(ps, base=2)  # Faster than np.log2()

    def _most_common_label(self, y):
        return np.bincount(y).argmax()

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value
        return self._traverse_tree(x, node.left if x[node.feature] <= node.threshold else node.right)

class RandomForest:
    def __init__(self, n_trees=100, max_depth=10, min_samples_split=2, max_features=None, n_jobs=-1):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.n_jobs = n_jobs
        self.trees = []

    def fit(self, X, y):
        X = X.astype(np.float32)  # Reduce memory usage
        if self.max_features is None:
            self.max_features = int(np.sqrt(X.shape[1]))

        self.trees = Parallel(n_jobs=min(self.n_jobs, 2))(  # Reduce parallel jobs
            delayed(self._train_tree)(X, y) for _ in range(self.n_trees)
        )

    def _train_tree(self, X, y):
        tree = DecisionTree(
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            n_features=self.max_features
        )
        X_sample, y_sample = self._bootstrap_samples(X, y)
        tree.fit(X_sample, y_sample)
        return tree

    def _bootstrap_samples(self, X, y):
        n_samples =  X.shape[0] 
        idxs = np.random.choice(X.shape[0], n_samples, replace=True)
        return X[idxs], y[idxs]

    def predict(self, X):
        X = X.astype(np.float32)  # Reduce memory usage
        predictions = np.array(
            Parallel(n_jobs=min(self.n_jobs, 2))(  # Reduce jobs
                delayed(tree.predict)(X) for tree in self.trees
            )
        )
        tree_preds = np.swapaxes(predictions, 0, 1)
        return np.array([self._most_common_label(pred) for pred in tree_preds])

    def _most_common_label(self, y):
        return Counter(y).most_common(1)[0][0]