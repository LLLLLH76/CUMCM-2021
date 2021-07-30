import random
import numpy as np
from sympy import *
from sympy.geometry import *

def translate2tangent(e, l):
    '''
    将直线 l 平移至与椭圆 e 大致相切
    '''
    o = Point(0,0)                      # 原点
    l_vertical = Line(o, slope = -1/l.slope)    # l 的过原点的垂线
    p0 = e.intersection(l_vertical)[0]          # 垂线与椭圆的一个交点
    lower_bound = p0.distance(o).evalf()        # 切点必然在垂线交点"外部", 因此以交点与原点距离为下界
    upper_bound = np.inf
    l_vertical = Segment(3*p0, -3*p0)
    while true:
        p = l_vertical.random_point()       # 垂线上任一点
        print(lower_bound, upper_bound)
        if p.distance(o) < lower_bound or p.distance(o) > upper_bound:
            print(p.distance(o).evalf())
            continue
        l_parallel = Line(p, slope = l.slope)
        intersection_list = e.intersection(l_parallel) # 会卡死
        if len(intersection_list) == 1:   # 刚好相切, 不可能
            return l_parallel
        elif len(intersection_list) == 0: # 相离, 缩小线段
            upper_bound = p.distance(o)
            l_vertical = Segment(p, -p)
        elif len(intersection_list) == 2: # 相交, 提高下界
            if intersection_list[0].distance(intersection_list[1]) < 1e-5: # 虽然相交, 但两交点非常接近, 近似为相切
                return l_parallel
            else:
                lower_bound = p.distance(o)
        p = l_vertical.random_point()

if __name__ == "__main__":
    o = Point(0,0)              # 原点
    A = random.randint(1,10)    # 长轴
    B = random.randint(1,10)    # 短轴
    e = Ellipse(o, A, B)        # 创建椭圆
    print(e.area.evalf())       # 椭圆面积
    p1 = e.random_point()       # 随机找一个椭圆上的点p1
    l1 = e.tangent_lines(p1)[0] # 椭圆在p1的切线l1
    a = 2 * l1.distance(o)      # 六边形一组对边距离, 即a
    l2_parallel = l1.rotate( 2 * np.pi / 3) # l1旋转 120度得到六边形邻边l2的平行边
    l3_parallel = l1.rotate(-2 * np.pi / 3)  # l1旋转-120度得到六边形邻边l3的平行边
    l2 =  translate2tangent(e, l2_parallel) # 将l2平行边平移至切线处, 即l2
    l3 =  translate2tangent(e, l3_parallel) # 将l3平行边平移至切线处, 即l3
    b = 2 * l2.distance(o)
    c = 2 * l3.distance(o)
    result = (np.pi *  max([a,b,c]) * min([a,b,c]) / 4).evalf()
    print(result)
