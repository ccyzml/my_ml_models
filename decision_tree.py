'''
基于id3算法的决策树模型

def 创建决策树
    if 所有样本都是一个类别：
        创建叶节点
    elif 没有属性可以划分：
        选择样本标签多的作为节点值（如果label数量一样，随便选择）
    else:
        计算信息增益，选择分裂特征
        根据分裂特征将样本分离
        将已选特征从特征集中删除
        for 每个样本集
            递归生成决策树


'''
import math

def describe_label(dataset):
    return describe(dataset,-1)

def describe(dataset,pos):
    result = {}
    for i in dataset:
        key = str(i[pos])
        if key in result:
            result[key] += 1
        else:
            result[key] = 1
    return result

def describe_feature_label(dataset,pos,feature):
    result = {}
    for i in dataset:
        if i[pos] == feature:
            key = str(i[-1])
            if key in result:
                result[key] += 1
            else:
                result[key] = 1
    return result


def check_feature(dataset):
    if len(dataset[0]) == 1:
        return True
    else:
        return False

def calc_id3(dataset, pos):
    labels= describe_label(dataset)
    sum = 0
    h = 0
    for value in labels.values():
        sum += value
    for value in labels.values():
        p = float(value)/(sum)
        h += -p*math.log(p,2)
    feature_dict = describe(dataset,pos)
    for feature in feature_dict:
        count = feature_dict[feature]
        feature_label_dict = describe_feature_label(dataset,pos,feature)
        h2 = 0
        for value in feature_label_dict.values():
            p = float(value) / count
            h2 += -p * math.log(p,2)
        h -= h2
    return h

def get_best_feature(dataset):
    feature_sum = len(dataset[0])-1
    max_value = 0
    best_feature = 0
    for i in range(0,feature_sum):
        value = calc_id3(dataset, i)
        if value > max_value:
            max_value = value
            best_feature = i
    return best_feature



def divide_dataset(dataset,feature_pos):
    dict = {}
    for i in dataset:
        key = str(i[feature_pos])
        if key in dict:
            dict[key].append(i)
        else:
            dict[key] = [i]
    return dict

'''
{"rich":{"cool":"date","ugly":"home"},"poor":{"cool":"date","ugly":"home"}}
'''
def create_decision_tree(dataset):
    print('开始创建')
    labels = describe_label(dataset)
    print(labels)
    if len(labels) == 1:                 #所有标签都相同
        print("所有标签都相同，构建叶子节点")
        label = list(labels.keys())[0]
        return label
    elif check_feature(dataset): #没有更多特征了，根据label种类哪个多确定叶子节点值
        print("没有更多特征了，根据label服从多数创建节点")
        keys = list(labels.keys())
        label = keys[0]
        for key in keys:
            label = key if labels[key] > labels[label] else label
        return label
    else:
        feature_pos = get_best_feature(dataset)
        print("筛选最优划分特征："+str(feature_pos))
        dataset_dict = divide_dataset(dataset, feature_pos)
        for l in dataset_dict.values():
            for sub_l in l:
                sub_l.pop(feature_pos)   #剔除特征
        dict_tmp = {}
        for key in dataset_dict:
            dict_tmp[key] = create_decision_tree(dataset_dict[key])
        return dict_tmp


'''
训练样本：
 [['rich','ugly','home'],
  ['rich','ugly','date'],
  ['rich','cool','date'],
  ['poor','cool','date'],
  ['poor','ugly','home'],
  ['poor','cool','home']]
'''

sample =  [['rich','ugly','home'],
          ['rich','ugly','date'],
          ['rich','cool','date'],
          ['poor','cool','date'],
          ['poor','ugly','home'],
          ['poor','cool','home']]

print("最优决策树："+str(create_decision_tree(sample)))