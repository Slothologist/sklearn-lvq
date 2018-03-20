import numpy as np


from sklearn.utils.testing import assert_greater, assert_raise_message, check_docstring_parameters

from sklearn import datasets
from sklearn.utils import check_random_state
from sklearn.utils.estimator_checks import check_estimator

# also load the iris dataset
from rslvq import LmrslvqModel
from rslvq import MrslvqModel
from rslvq import RslvqModel

iris = datasets.load_iris()
rng = check_random_state(42)
perm = rng.permutation(iris.target.size)
iris.data = iris.data[perm]
iris.target = iris.target[perm]

def test_rslvq_iris():
    check_estimator(RslvqModel)
    model = RslvqModel()
    model.fit(iris.data, iris.target)
    assert_greater(model.score(iris.data, iris.target), 0.94)

    assert_raise_message(ValueError, 'display must be a boolean',
                         RslvqModel(display='true').fit, iris.data, iris.target)
    assert_raise_message(ValueError, 'gtol must be a positive float',
                         RslvqModel(gtol=-1.0).fit, iris.data, iris.target)
    assert_raise_message(ValueError, 'the initial prototypes have wrong shape',
                         RslvqModel(initial_prototypes=[[1, 1], [2, 2]]).fit,
                         iris.data, iris.target)
    assert_raise_message(ValueError,
                         'prototype labels and test data classes do not match',
                         RslvqModel(initial_prototypes=[[1, 1, 1, 1, 'a'],
                                                       [2, 2, 2, 2, 5],
                                                       [2, 2, 2, 2, -3]]).fit,
                         iris.data, iris.target)
    assert_raise_message(ValueError, 'max_iter must be an positive integer',
                         RslvqModel(max_iter='5').fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError, 'max_iter must be an positive integer',
                         RslvqModel(max_iter=0).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError, 'max_iter must be an positive integer',
                         RslvqModel(max_iter=-1).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError,
                         'values in prototypes_per_class must be positive',
                         RslvqModel(prototypes_per_class=np.zeros(
                             np.unique(iris.target).size) - 1).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError,
                         'length of prototypes per class'
                         ' does not fit the number of',
                         RslvqModel(prototypes_per_class=[1, 2]).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError, 'X has wrong number of features',
                         model.predict, [[1, 2], [3, 4]])


def test_mrslvq_iris():
    check_estimator(MrslvqModel)
    model = MrslvqModel()
    model.fit(iris.data, iris.target)
    assert_greater(model.score(iris.data, iris.target), 0.94)

    assert_raise_message(ValueError, 'regularization must be a positive float',
                         MrslvqModel(regularization=-1.0).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError,
                         'initial matrix has wrong number of features',
                         MrslvqModel(
                             initial_matrix=[[1, 2], [3, 4], [5, 6]]).fit,
                         iris.data, iris.target)
    assert_raise_message(ValueError, 'dim must be an positive int',
                         MrslvqModel(dim=0).fit, iris.data, iris.target)

def test_lmrslvq_iris():
    check_estimator(LmrslvqModel)
    model = LmrslvqModel()
    model.fit(iris.data, iris.target)
    assert_greater(model.score(iris.data, iris.target), 0.94)

    assert_raise_message(ValueError, 'regularization must be a positive float',
                         LmrslvqModel(regularization=-1.0).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError,
                         'length of regularization'
                         ' must be number of prototypes',
                         LmrslvqModel(regularization=[-1.0]).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError,
                         'length of regularization must be number of classes',
                         LmrslvqModel(regularization=[-1.0],
                                     classwise=True).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError, 'initial matrices must be a list',
                         LmrslvqModel(initial_matrices=np.array(
                             [[1, 2], [3, 4], [5, 6]])).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError, 'length of matrices wrong',
                         LmrslvqModel(
                             initial_matrices=[[[1, 2], [3, 4], [5, 6]]]).fit,
                         iris.data, iris.target)
    assert_raise_message(ValueError, 'each matrix should have',
                         LmrslvqModel(
                             initial_matrices=[[[1]], [[1]], [[1]]]).fit,
                         iris.data, iris.target)
    assert_raise_message(ValueError, 'length of matrices wrong',
                         LmrslvqModel(initial_matrices=[[[1, 2, 3]]],
                                     classwise=True).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError, 'each matrix should have',
                         LmrslvqModel(initial_matrices=[[[1]], [[1]], [[1]]],
                                     classwise=True).fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError, 'classwise must be a boolean',
                         LmrslvqModel(classwise="a").fit, iris.data,
                         iris.target)
    assert_raise_message(ValueError, 'dim must be a list of positive ints',
                         LmrslvqModel(dim=[-1]).fit, iris.data, iris.target)
    assert_raise_message(ValueError, 'dim length must be number of prototypes',
                         LmrslvqModel(dim=[1, 1]).fit, iris.data, iris.target)
    assert_raise_message(ValueError, 'dim length must be number of classes',
                         LmrslvqModel(dim=[1, 1], classwise=True).fit,
                         iris.data, iris.target)

    LmrslvqModel(classwise=True, dim=[1], prototypes_per_class=2).fit(
        iris.data, iris.target)

    model = LmrslvqModel(regularization=0.1)
    model.fit(iris.data, iris.target)
