from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from pylab import *

# Create your views here.
def home(request):
    import requests 
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_3a23ad6ed1d84ad1b10f01c72dc2d07e")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html' , {'api': api })

    else: 
        return render(request, 'home.html' , {'ticker': " Enter a Ticker Symbol in the Search..."})

def about(request):
    return render(request, 'about.html' , {})

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def chart(request):
    #return render(request, 'chart.html' , {})
    import requests 
    import json

    if request.method == 'POST':
        schart = request.POST['schart']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + schart + "/chart/5d?token=pk_3a23ad6ed1d84ad1b10f01c72dc2d07e")
        try:
            api = json.loads(api_request.content)
            print(json.dumps(api, indent=4))
        except Exception as e:
            api = "Error..."
        return render(request, 'chart.html' , {'api': api })

    else: 
        return render(request, 'chart.html' , {'schart': " Enter a Ticker Symbol in the Search..."})
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def add_stock(request):
    import requests 
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added "))
            return redirect('add_stock')
    else: 
        ticker = Stock.objects.all()
        output = []

        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_3a23ad6ed1d84ad1b10f01c72dc2d07e")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stock.html' , {'ticker': ticker, 'output': output})



def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Has Been deleted !"))
    return redirect('delete_stock')

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html' , {'ticker': ticker})

# XXXXXXXXXXXXXXXXXXX
def tickplot(request):
    from django.shortcuts import render
    import matplotlib.pyplot as plt
    import io
    import urllib, base64
    from matplotlib import pylab
    #from pylab import *
    plt.plot(range(10))
    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'tickplot.html',{'data':uri}) 

