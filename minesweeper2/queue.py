

# class queue:
#   lista,
#   inserir no inicio da lista ->> final da fila
#   tirar do final da lista ->> inicio da fila
class Queue:
    def __init__(self):
        self.items = []
    
    # retorna true if queue is empty
    def empty(self):
        return self.items == []
    
    # inserir no inicio
    def push(self, item):
        self.items.insert(0, item)
    
    # tirar ultimo elemento (inicio da fila)
    def pop(self):
        self.items.pop()

    # retorna primeiro elemento da fila
    def front(self):
        return self.items[-1]
        
def main():
    q = Queue()
    q.push(1)
    q.push(2)
    q.pop()
    print(q.front())
    q.pop()
    print(q.empty())
    q.push(5)
    print(q.front())

if(__name__ == "__main__"): main()