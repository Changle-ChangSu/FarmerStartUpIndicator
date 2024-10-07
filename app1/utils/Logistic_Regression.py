# 开发者：苏畅
# 2023/5/11 11:45 于上海财经大学

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


def dummy(data, categorical_var, min, max):
    for i in range(min, max):
        prefix = f'{categorical_var}_{i}'
        data[prefix] = (data[categorical_var] == i).astype(int)

    data = data.drop(categorical_var, axis=1)

    return data


def preProcessing(data):
    # 选定分隔符将列表或元组转换为字符串，将一个特征变量变为计算机能读懂的特征距离
    data = dummy(data, 'famtype', 0, 3)
    data = dummy(data, 'expectation', 1, 5)
    data = dummy(data, 'socistatu', 1, 7)
    data = data.drop(['name', 'tel', 'recptime', 'recpplace'], axis=1)

    if 'remark' in data.columns:
        data = data.drop(['remark'], axis=1)

    return data


def Logistic_Regression():
    # 数据集划分
    data = pd.read_excel('D:\SUFE\Projects\VS\FarmerStartUpIndicator_2\训练集.xlsx')
    data = preProcessing(data)
    X = data.drop(['entrepre'], axis=1)
    y = data['entrepre']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=114514)
    # print(len(X_train), len(X_test))

    # 训练模型
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)
    print(data.head())

    return logreg
