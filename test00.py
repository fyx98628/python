'''
import os
def openfile():
    #file = r'C:/Users/Rain Sunny/Desktop/loge.txt'
    with open(r'G:/loge.txt',mode='w',encoding='utf-8') as f:
        f.write('0\n0')

if __name__ == '__main__':
    openfile()
'''


lst = {}
for i in range(0,5):
    lst[i] = int(input())
print(lst)
print(max(lst.values()))