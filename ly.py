import random
import sys
import time
from datetime import datetime 
sys.setrecursionlimit(100000)
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None
def generate_random_linked_list(n, m):
    head = Node()
    current = head
    for _ in range(n):
        data = random.randint(1, m)
        new_node = Node(data)
        current.next = new_node
        new_node.prev = current
        current = current.next
    return head.next
def count_greater_than_50(head):
    count = 0
    current = head
    while current:
        if current.data > 50:
            count += 1
        current = current.next
    return count
def sort_linked_list(head, increasing_order=True):
    if head is None or head.next is None:
        return head
    
    mid = get_middle(head)
    mid_next = mid.next
    mid_next.prev = None
    mid.next = None
    
    left = sort_linked_list(head, increasing_order)
    right = sort_linked_list(mid_next, increasing_order)
    
    return merge(left, right, increasing_order)
def get_middle(head):
    slow = head
    fast = head
    
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow
def merge(left, right, increasing_order):
    result = None
    
    if left is None:
        return right
    if right is None:
        return left
    
    if increasing_order:
        if left.data <= right.data:
            result = left
            result.next = merge(left.next, right, increasing_order)
        else:
            result = right
            result.next = merge(left, right.next, increasing_order)
    else:
        if left.data >= right.data:
            result = left
            result.next = merge(left.next, right, increasing_order)
        else:
            result = right
            result.next = merge(left, right.next, increasing_order)
    
    result.next.prev = result
    return result
def delete_element(head, index):
    if head is None or index < 0:
        return
    current = head
    for _ in range(index):
        if current is None:
            return
        current = current.next
    if current is None:
        return
    print('deleted element')
    prev_node = current.prev
    next_node = current.next
    if prev_node:
        prev_node.next = next_node
    if next_node:
        next_node.prev = prev_node
def insert_element(head, data):
    new_node = Node(data)
    if head is None:
        return new_node
    
    current = head
    while current.next and current.next.data < new_node.data:
        current = current.next
    
    next_node = current.next
    current.next = new_node
    new_node.prev = current
    new_node.next = next_node
    if next_node:
        next_node.prev = new_node
    
    return head

def insert_to_dsc_order(head, value):
    new_node= Node(value)
    cur = head 
    while cur.data >= value:
        cur=cur.next
    new_node.next =cur 
    new_node.prev =cur.prev 
    prev_ele = cur.prev
    cur.prev = new_node
    prev_ele.next=new_node

def insert_to_asc_order(head,value):
        new_node = Node(value)
        cur =head
        ython
def insert_to_asc_order(linked_list, value):
    new_node = Node(value)
    if linked_list is None:
        linked_list = new_node
        return linked_list
    if linked_list.data > value:
        new_node.next = linked_list
        linked_list.prev = new_node
        linked_list = new_node
        return linked_list
    prev_node = linked_list
    cur_node = linked_list.next
    while cur_node is not None and cur_node.data < value:
        prev_node = cur_node
        cur_node = cur_node.next
    prev_node.next = new_node
    new_node.prev = prev_node
    if cur_node is not None:
        new_node.next = cur_node
        cur_node.prev = new_node

def print_linked_list(head):
    current = head
    while current:
        print(current.data)
        current = current.next
def generate_random_array(n, m):
    return [random.randint(1, m) for _ in range(n)]
def count_greater_than_50_array(arr):
    count = 0
    for num in arr:
        if num > 50:
            count += 1
    return count

# Generate random linked list and perform operations
n = int(input('enter n:'))
m = int(input('enter m:'))
s = int(input('enter s:'))
i=0
while (i<s):
    starttime=datetime.now()
    linked_list = generate_random_linked_list(n, m)
    print("Random Linked List:")
    print_linked_list(linked_list)
    count = count_greater_than_50(linked_list)
    print("Number of elements greater than 50:", count)
    if count > 5:
        linked_list = sort_linked_list(linked_list, True)
        delete_element(linked_list, 4)
        insert_to_asc_order(linked_list,10)
    else:
        linked_list = sort_linked_list(linked_list, False)
        print('after sort')
        print_linked_list(linked_list)

        delete_element(linked_list, 1)
        print('after delete')
        print_linked_list(linked_list)
        insert_to_dsc_order(linked_list, 10)
    linked_list = insert_element(linked_list, 10)
    print("Final Linked List:")
    print_linked_list(linked_list)
    endtime=datetime.now()
    totaltime=endtime-starttime
    print("totaltime=",totaltime.microseconds)
    i=i+1
