class Hello():
    def __init__(self):

        print("YOO")

class H(Hello):

    def __init__(self):
        Hello.__init__(self)
        print("YAAs")


h = H()

