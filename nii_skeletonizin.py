import nibabel as nib
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt                                                                              
from mpl_toolkits.mplot3d import Axes3D
from skimage.morphology import skeletonize_3d

def get_data(fielpath):
    img = nib.load(fielpath)
    #data是一个Numpy数组,这里的三维数组存储的是图像的像素值，也就是说data[x][y][z] = 1表示图像中的(x,y,z)这个点是血管，data[x][y][z] = 0表示图像中的(x,y,z)这个点是背景
    data = img.get_fdata()

    # 获取三维数组中的非零点的坐标
    #这里的coords是一个元组，元组中的每个元素都是一个数组，数组中的元素是非零点的坐标，coords[0]是x坐标，coords[1]是y坐标，coords[2]是z坐标
    coords = np.where(data != 0)
    
    # 使用skeletonize_3d函数进行骨架化
    skeleton = skeletonize_3d(data)

    # 获取骨架的坐标
    coords = np.where(skeleton != 0)


    inter = 3
    selected_coords = (coords[0][::inter], coords[1][::inter], coords[2][::inter])

    return selected_coords

