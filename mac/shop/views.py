from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
import math
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .Paytm import Checksum


MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'
# Create your views here.


def index(request):
    #product = Product.objects.all()
    #print(product)
    #n = len(product)
    #nSlides = n//4 - math.ceil((n/4)-(n//4))
    #params = {'no of slides':nSlides,'range':range(1,nSlides),'product':product,}
    #allprods = [[product,range(1,nSlides),nSlides],[product,range(1,nSlides),nSlides]]

    #params = {'allprods':allprods}
    allprods = []
    catprod = Product.objects.values('category')
    cats = {item['category'] for item in catprod}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 - math.ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nSlides), nSlides])
    params = {'allprods': allprods}

    return render(request, 'shop/index.html', params)

def searchmatch(query,item):
    #return true if query matches the item
    if query.lower() in item.product_name.lower()  or query in item.desc.lower() or query in item.category.lower():
        return True
    else:
        return False



def search(request):
    query = request.GET.get('search')
    allprods = []
    catprod = Product.objects.values('category')
    cats = {item['category'] for item in catprod}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchmatch(query ,item)]

        n = len(prod)
        nSlides = n // 4 - math.ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allprods.append([prod, range(1, nSlides), nSlides])
    params = {'allprods':allprods,'msg':""}
    if len(allprods) == 0 or len(query)<3:
        params = {'msg':"Please enter a relevant Item."}
    return render(request, 'shop/search.html', params)





def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        query = request.POST.get('query', '')
        contact = Contact(name=name, email=email, phone=phone, query=query)
        contact.save()
        Thanks = True
        return render(request, 'shop/contact.html', {'Thanks': Thanks})

    return render(request, 'shop/contact.html')


def track(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates, "itemsJson":order[0].item_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"no item"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def prodview(request, id):
    #fetching product through id
    product = Product.objects.filter(id=id)
    print(product)
    return render(request, 'shop/prodview.html', {'product': product[0]})


def checkout(request):
    if request.method == 'POST':
        item_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        zip = request.POST.get('zip', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        checkout = Orders(item_json=item_json, name=name, email=email, phone=phone, address=address, zip=zip, city=city, state=state,amount=amount)
        checkout.save()
        update = OrderUpdate(order_id=checkout.order_id, update_desc="The order has been placed.")
        update.save()
        thank = True
        id = checkout.order_id
        #return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        # request paytm to transfer amount to your account after payment is done
        param_dict={

            'MID': 'WorldP64425807474247', # enter your merchant id here
            'ORDER_ID': str(checkout.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request,'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')
@csrf_exempt
def handlerequest(request):

    # paytm will send post request here
    form = request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum= form[i]
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Order Successful')
        else:
            print('Order was not successful' + response_dict['RESPMSG'])

    return render(request,'shop/paymentstatus.html', {'response': response_dict})
