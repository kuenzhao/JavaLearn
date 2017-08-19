# -*- coding:utf-8 -*-
from __future__ import print_function

from time import time#计时
import logging#打印进展信
import matplotlib.pyplot as plt#绘图打印，绘图工具

from sklearn.cross_validation import train_test_split#
from sklearn.datasets import fetch_lfw_people#专门用来下载数据集
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import RandomizedPCA
from sklearn.svm import SVC
from blaze.expr.split import _split
print(__doc__)

#display progress logs on stdout
logging.basicConfig(level = logging.INFO,format = '%(asctime)s %(message)s')

#Download the data ,if not already on disk and load it as numpy arrays
lfw_people = fetch_lfw_people(min_faces_per_person = 70,resize = 0.4)

n_samples,h,w = lfw_people.images.shape

#for machine learning we use the a data directly (as relative pixel 
#positions info is ignored by this model)
X = lfw_people.data#提取数据的特征向量的矩阵
n_features = X.shape[1]

#the label to predict is the id of the person
y = lfw_people.target
target_names = lfw_people.target_names
n_classes = target_names.shape[0]

print("Total dataset size:")
print("n_samples: %d" % n_samples)
print("n_features: %d" % n_features)
print("n_classes： %d" % n_classes)



#拆分数据集
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.25)

#
#数据进行将维处理
n_components = 150
print("Extracting the top %d eigenfaces from %d faces"
        %(n_components,X_train.shape[0]))

t0 = time()
pca = RandomizedPCA(n_components=n_components,whiten = True).fit(X_train)
print("done in %0.3fs"%(time()-t0))

eigenfaces = pca.components_.reshape(n_components,h,w)#提取人脸的eigenfaces

print("Projecting the input data on the eigenfaces orthonormal basis")

to = time()
X_train_pca = pca.transform(X_train)#转换为更低维的矩阵
X_test_pca = pca.transform(X_test)
print("done in %0.3fs"%(time() - t0))

#开始进行训练

print("Fitting the classifier to the training set")
t0 = time()

param_grid = {'C':[1e3,5e3,1e4,5e4,1e5],'gamma':[0.0001,0.0005,0.001,0.005,0.01,0.1],}
clf = GridSearchCV(SVC(kernel = 'rbf',class_weight = 'balanced'),param_grid)
clf = clf.fit(X_train_pca,y_train)
print("done in %0.3fs"% (time() - t0))
print("Best estimator found by grid search:")
print(clf.best_estimator_)



print("Predicting people's names on the test set")
t0 = time()
y_pred = clf.predict(X_test_pca)
print("done in %0.3fs"%(time() -t0))

print(classification_report(y_test,y_pred,target_names = target_names))
print(confusion_matrix(y_test,y_pred,labels = range(n_classes)))


def plot_gallery(images,titles,h,w,n_row = 3,n_col = 4):
    """Helper function to plot a gallery of portarits"""
    plt.figure(figsize = (1.8 * n_col,2.4*n_row))
    plt.subplots_adjust(bottom = 0,left = .01,right = .99,top = .90,hspace = .35)
    for i in range(n_row*n_col):
        plt.subplot(n_row,n_col,i +1)
        plt.imshow(images[i].reshape(h,w),cmap = plt.cm.gray)
        plt.title(titles[i],size = 12)
        plt.xticks(())
        plt.yticks(())


def title(y_pred,y_test,target_names,i):
    pred_name = target_names[y_pred[i]].rsplit(' ',1)[-1]
    true_name = target_names[y_test[i]].rsplit(' ',1)[-1]
    return 'predicted: %s\ntrue:    %s'%(pred_name,true_name)

prediction_titles = [title(y_pred,y_test,target_names,i)
                for i in range(y_pred.shape[0])]
plot_gallery(X_test,prediction_titles,h,w)

eigenface_titles = ["eigenface %d"% i for i in range(eigenfaces.shape[0])]
plot_gallery(eigenfaces,eigenface_titles , h, w)
plt.show()




