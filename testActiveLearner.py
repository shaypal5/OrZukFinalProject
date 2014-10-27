# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 18:33:19 2014

@author: Shay
"""

from UncertaintySampleSelector import UncertaintySampleSelector
from QueryByPartialDataCommiteeSampleSelector import QueryByPartialDataCommiteeSampleSelector
from TargetAndSourceQBCSampleSelector import TargetAndSourceQBCSampleSelector

import ActiveLearner

import collections
from sklearn.svm import LinearSVC

class ActiveLearnerTester:
    dataType = collections.namedtuple('data', ['X', 'Y'])
    domainType = collections.namedtuple('domain', ['name', 'train', 'test'])
    resultsType = collections.namedtuple('result', ['name', 'correct', 'incorrect', 'TP', 'FP', 'TN', 'FN', 'precision', 'recall', 'accuracy'])

def testResultantClassifier(name, classifier, testSet):
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    correct = 0
    wrong = 0
    
    for i in range(testSet.Y.shape[0]):
        prediction = classifier.predict(testSet.X[i])
        if prediction == testSet.Y[i]:
            correct += 1
            if prediction == 1:
                TP += 1
            else:
                TN += 1
        else:
            wrong += 1
            if prediction == 1:
                FP += 1
            else:
                FN += 1
    
    print("TP: {0} FP: {1} TN: {2} FN: {3}".format(TP, FP, TN, FN))
    precision = TP / (TP + FP) #out of all the examples the classifier labeled as positive, what fraction were correct?
    recall = TP / (TP + FN) #out of all the positive examples there were, what fraction did the classifier pick up?
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    print("precision: {0}  recall: {1}  accuracy: {2}".format(precision, recall, accuracy))
    print("correct: {0}, wrong: {1}".format(correct, wrong))
    thisResult = ActiveLearnerTester.resultsType(name, correct, wrong, TP, FP, TN, FN, precision, recall, accuracy)
    return thisResult

#each domain is a tuple of (name, train, test)
def testActiveLearners(sourceDomain, targetDomain):
    
    sourceTrainSize = sourceDomain.train.Y.shape[0]
    sourceTestSize = sourceDomain.test.Y.shape[0]
    targetTrainSize = targetDomain.train.Y.shape[0]
    targetTestSize = targetDomain.test.Y.shape[0]
    
    print("\n\n\n")
    print("Checking domain adaptation from source domain %s to target domain %s" % (sourceDomain.name, targetDomain.name))
    print("|Source Domain: %s | Total Size: %d | Train Set Size: %d | Test Set Size: %d |" % (sourceDomain.name, sourceTrainSize+sourceTestSize, sourceTrainSize, sourceTestSize ))
    print("|Target Domain: %s | Total Size: %d | Train Set Size: %d | Test Set Size: %d |" % (targetDomain.name, targetTrainSize+targetTestSize, targetTrainSize, targetTestSize ))  
    
    #train classifier on source domain
    print("\n\n\n")
    print("=================================================================================")
    print("(1) Testing Source Classifier: ")
    sourceClassifier = LinearSVC()
    sourceClassifier.fit(sourceDomain.train.X,sourceDomain.train.Y)
    print("Source classifier was trained on %d labeled instances" % sourceDomain.train.Y.shape[0])
    sourceClassRes = testResultantClassifier('source_classifier', sourceClassifier, targetDomain.test)
    print("=================================================================================")
    
    #train classifier on target domain
    print("\n\n\n")
    print("=================================================================================")
    print("(2) Testing Target classifier: ")
    targetClassifier = LinearSVC()
    targetClassifier.fit(targetDomain.train.X,targetDomain.train.Y)
    print("target classifier was trained on %d labeled instances" % targetDomain.train.Y.shape[0])
    targetClassRes = testResultantClassifier('target_classifier', targetClassifier, targetDomain.test)
    print("=================================================================================")
    
    print("\n\n\n")
    print("=================================================================================") 
    print("(3) Testing Active Learning classifier with UNCERTAINTY sample selector: ")    
    selector = UncertaintySampleSelector()
    learner = ActiveLearner.ActiveLearner(selector)
    uncertaintyClassifier = learner.train(sourceClassifier,[sourceDomain.train.X,sourceDomain.train.Y],[targetDomain.train.X,targetDomain.train.Y])
    uncertaintyClassRes = testResultantClassifier('uncertainty_classifier', uncertaintyClassifier, targetDomain.test)
    print("=================================================================================")

    print("\n\n\n")
    print("=================================================================================")   
    print("(4) Testing Active Learning classifier with *Query By Partial Data Commitee* sample selector: ") 
    selector = QueryByPartialDataCommiteeSampleSelector(sourceClassifier)
    learner = ActiveLearner.ActiveLearner(selector)
    partialComClassifier = learner.train(sourceClassifier,[sourceDomain.train.X,sourceDomain.train.Y],[targetDomain.train.X,targetDomain.train.Y])
    partialComClassRes = testResultantClassifier('partial_committee_classifier', partialComClassifier, targetDomain.test)
    print("=================================================================================")

    print("\n\n\n")
    print("=================================================================================") 
    print("(5) Testing Active Learning classifier with *Target & Source QBC* sample selector: ") 
    selector = TargetAndSourceQBCSampleSelector(sourceClassifier)
    learner = ActiveLearner.ActiveLearner(selector)
    targetSourceQBCClassifier = learner.train(sourceClassifier,[sourceDomain.train.X,sourceDomain.train.Y],[targetDomain.train.X,targetDomain.train.Y])
    targetSourceQBCClassRes = testResultantClassifier('partial_committee_classifier', targetSourceQBCClassifier, targetDomain.test)
    print("=================================================================================")
    
    print("Test done")