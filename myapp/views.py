from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from myapp.models import Games,Cart,Order
import random 
import razorpay
import uuid

# Create your views here.
def index_pg(request):
    context={}
    allg = Games.objects.all()
    context['Games']=allg
    return render(request,'new_index.html',context)

def filterByType(request,tyname):
    context={}
    c1 = Q(type=tyname)
    c2 = Q(price__gte = 100 )
    allstu = Games.objects.filter(c1 & c2)
    context['Games']=allstu
    return render(request,'new_index.html',context)

def rangeSearch(request):
    context={}
    min = request.GET['min']
    max  = request.GET['max']
    c1 = Q(price__gte = min)
    c2 = Q(price__lte = max)
    allstu = Games.objects.filter(c1 & c2)
    context['Games']=allstu
    return render(request,'new_index.html',context)

def sortGames(request,ord):
    context={}
    if ord == '0':
        col='price'
    else:
        col='-price'
    allstu = Games.objects.all().order_by(col)
    context['Games']=allstu
    return render(request,'new_index.html',context)

def home(request):
     return render(request,"home.html")

def aboutUs(request):
     return render(request,"aboutUs.html")

def contactUs(request):
     return render(request,"contactUs.html")

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        context={}
        n= request.POST['username']
        e= request.POST['useremail']
        p= request.POST['userpassword']
        c= request.POST['confirmpassword']
        if n=='' or p=='':
            context['errorMsg']='Kindly enter all fields'
            return render(request,'register.html',context)
        elif p!=c:
            context['errorMsg']='Password and confirm password must be same'
            return render(request,'register.html',context)
        else:
            u = User.objects.create(username=n,email=e)
            u.set_password(p)#for encrypted password
            u.save()
            context['success']='Registered successfully!!'
            return render(request,'login.html',context)
        
def user_login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        context={}
        u=request.POST['username']
        p=request.POST['userpassword']
        if u=='' or p=='':
            context['errorMsg']='plz provide all details'
            return render(request,'login.html',context)
        else:
            u = authenticate(username=u, password=p)
            if u is not None:
                login(request,u)
                print(request.user.is_authenticated)
                return render(request,'/index')
            else:
                context['errorMsg']='plz provide correct credentials'
                return render(request,'login.html',context)

def user_logout(request):
    logout(request)
    return redirect('/home')

def showDetails(request,gid):
    g = Games.objects.filter(id=gid)
    context={}
    context['Games']=g[0]
    return render(request,'details.html',context)


def addToCart(request,gid):
    userid = request.user.id
    if userid:
        user = User.objects.filter(id=userid)
        g = Games.objects.filter(id=gid)
        c = Cart.objects.create(gid=g[0],uid=user[0])
        c.save()
        #return HttpResponse('cart added!!')
        return redirect('/index')
    else:
        return render(request,'login.html')
    
def viewcart(request):
    userid = request.user.id
    if userid:
        user = User.objects.filter(id=userid)
        mycart = Cart.objects.filter(uid=user[0])
        context={}
        context['cart']=mycart
        count = len(mycart)
        total = 0
        for cart in mycart:
            total += cart.quantity*cart.gid.price
        context['count'] = count
        context['total'] = total
        return render(request,'viewcart.html',context)
    else:
        return render(request,'login.html',context)
    
def deleteFromCart(request,cid):
    cart = Cart.objects.filter(id = cid)
    cart.delete()
    return redirect('/viewcart')

def updateQuantity(request,incr,cid):
    c = Cart.objects.filter(id = cid)
    if incr=='0': #decr qty
        new_qunat = c[0].quantity -1
    else: #incr qty
        new_qunat = c[0].quantity +1
    c.update(quantity = new_qunat)
    return redirect('/viewcart')

def placeOrder(request):
    context={}
    userid = request.user.id
    order_id = random.randrange(1000,9999)
    #fetch current cart
    mycart = Cart.objects.filter(uid = userid)
    #add the cart items to order
    for cart in mycart:
        ord = Order.objects.create(order_id=order_id,gid=cart.gid,uid=cart.uid,quantity=cart.quantity)
        ord.save()
    mycart.delete()#clear cart table for current user
    mycart = Order.objects.filter(order_id=order_id)#fetch order details
    #calculate count and total
    count = len(mycart)
    total = 0
    for cart in mycart:
        total += cart.quantity*cart.gid.price
    context['count']=count
    context['total']= total
    context['mycart']=mycart
    return render(request,'placeorder.html',context)

def generate_unique_token():
    return str(uuid.uuid4())

def makepayment(request):
    #get the orderdetails for current loggedin user
    userid = request.user.id
    ordDetails = Order.objects.filter(uid = userid)
    #calculate the billamount
    bill=0
    for ord in ordDetails:
        bill += ord.gid.price*ord.quantity
        ordId = ord.order_id
    # games = Games.objects.all()
     # generate a unique token for the order
    # token = generate_unique_token()
    # Order.token = token
    # Order.save()
    client = razorpay.Client(auth=("rzp_test_kfOrIsbIsB6pZK", "9frPZO8Q2VPMMrEDJRwDLUHX"))
    data = { "amount": bill*100, "currency": "INR", "receipt": str(ordId) }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    # context = {"data": payment, "token": token, "games": games}
    return render (request,'pay.html',context)

def get_file_path_for_game(game):
    return game.file_path.path

def download_view(request, token,game_id):
    # check if the token is valid
    order = get_object_or_404(Order, token=token)

    # check if the user who made the request is the owner of the order
    if request.user == Order.uid:
        # provide the file for download
        file_path = get_file_path_for_game(Order.gid)
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{order.gid.name}.zip"'
            return response
    else:
        raise Http404("You don't have permission to access this resource.")