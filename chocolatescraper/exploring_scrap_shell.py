# IPython log file

# We can use scrapy shell to test our data selection process on the webpapge

# Fetching the main product page of our website "https://www.chocolate.co.uk/collections/all"
fetch("https://www.chocolate.co.uk/collections/all")

# Checking successful retrieval of the webpage
response
#[Out]# <200 https://www.chocolate.co.uk/collections/all>

# Selecting products from the webpage based on a CSS selector
response.css("product-item")
#[Out]# [<Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>,
#[Out]#  <Selector query='descendant-or-self::product-item' data='<product-item class="product-item " r...'>]

# To get the HTML of the first product from the selection made above:
response.css("product-item").get()
#[Out]# '<product-item class="product-item product-item--sold-out" reveal><div class="product-item__image-wrapper "><div class="product-item__label-list label-list"><span class="label label--subdued">Sold out</span></div><a href="/products/2-5kg-bulk-of-our-41-milk-hot-chocolate-drops" class="product-item__aspect-ratio aspect-ratio aspect-ratio--square" style="padding-bottom: 107.33944954128441%; --aspect-ratio: 0.9316239316239316">\n      <img class="product-item__primary-image" loading="lazy" data-media-id="6054417104939" sizes="(max-width: 740px) calc(50vw - 24px), calc((min(100vw - 80px, 1520px) - 305px) / 4 - 18px)" height="702" width="654" alt="2.5kg Bulk 41% Milk Hot Chocolate Drops" src="//www.chocolate.co.uk/cdn/shop/products/hotchoc_654x.jpg?v=1597917174" srcset="//www.chocolate.co.uk/cdn/shop/products/hotchoc_200x.jpg?v=1597917174 200w, //www.chocolate.co.uk/cdn/shop/products/hotchoc_300x.jpg?v=1597917174 300w, //www.chocolate.co.uk/cdn/shop/products/hotchoc_400x.jpg?v=1597917174 400w, //www.chocolate.co.uk/cdn/shop/products/hotchoc_500x.jpg?v=1597917174 500w, //www.chocolate.co.uk/cdn/shop/products/hotchoc_600x.jpg?v=1597917174 600w, //www.chocolate.co.uk/cdn/shop/products/hotchoc_654x.jpg?v=1597917174 654w"></a></div>\n\n  <div class="product-item__info  ">\n    <div class="product-item-meta"><a href="/products/2-5kg-bulk-of-our-41-milk-hot-chocolate-drops" class="product-item-meta__title">2.5kg Bulk 41% Milk Hot Chocolate Drops</a>\n\n      <div class="product-item-meta__price-list-container">\n        <div class="price-list price-list--centered"><span class="price">\n              <span class="visually-hidden">Sale price</span>£45.00</span></div>\n      </div></div></div>\n</product-item>'

# storing all the products' DOM nodes selected using the CSS selector to a variable
products = response.css("product-item")

# The products variable is now a list of all the products on the page
len(products)
#[Out]# 24

# We'll use css to extract the price, url and name of a single product and later with it extract details of all the products using a loop
product = products[0] # product will contain a single product
product
#[Out]# <Selector query='descendant-or-self::product-item' data='<product-item class="product-item pro...'>

# Extracting the product name
product.css("a.product-item-meta__title::text").get()
#[Out]# '2.5kg Bulk 41% Milk Hot Chocolate Drops'

# Extracting the product price
product.css("span.price").get()
#[Out]# '<span class="price">\n              <span class="visually-hidden">Sale price</span>£45.00</span>'

# Getting rid of the extra html and extracting the price
product.css("span.price").get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>£', "").replace("</span>", "")
#[Out]# '45.00'

# Extracting teh product URL
product.css("div.product-item-meta a").attrib["href"]
#[Out]# '/products/2-5kg-bulk-of-our-41-milk-hot-chocolate-drops'

# Now we can use these selectors found in our spider
quit()

# Now that we've scraped the first page we'll navigate to the next page if it exists and scrape it recursively
fetch("https://www.chocolate.co.uk/collections/all")
response.css('[rel="next"]::attr(href)').get()
#[Out]# '/collections/all?page=2'
# We update our spider to navigagte to the next page, the link to which it can find using the selector above
quit()
