class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.head=None
        self.tail=None
        self.size=0
    
    def enqueue(self, x: int) -> None:
        new_node=Node(x)
        if self.tail is None:
            self.head=new_node
            self.tail=new_node
        else:
            self.tail.next=new_node
            self.tail=new_node
        self.size+=1
    
    def dequeue(self):
        if self.head is None:
            self.tail= None
            return "Queue is empty"
        value=self.head.value
        self.head=self.head.next

        self.size-=1
        return value
        
    

q = Queue ()
q.enqueue(1)
q.enqueue(2)
print(q.dequeue())
q.enqueue(3)
print(q.dequeue())
print(q.dequeue())
print(q.dequeue())