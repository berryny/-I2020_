def hello_world():
    print("hello world")

def goodbye():
    print("goodbye")
    
def func(arg):
    return 100 * arg

if __name__ == "__main__":
    import sys
    print(func(sys.argv[1]))
    print(func(100))