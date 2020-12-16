from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Catalog, Category, Product, Cart
from UserLogin.models import Sponsor, Driver, Employs
from .forms import CreateNewCatalog, CreateNewProduct
from ebaysdk.shopping import Connection as shopping
from bs4 import BeautifulSoup
import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.models import User
import json
from django.core.serializers.json import DjangoJSONEncoder

def sendEmail(send_from, send_to, subject, msg):
    RECIPIENT  = send_to
    send_from="root@ahhtiger.com"
    HOST = "email-smtp.us-west-2.amazonaws.com"
    PORT = 587
    SUBJECT = subject
    BODY_TEXT = msg
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Drivers</h1>
    <p>"""+msg+"""</p>
    </body>
    </html>
                """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr(("Drivers", send_from))
    msg['To'] = RECIPIENT
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')
    msg.attach(part1)
    msg.attach(part2)
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("AKIAZZ2UPLYCPTWWT6O3","BEVcUJXPgZ4s3ZBFumhgCEwuQAi73RIzVt8HsWmfB6DZ")
        server.sendmail(send_to, RECIPIENT, msg.as_string())
        server.close()
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")

# Create your views here.
def index(request, id):
    cat = Catalog.objects.get(id=id)
    form = CreateNewCatalog()
    form2 = CreateNewProduct()
    return render(request, 'catalog/list.html', {'cat':cat, 'form':form, 'form2':form2})

def viewCatalogs(request):
    spon = Sponsor.objects.get(id=request.user.id)
    catalogs = spon.catalog.all()
    form = CreateNewCatalog()
    return render(request, 'catalog/view.html', {'catalogs':catalogs, 'form':form})

def viewCatalogsDriver(request):
    user=request.user
    if Sponsor.objects.filter(id=user.id):
        realSponsor=Sponsor.objects.get(id=user.id)
    elif Driver.objects.filter(id=user.id):
        sponsor=Employs.objects.filter(drivers=request.user.id).values_list('sponsors',flat=True).first()
        realSponsor=Sponsor.objects.get(id=sponsor)
    #catalog=Catalog.objects.filter(sponsor=sponsor)
    cat=realSponsor.catalog.all()[0]
    category=cat.category_set.all()
    jsonOutput=[]
    for c in category:
        products=c.product_set.all()
        for product in products:
            jsonOutput.append({"title":product.name,"price":product.price,"pic":product.productImg,"rating":product.rating,"brand":c.name,"id":product.id})
    return render(request, 'catalog/catalog.html', {'values':json.dumps(jsonOutput,cls=DjangoJSONEncoder)})
    
def createCatalog(request):
    if request.method == "POST":
        form = CreateNewCatalog(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            c = Catalog(name=n, isPrimary=False)
            c.save()
            mySponsor = Sponsor.objects.get(id=request.user.id)
            mySponsor.catalog.add(c)

        return HttpResponseRedirect("/catalog/%i" %c.id)

    form = CreateNewCatalog()
    return render(request, 'catalog/create.html', {'form':form})

def createCategory(request, id):
    if request.method == "POST":
        form = CreateNewCatalog(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            c = Category(name=n, catalog=Catalog.objects.get(id=id))
            c.save()

    return HttpResponseRedirect("/catalog/%i" %c.catalog.id)

def createProduct(request, id):
    if request.method == "POST":
        form = CreateNewProduct(request.POST)
        if form.is_valid():
            link = form.cleaned_data["link"]
            productID = link.split('/')[5].split('?')[0]
            api = shopping(appid='JaySkrob-TrailerP-PRD-0e65090ee-840b0c33', config_file=None)
            api_request = {'ItemID':productID}

            response = api.execute('GetSingleItem', api_request)
            soup = BeautifulSoup(response.content, 'lxml')
            item = soup.find('item')
            title = item.title.string.strip()
            price = item.convertedcurrentprice.string
            pic = item.pictureurl.string
            condition = item.conditiondisplayname.string
            url = item.viewitemurlfornaturalsearch.string.strip()

            p = Product(name=title, price=price, productImg=pic, productid=productID, category=Category.objects.get(id=id), rating=condition, link=url)
            p.save()

    return HttpResponseRedirect("/catalog/%i" %p.category.catalog.id)

def deleteProduct(request, id):
    if request.method == "POST":
        product = Product.objects.get(id=id)
        cat = product.category
        product.delete()

    return HttpResponseRedirect("/catalog/%i" %cat.catalog.id)

def deleteCatalog(request, id):
    if request.method == "POST":
        catalog = Catalog.objects.get(id=id)
        catalog.delete()

    return HttpResponseRedirect("/catalog/view")

def makePrimary(request, id):
    if request.method == "POST":
        catalog = Catalog.objects.get(id=id)
        catalog.isPrimary = True
        catalog.save()

def addToCart(request, id):
    driver = Driver.objects.get(id=request.user.id)
    p = Product.objects.get(id=id)
    cart = Cart(driver=driver, product=p)
    cart.save()
    email=User.objects.get(id=request.user.id).email
    sendEmail("root@ahhtiger.com",email,"Points","You added a product to your cart")
    sponsor=Employs.objects.filter(drivers=request.user.id).values_list('sponsors',flat=True).first()
    sendEmail("root@ahhtiger.com",User.objects.get(id=sponsor).email,"Points","Someone bought from your catalog")
    return render(request, 'catalog/viewCart.html', {'cart':cart})

def removeFromCart(request, id):
    if request.method == "POST":
        driver = Driver.objects.get(id=request.user.id)
        p = Product.objects.get(id=id)
        cart = driver.cart.all()[0]
        cart.product = None
        cart.save()
        return HttpResponseRedirect("/catalog/viewDriver")

def viewCart(request):
    driver = Driver.objects.get(id=request.user.id)
    cart = driver.cart.all()[0]
    return render(request, 'catalog/viewCart.html', {'cart':cart})

def error_404(request, exception):
    return render(request, 'catalog/404.html', status=404)
