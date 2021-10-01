from django.db import models
from django.utils import timezone
from .reuse import ShippingAddress, Communication, BankAccount, PurchaseData


class Dashboard(models.Model):
    """Model of the dashboard.
    
    """
    pass


class Company(models.Model):
    """Model of the company.

    Attributes
    ----------
    name : str
        Name of the company.
    owner : str
        Owner of the company.
    gstin : str
        GSTIN number of the company.
    phone : str
        Contact number.
    address : str
        Postal address.
    email : str
        E-mail address of the contact person.
    location : str
        City of the company.
    image : ImageField
        Photo/logo of the company.
    shippingaddress : ShippingAddress
        Primary key of the ``ShippingAddress`` instance associated with the company.

    Returns
    -------
    str
        String representation of the company name.
    """
    name = models.CharField(null=True,max_length=100)
    owner = models.CharField(null=True,max_length=100)
    gstin = models.CharField(default=None,null=True, max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.CharField(null=True, blank=True,max_length=100)
    location = models.CharField(null=True, blank=True,max_length=100)
    image = models.ImageField(blank=True,upload_to='images/') 
    shippingaddress = models.OneToOneField(ShippingAddress,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    """Model of the vendor.

    Attributes
    ----------
    name : str
        Name of the vendor.
    identifier : str
        Unique identifier of the vendor.
    gstin : str
        GSTIN number of the vendor.
    address : ShippingAddress
        Primary key of the ``ShippingAddress`` instance associated with the vendor.
    communication : Communication
        Primary key of the ``Communication`` instance associated with the vendor.
    backaccount : BankAccount
        Primary key of the ``BankAccount`` instance associated with the vendor.
    purchasedata : PurchaseData
        Primary key of the ``PurchaseData`` instance associated with the vendor.

    Returns
    -------
    str
        String representation of the vendor name.
    """
    name = models.CharField(max_length=100)
    identifier = models.CharField(null=True, blank=True,max_length=100)
    gstin = models.CharField(default=None, null=True, max_length=100)
    address = models.OneToOneField(ShippingAddress, on_delete=models.PROTECT, null=True)
    communication = models.OneToOneField(Communication, on_delete=models.PROTECT, null=True)
    bankaccount = models.OneToOneField(BankAccount, on_delete=models.PROTECT, null=True)
    purchasedata = models.OneToOneField(PurchaseData, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name
    

class Consumer(models.Model):
    """Model of the consumer.

    Attributes
    ----------
    name : str
        Name of the consumer.
    identifier : str
        Unique identifier of the consumer.
    gstin : str
        GSTIN number of the consumer.
    phone : str
        Contact number.
    address : str
        Address of the consumer.
    email : str
        E-mail address of the consumer.
    location : str
        City of the consumer.

    Returns
    -------
    [type]
        [description]
    """
    name = models.CharField(max_length=100)
    identifier = models.CharField(null=True, blank=True,max_length=100)
    gstin = models.CharField(default=None, null=True, max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.CharField(null=True, blank=True,max_length=100)
    location = models.CharField(null=True, blank=True,max_length=100)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    """Model of the purchase order.

    Attributes
    ----------
    vendor : Vendor
        Vendor associated with the purchase order.
    date : DateField
        Date and time of the purchase order creation.
    po : int
        Purchase order number.
    discount : float
        Percentage discount.
    tax : float
        Percentage of tax applicable for the purchase.
    paid : float
        Amount paid against the PO.
    balance : float
        Amount balance which remains to be paid.
    subtotal : float
        Total of all the product purchase entries associated with the purchase order.
    taxtotal : float
        Total tax applicable on the `subtotal`.
    ordertotal : float
        Total price of the purchase order including  `taxtotal`.

    Methods
    -------
    is_complete()
        Returns the completion status (boolean).
    pending_ppes()
        Returns list of product purchase entries which are not completed.
    """
    # Vendor details
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    # Order details
    date = models.DateTimeField(default=timezone.now().strftime("%d %B, %Y"),null=True, blank=True)
    po = models.IntegerField()
    # Pricing information
    discount = models.FloatField(default=0,null=True)
    tax = models.FloatField(default=0,null=True)
    paid = models.FloatField(default=0,null=True)
    balance = models.FloatField(default=0,null=True)
    subtotal = models.FloatField(default=0,null=True)
    taxtotal = models.FloatField(default=0,null=True)
    ordertotal = models.FloatField(default=0,null=True)
    
    def is_complete(self):
        completionStatus = True
        for ppe in self.productpurchaseentry_set.all():
            if ppe.is_complete() == False:
                completionStatus = False
                break
        return completionStatus
    
    def pending_ppes(self):
        ppes = []
        for ppe in self.productpurchaseentry_set.all():
            if ppe.is_complete() == False:
                ppes.append(ppe)
        return ppes
        

class GoodsReceiptNote(models.Model):
    """Model of the goods receipt note (GRN).

    Attributes
    ----------
    vendor : ModelChoiceField
        Vendor associated with the goods receipt note.
    poRef : MultipleChoiceField
        List of identifiers of the purchase orders from which the goods receipt note is derived.
    identifier : str
        Unique identifier of the goods receipt note.
    date : DateField
        Date of GRN creation.
    grnType : ChoiceField
        Type of GRN (``auto`` or ``manual``).
    amendNumber : int
        Amendment number of the GRN.
    amendDate : DateField
        Amendment date.
    transporter : str
        Name of the transport/shipping service.
    vehicleNumber : str
        Vehicle number using which the products are shipped.
    gateInwardNumber : str
        Gate inward number of the vehicle.
    preparedBy : str
        Name/identifier of the person who created the goods receipt note.
    checkedBy : str
        Name/identifier of the person who validated the goods receipt note.
    checkedBy : str
        Name/identifier of the person who inspected the physical products in the goods receipt note.
    approvedBy : str
        Name/identifier of the authority who approved the goods receipt note.
    """
    TYPE_CHOICES = [
        ('manual', 'Blank'),
        ('auto', 'PO Reference')
    ]
    # Vendor details
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    poRef = models.ManyToManyField(PurchaseOrder)
    # GRN details
    identifier = models.IntegerField()
    date = models.DateTimeField(default=timezone.now,null=True, blank=True)
    grnType = models.CharField(default='manual', max_length=10, null=True,
                               choices=TYPE_CHOICES)
    # Amendments
    amendNumber = models.IntegerField(default=0, null=True, blank=True)
    amendDate = models.DateTimeField(default=timezone.now, null=True, blank=True)
    # Transport
    transporter = models.TextField(default=None, null=True, blank=False)
    vehicleNumber = models.TextField(default=None,null=True, blank=False)
    gateInwardNumber = models.TextField(default=None, null=True, blank=True)
    # Validation and Approval authorities
    preparedBy = models.CharField(default=None, max_length=50, null=True, blank=True)
    checkedBy = models.CharField(default=None, max_length=50, null=True, blank=True)
    inspectedBy = models.CharField(default=None, max_length=50, null=True, blank=True)
    approvedBy = models.CharField(default=None, max_length=50, null=True, blank=True)
    
    
class SalesOrder(models.Model):
    """Model of the sales order.

    Attributes
    ----------
    consumer : ModelChoiceField
        Consumer associated with the sales order.
    date : DateField
        Date of the sales order creation.
    so : int
        Sales order number.
    discount : float
        Percentage discount associated with the sales order.
    tax : float
        Percentage of tax applicable.
    paid : float
        Amount received from the consumer.
    balance : float
        Amount balance with the consumer.
    subtotal : float
        Total of all the product sales entries associated with the sales order.
    taxtotal : float
        Total tax applicable on the `subtotal`.
    ordertotal : float
        Total price of the sales order including  `taxtotal`.
    """
    # Vendor details
    consumer = models.ForeignKey(Consumer,on_delete=models.CASCADE)
    # Order details
    date = models.DateTimeField(default=timezone.now,null=True, blank=True)
    so = models.IntegerField()
    # Pricing information
    discount = models.FloatField(default=0,null=True)
    tax = models.FloatField(default=0,null=True)
    paid = models.FloatField(default=0,null=True)
    balance = models.FloatField(default=0,null=True)
    subtotal = models.FloatField(default=0,null=True)
    taxtotal = models.FloatField(default=0,null=True)
    ordertotal = models.FloatField(default=0,null=True)


class Product(models.Model):
    """Model of the product.

    Attributes
    ----------
    name : str
        Name of the product.
    category : str
        Product category.
    item_type : str
        Type of the product.
    description : str
        Short description of the product.
    price : float
        Price of the product.
    quantity : int
        Stock quantity of the product.
    identifier : str
        Unique identifier of the product.
    location : str
        Physical location of the product.
    length : str
        Length of the product.
    width : str
        Width of the product.
    height : str
        Height of the product.
    weight : str
        Weight of the product.
    discount : float
        Default discount percentage on the product.
    barcode : str
        Barcode of the product.
    expiry : DateField
        Expiry date of the product.
    image : ImageField
        Image of the product.
    """
    # Basic Information
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    # Pricing
    price = models.FloatField(null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True)
    identifier = models.CharField(max_length=30,blank=False, null=True)
    location = models.CharField(max_length=100,blank=False, null=True)
    # Dimensions
    length = models.FloatField(null=True,blank=True)
    width = models.FloatField(null=True,blank=True)
    height = models.FloatField(null=True,blank=True)
    weight = models.FloatField(null=True,blank=True)
    discount = models.IntegerField(default=0)
    barcode = models.CharField(max_length=100,null=True,blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(blank=True,upload_to='images/') 

    def __str__(self):
        return self.name


class ProductPurchaseEntry(models.Model):
    """Model of the product purchase entry.
    
    Attributes
    ----------
    product : ModelChoiceField
        Product associated wit the product purchase entry.
    quantity : int
        Quantity of the product to be ordered.
    price : float
        Price of the product.
    discount : float
        Percentage discount on the product purchase.
    order : PurchaseOrder
        Referenced purchase order.
    receivedQty : str
        Quantity of product received against the ordered quantity.
    acceptedQty : str
        Quantity of product accepted as OK.
    rejectedQty : str
        Quantity of product rejected (not OK, on HOLD, extra delivery, etc.)
    
    Methods
    -------
    is_complete()
        Returns the completion status (boolean).
    pending_quantity()
        Returns the pending quantity against the entry (int).
    """
    # identifier = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    # subtotal = models.FloatField()
    order = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE)
    receivedQty = models.IntegerField(default=0, null=True, blank=True)
    acceptedQty = models.IntegerField(default=0, null=True, blank=True)
    rejectedQty = models.IntegerField(default=0, null=True, blank=True)
    
    def is_complete(self):
        totalAcceptedQty = 0
        for grnentry in self.grnentry_set.all():
            totalAcceptedQty += grnentry.acceptedQty
        completionStatus = False
        if totalAcceptedQty == self.quantity:
            completionStatus = True
        return completionStatus
    
    @property
    def pending_quantity(self):
        totalAcceptedQty = 0
        for grnentry in self.grnentry_set.all():
            totalAcceptedQty += grnentry.acceptedQty
        return self.quantity - totalAcceptedQty
        

class GRNEntry(models.Model):
    """Model of the goods receipt note entry (GRNE).

    Attributes
    ----------
    product : Product
        Primary key of the ``Product`` instance associated with the goods receipt note entry.
    quantity : int
        Ordered quantity of product with reference to product purchase entry.
    grne : int
        Primary key of the ``GoodsReceiptNote`` instance.
    ppe : int
        Primary key of the ``ProductPurchaseEntry`` instance associated with the GRNE.
    remark : str
        Remarks of the quality engineer or the GRN creator about status of products received.
    receivedQty : str
        Quantity of product received against the ordered quantity.
    acceptedQty : str
        Quantity of product accepted as OK.
    rejectedQty : str
        Quantity of product rejected (not OK, on HOLD, extra delivery, etc.)
    """
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(null=True)
    grn = models.ForeignKey(GoodsReceiptNote,on_delete=models.CASCADE)
    ppes = models.ForeignKey(ProductPurchaseEntry, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.TextField(default=None, null=True, blank=True)
    receivedQty = models.IntegerField(default=0, null=True, blank=True)
    acceptedQty = models.IntegerField(default=0, null=True, blank=True)
    rejectedQty = models.IntegerField(default=0, null=True, blank=True)


class ProductSalesEntry(models.Model):
    """Model of the product sales entry.

    Attributes
    ----------
    product : Product
        Primary key of the ``Product`` associated with the product sales entry.
    quantity : int
        Quantity of the product.
    price : float
        Price of the product.
    discount : float
        Percentage discount on the product.
    order : SalesOrder
        Primary key of the ``SalesOrder`` referenced by the entry.
    """
    # identifier = models.CharField(max_length=100)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    # subtotal = models.FloatField()
    order = models.ForeignKey(SalesOrder,on_delete=models.CASCADE)


class PurchaseInvoice(models.Model):
    """Model for the purchase invoice.

    Attributes
    ----------
    company : Company
        Primary key of the ``Company``.
    po : PurchaseOrder
        Primary key of the ``PurchaseOrder``.
    shippingaddress : ShippingAddress
        Primary key of the ``ShippingAddress``.
    communication : Communication
        Primary key of the ``Communication``.
    """
    company = models.OneToOneField(Company,on_delete=models.SET_NULL,null=True)
    po = models.OneToOneField(PurchaseOrder,on_delete=models.SET_NULL,null=True)
    shippingaddress = models.OneToOneField(ShippingAddress,on_delete=models.SET_NULL,null=True)
    communication = models.OneToOneField(Communication, on_delete=models.SET_NULL, null=True)
    
class GRNInvoice(models.Model):
    """Model for the goods receipt note invoice.

    Attributes
    ----------
    company : Company
        Primary key of the ``Company``.
    grn : GoodsReceiptNote
        Primary key of the ``GoodsReceiptNote``.
    shippingaddress : ShippingAddress
        Primary key of the ``ShippingAddress``.
    communication : Communication
        Primary key of the ``Communication``.
    """
    company = models.OneToOneField(Company,on_delete=models.SET_NULL,null=True)
    grn = models.OneToOneField(GoodsReceiptNote,on_delete=models.SET_NULL,null=True)
    shippingaddress = models.OneToOneField(ShippingAddress,on_delete=models.SET_NULL,null=True)
    communication = models.OneToOneField(Communication, on_delete=models.SET_NULL, null=True)
    
class SalesInvoice(models.Model):
    """Model for the sales order invoice.

    Attributes
    ----------
    company : Company
        Primary key of the ``Company``.
    so : SalesOrder
        Primary key of the ``SalesOrder``.
    shippingaddress : ShippingAddress
        Primary key of the ``ShippingAddress``.
    """
    company = models.OneToOneField(Company,on_delete=models.SET_NULL,null=True)
    so = models.OneToOneField(SalesOrder,on_delete=models.SET_NULL,null=True)
    shippingaddress = models.OneToOneField(ShippingAddress,on_delete=models.SET_NULL,null=True)
