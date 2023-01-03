from .cart import Cart


def cart(request):
    
    """ the cart object will send to all templates with the help of processors """
    
    return {"cart": Cart(request)}
