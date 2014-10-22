# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 18:33:19 2014

@author: Shay
"""

from UncertaintySampleSelector import UncertaintySampleSelector
from QueryByPartialDataCommiteeSampleSelector import QueryByPartialDataCommiteeSampleSelector
from TargetAndSourceQBCSampleSelector import TargetAndSourceQBCSampleSelector
from BlitzerDatasetDomain import BlitzerDatasetDomain

import ActiveLearner
import parseProcessedDataFileForScikit

from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder

sourceDomain = BlitzerDatasetDomain.jewelry
targetDomain = BlitzerDatasetDomain.electronics
print("")
print("")
print("")
print("")
print("Checking domain adaptation from source domain %s to target domain %s" % (sourceDomain.value, targetDomain.value))
print("|Source Domain: %s | Total Size: %d | Train Set Size: %d | Test Set Size: %d |" % (sourceDomain.value, sourceDomain.getNumOfTotalInstanceInDomain(), sourceDomain.getNumOfTrainInstanceInDomain(), sourceDomain.getNumOfTestInstanceInDomain() ))
print("|Target Domain: %s | Total Size: %d | Train Set Size: %d | Test Set Size: %d |" % (targetDomain.value, targetDomain.getNumOfTotalInstanceInDomain(), targetDomain.getNumOfTrainInstanceInDomain(), targetDomain.getNumOfTestInstanceInDomain() ))

#Parsing train and test data for source domain
trainXsource, trainYsource  = parseProcessedDataFileForScikit.parseDataFile(sourceDomain.getTrainFileFullPath())
testXsource, testYsource = parseProcessedDataFileForScikit.parseDataFile(sourceDomain.getTestFileFullPath())
trainSourceSize = len(trainXsource)
vectorizer = DictVectorizer(dtype=float, sparse=True)
encoder = LabelEncoder()

#Parsing train and test data for target domain
trainXtarget, trainYtarget  = parseProcessedDataFileForScikit.parseDataFile(targetDomain.getTrainFileFullPath())
testXtarget, testYtarget = parseProcessedDataFileForScikit.parseDataFile(targetDomain.getTestFileFullPath())
trainTargetSize = len(trainXtarget)
#print(type(trainXtarget))

#vectorize!
print("\nVectorizing train sets of source and target domains.")
vectorized = vectorizer.fit_transform(trainXsource+trainXtarget)
vectorizedLabels = encoder.fit_transform(trainYsource+trainYtarget)
total = trainSourceSize+trainTargetSize
#print(type(vectorized))
#print(type(vectorized[0]))
print("Vectorizer num of features: "+str(vectorized[0].get_shape()[1]))
numOfFeatures = vectorized[0].get_shape()[1]

#for i in range(total):
#    if vectorized[i].get_shape()[1] != numOfFeatures:
#        print("found different: "+str(vectorized[i].get_shape()[1]))

newTrainXsource = vectorized[0:trainSourceSize]
newTrainYsource = vectorizedLabels[0:trainSourceSize]
newTrainXtarget = vectorized[trainSourceSize+1:total]
newTrainYtarget = vectorizedLabels[trainSourceSize+1:total]
#print(newTrainXapparel)

#train classifier on source domain
print("")
print("")
print("")
print("=================================================================================")
print("(1) Testing Source Classifier: ")
sourceClassifier = LinearSVC()
sourceClassifier.fit(newTrainXsource,newTrainYsource)
print("Source classifier was trained on %d labeled instances" % (len(newTrainYsource)))
TP = 0
FP = 0
TN = 0
FN = 0
correct = 0
wrong = 0
newTestX = vectorizer.transform(testXtarget)
classes = encoder.classes_
for i in range(len(testXtarget)):
    prediction = sourceClassifier.predict(newTestX[i])
    if classes[prediction] == testYtarget[i]:
        correct += 1
        if classes[prediction] == 1:
            TP += 1
        else:
            TN += 1
    else:
        wrong += 1
        if classes[prediction] == 1:
            FP += 1
        else:
            FN += 1
print("TP: {0} FP: {1} TN: {2} FN: {3}".format(TP, FP, TN, FN))
precision = TP / (TP + FP) #out of all the examples the classifier labeled as positive, what fraction were correct?
recall = TP / (TP + FN) #out of all the positive examples there were, what fraction did the classifier pick up?
accuracy = (TP + TN) / (TP + TN + FP + FN)
print("precision: {0}  recall: {1}  accuracy: {2}".format(precision, recall, accuracy))
print("correct: {0}, wrong: {1}".format(correct, wrong))
print("=================================================================================")

#train classifier on target domain
print("")
print("")
print("")
print("=================================================================================")
print("(2) Testing Target classifier: ")
targetClassifier = LinearSVC()
targetClassifier.fit(newTrainXtarget,newTrainYtarget)
print("target classifier was trained on {0} labeled instances".format(len(newTrainYtarget)))
TP = 0
FP = 0
TN = 0
FN = 0
correct = 0
wrong = 0
newTestX = vectorizer.transform(testXtarget)
classes = encoder.classes_
for i in range(len(testXtarget)):
    prediction = targetClassifier.predict(newTestX[i])
    if classes[prediction] == testYtarget[i]:
        correct += 1
        if classes[prediction] == 1:
            TP += 1
        else:
            TN += 1
    else:
        wrong += 1
        if classes[prediction] == 1:
            FP += 1
        else:
            FN += 1
print("TP: {0} FP: {1} TN: {2} FN: {3}".format(TP, FP, TN, FN))
precision = TP / (TP + FP) #out of all the examples the classifier labeled as positive, what fraction were correct?
recall = TP / (TP + FN) #out of all the positive examples there were, what fraction did the classifier pick up?
accuracy = (TP + TN) / (TP + TN + FP + FN)
print("precision: {0}  recall: {1}  accuracy: {2}".format(precision, recall, accuracy))
print("correct: {0}, wrong: {1}".format(correct, wrong))
print("=================================================================================")


print("")
print("")
print("")
print("=================================================================================") 
print("(3) Testing Active Learning classifier with UNCERTAINTY sample selector: ")    
selector = UncertaintySampleSelector()
learner = ActiveLearner.ActiveLearner(selector)
resultClassifier = learner.train(sourceClassifier,[newTrainXsource,newTrainYsource],[newTrainXtarget,newTrainYtarget])
TP = 0
FP = 0
TN = 0
FN = 0
correct = 0
wrong = 0
newTestX = vectorizer.transform(testXtarget)
classes = encoder.classes_
for i in range(len(testXtarget)):
    prediction = resultClassifier.predict(newTestX[i])
    if classes[prediction] == testYtarget[i]:
        correct += 1
        if classes[prediction] == 1:
            TP += 1
        else:
            TN += 1
    else:
        wrong += 1
        if classes[prediction] == 1:
            FP += 1
        else:
            FN += 1
print("TP: {0} FP: {1} TN: {2} FN: {3}".format(TP, FP, TN, FN))
precision = TP / (TP + FP) #out of all the examples the classifier labeled as positive, what fraction were correct?
recall = TP / (TP + FN) #out of all the positive examples there were, what fraction did the classifier pick up?
accuracy = (TP + TN) / (TP + TN + FP + FN)
print("precision: {0}  recall: {1}  accuracy: {2}".format(precision, recall, accuracy))
print("correct: {0}, wrong: {1}".format(correct, wrong))
print("=================================================================================")


print("")
print("")
print("")
print("=================================================================================")   
print("(4) Testing Active Learning classifier with *Query By Partial Data Commitee* sample selector: ") 
selector = QueryByPartialDataCommiteeSampleSelector(sourceClassifier)
learner = ActiveLearner.ActiveLearner(selector)
resultClassifier = learner.train(sourceClassifier,[newTrainXsource,newTrainYsource],[newTrainXtarget,newTrainYtarget])   
TP = 0
FP = 0
TN = 0
FN = 0
correct = 0
wrong = 0
newTestX = vectorizer.transform(testXtarget)
classes = encoder.classes_
for i in range(len(testXtarget)):
    prediction = resultClassifier.predict(newTestX[i])
    if classes[prediction] == testYtarget[i]:
        correct += 1
        if classes[prediction] == 1:
            TP += 1
        else:
            TN += 1
    else:
        wrong += 1
        if classes[prediction] == 1:
            FP += 1
        else:
            FN += 1
print("TP: {0} FP: {1} TN: {2} FN: {3}".format(TP, FP, TN, FN))
precision = TP / (TP + FP) #out of all the examples the classifier labeled as positive, what fraction were correct?
recall = TP / (TP + FN) #out of all the positive examples there were, what fraction did the classifier pick up?
accuracy = (TP + TN) / (TP + TN + FP + FN)
print("precision: {0}  recall: {1}  accuracy: {2}".format(precision, recall, accuracy))
print("correct: {0}, wrong: {1}".format(correct, wrong))
print("=================================================================================")

print("")
print("")
print("")
print("=================================================================================") 
print("(5) Testing Active Learning classifier with *Target & Source QBC* sample selector: ") 
selector = TargetAndSourceQBCSampleSelector(sourceClassifier)
learner = ActiveLearner.ActiveLearner(selector)
resultClassifier = learner.train(sourceClassifier,[newTrainXsource,newTrainYsource],[newTrainXtarget,newTrainYtarget]) 
TP = 0
FP = 0
TN = 0
FN = 0
correct = 0
wrong = 0
newTestX = vectorizer.transform(testXtarget)
classes = encoder.classes_
for i in range(len(testXtarget)):
    prediction = resultClassifier.predict(newTestX[i])
    if classes[prediction] == testYtarget[i]:
        correct += 1
        if classes[prediction] == 1:
            TP += 1
        else:
            TN += 1
    else:
        wrong += 1
        if classes[prediction] == 1:
            FP += 1
        else:
            FN += 1
print("TP: {0} FP: {1} TN: {2} FN: {3}".format(TP, FP, TN, FN))
precision = TP / (TP + FP) #out of all the examples the classifier labeled as positive, what fraction were correct?
recall = TP / (TP + FN) #out of all the positive examples there were, what fraction did the classifier pick up?
accuracy = (TP + TN) / (TP + TN + FP + FN)
print("precision: {0}  recall: {1}  accuracy: {2}".format(precision, recall, accuracy))
print("correct: {0}, wrong: {1}".format(correct, wrong))
print("=================================================================================")


print("Test done")