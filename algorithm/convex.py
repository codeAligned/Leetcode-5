# coding =utf-8
import numpy as np
import matplotlib.pylab as plt
import random
import math
import time
from matplotlib import pyplot as plt

class Stack(object):
    def __init__(self):
        self.stack = []
    
    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        if self.stack == []:
            raise IndexError('pop from empty stack')
        else:
            del self.stack[-1]
    
    def top(self):
        return self.stack[-1]
    
    def peek(self):
        return self.stack[-1]
    
    def size(self):
        return self.stack.__len__()
    
    def isEmpty(self):
        return True if self.stack == [] else False
    
    def nextTotop(self):
        return self.stack[-2]


class Point(object):
    """docstring for point"""
    
    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = x
        self.y = y
        self.polar = 0
        
    def set_polar(self, polar):
        self.polar = polar

class line(object):
    def __init__(self, start=object, end=object):
        super(line, self).__init__()
        self.start = start
        self.end = end

class Convex(object):
    """docstring for ClassName"""
    
    def __init__(self):
        super(Convex, self).__init__()
    
    def get_points(self, n=int):
        points = []
        for i in range(0, n):
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            p = Point(x, y)
            points.append(p)
        return points
    
    @staticmethod
    def same_side(start_point, end_point, candidate_points):
        '''
        :param start_point:
        :param end_point:
        :param candidatePoint:
        :return: bool if candidatePoints in same side.
        '''
        np.seterr(invalid='ignore')
        
        op = ['null' for i in range(0, len(candidate_points))]
        matrix = np.matrix([[start_point.x, start_point.y, 1],
                            [end_point.x, end_point.y, 1],
                            [candidate_points[0].x, candidate_points[0].y, 1]])
        op[0] = '+' if np.linalg.det(matrix) > 0 else '-'
        
        
        for i in range(1, len(candidate_points) ):
            matrix = np.matrix([[start_point.x, start_point.y, 1],
                                [end_point.x, end_point.y, 1],
                                [candidate_points[i].x, candidate_points[i].y, 1]])
            if np.linalg.det(matrix) > 0:
                op[i] = '+'
            
            else:
                op[i] = '-'
                
            if op[i - 1] == op[i]:
                continue
            else:
                return False

        return True
    
    def get_polar(self, point_base, point_select):
        if point_base.x == point_select.x and point_select.y == point_select.y:
            return 0
        else:
            return math.atan2(point_select.y - point_base.y, point_select.x - point_base.x)

    def cross(self, top, next_top, p3):
        vx, vy = (top.x - next_top.x, top.y - next_top.y)
        wx, wy = (p3.x - next_top.x, p3.y - next_top.y)
        return (vx * wy - vy * wx)
        
    def force(self, points):
        ans = []
        boundpoint = set([])
        points_set = set(points)
        for i in range(0, len(points)):
            for j in range(i, len(points)):
                if i == j: continue
                line_point = set([points[i], points[j]])
                candidate = list(points_set - line_point)
                if self.same_side(points[i], points[j], candidate):
                    boundline = line(points[i], points[j])
                    ans.append(boundline)
                    boundpoint.add(points[i])
                    boundpoint.add(points[j])
                    pass
        return boundpoint, ans

    def graham(self, points):
        points.sort(key=lambda point: point.y)
        point_base = points[0]
        origin_point = Point(0, 0)
        for item in points:
            polar = self.get_polar(point_base, item)
            item.set_polar(polar)
        
        points.sort(key=lambda point: point.polar)
        stack = Stack()
        stack.push(points[0])
        stack.push(points[1])
        stack.push(points[2])
        
        for i in range(3, len(points)):
            point = points[i]
            while self.cross(stack.top(), stack.nextTotop(), point) < 0:
                stack.pop()
            stack.push(point)

        for i in range(1, len(stack.stack)):
            plt.plot([stack.stack[i-1].x, stack.stack[i].x], [stack.stack[i-1].y, stack.stack[i].y], "--")
               
        return stack
    
    def divideConquer(self, points):
        points.sort(key=lambda point: point.x)
        middle = int(len(points)/2)
        left = points[:middle]
        right = points[middle:]
        CHQ_L = self.graham(left)
        CHQ_R = self.graham(right)
        
        for i in range(0, len(CHQ_R.stack) -1):
            if CHQ_R.stack[i].y > CHQ_R.stack[i+1].y:
                high = i
                break
        sq2 = CHQ_R.stack[:high]
        sq1 = CHQ_R.stack[high:]
        merge = sq1 + sq2 + CHQ_L.stack
        CHQ = self.graham(merge)
        return CHQ

class Main(object):
    """docstring for main"""
    def __init__(self):
        super(Main, self).__init__()
        self.main()

    def test_time(self, number):
        convex = Convex()
        points = convex.get_points(number)
        
        force_time_srart = time.time()
        force, ans = convex.force(points)
        force_time_end = time.time()

        graham_time_start = time.time()
        stack = convex.graham(points)
        graham_time_end = time.time()

        dc_time_start = time.time()
        hcq = convex.divideConquer(points)
        dc_time_end = time.time()
        
        t1 = force_time_end - force_time_srart
        t2 = graham_time_end - graham_time_start
        t3 = dc_time_end - dc_time_start
        
        plt.title('Convex Hull')
        plt.subplot(221)
        plt.title('{} samples running time'.format(str(len(points))), fontsize=10)
        plt.ylabel(u'Time cost/s')
        rects = plt.bar([1, 2, 3],list([t1, t2, t3]), width=0.35, facecolor = 'lightskyblue',edgecolor = 'white', align="center", alpha=0.8)
        plt.xticks(np.array([1,2,3]) , ('Force', 'Graham scan', 'DC'), fontsize=8)
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2., 1.03 * height, '%.2f' % float(height), fontsize=4)

        #plt.xticks(x, xticks1, size='small', rotation=30)
        plt.subplot(222)
        plt.title('Force', fontsize=10)
        plt.scatter([item.x for item in points], [item.y for item in points],  marker='x', s=0.5)
        for item in ans:
            plt.plot([item.start.x, item.end.x], [item.start.y, item.end.y], linewidth=2)
        plt.subplot(223)
        plt.title('Graham Scan', fontsize=10)
        plt.scatter([item.x for item in points], [item.y for item in points], marker='x', s=0.5)
        plt.plot([stack.stack[0].x, stack.stack[-1].x], [stack.stack[0].y, stack.stack[-1].y])
        for i in range(1, len(stack.stack)):
            plt.plot([stack.stack[i - 1].x, stack.stack[i].x], [stack.stack[i - 1].y, stack.stack[i].y], linewidth=2)
        plt.subplot(224)
        plt.title('Divide and Conquer', fontsize=10)
        plt.scatter([item.x for item in points], [item.y for item in points], marker='x', s=0.5)
        plt.plot([hcq.stack[0].x, hcq.stack[-1].x], [hcq.stack[0].y, hcq.stack[-1].y])
        for i in range(1, len(stack.stack)):
            plt.plot([hcq.stack[i - 1].x, hcq.stack[i].x], [hcq.stack[i - 1].y, hcq.stack[i].y], linewidth=2)
        plt.savefig('{}-samples.png'.format(len(points)), dpi=1000)
        #plt.show()

        return force_time_end - force_time_srart, graham_time_end - \
            graham_time_start, dc_time_end - dc_time_start, points

    def main(self):
        t1, t2, t3, points = self.test_time(4000)
        pass
    
if __name__ == '__main__':
    main = Main()