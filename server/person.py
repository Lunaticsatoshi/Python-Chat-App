class Person:
    """
    Represents a person 
    holds name, socket client and address
    """

    def __init__(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        """
        Sets the Person
        """
        self.name = name

    def __repr__(self):
        return f"Person({self.addr}, {self.name})"