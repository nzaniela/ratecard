# -*- encoding: utf-8 -*-
###############################################################################
#Outlet  --> Outlet                                                             #
###############################################################################
from openerp import models, fields, api
from  ragconstants import  days , seconds , minutes  ,list_position , hour_from , hour_to , page_no ,_ad_column , _ad_inches , outlettype_

class spot_length(models.Model):
    _name = 'spot.length'
    name = fields.Char(string='NAME')
    seconds = fields.Selection(selection=seconds, string='Seconds')
    ratecard_sin_id  = fields.One2many(comodel_name='ratecard.sin', inverse_name='spot_length_id', 
                                      string='Spot Length')
    logo = fields.Binary('Logo File')
    description = fields.Text('Description', translate=True)     
    
    product_ids = fields.One2many(
        'product.template',
        'spot_length_id',
        string='Spot  Length',
    )   
    products_count = fields.Integer(
            string='Number of products',
            compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)    


    
class res_partner(models.Model):
    _inherit = 'res.partner'
    
    vat_no = fields.Integer(string='VAT NO')
    
class outlet(models.Model):
    _name = 'outlet'

    name = fields.Char('Outlet Name', required=True)
    outlet_type_id = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')
    description = fields.Text('Description', translate=True)
    ratecard_sin = fields.One2many(comodel_name='ratecard.sin', inverse_name='outlet_id', 
                                  string='RateCard Singular')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        help='Select a company for this outlet if it exists',
        ondelete='restrict'
    )
    
    
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
        'product.template',
        'outlet_id',
        string='Outlet Products',
    )
    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )

    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)
        timeband_id = fields.Many2one(
                'timeband',
                string='Time Band',
                help='Select a time band for this product'
            )
    pages_id = fields.Many2one(
               'pages',
               string='Pages',
               help='Select a page for this product'
           )    
    ad_size_id = fields.Many2one(
                   'ad.size',
                   string='AD SIZE',
                   help='Set AD SIZE for this product'
               )
    outlet_type_id = fields.Many2one(
                   'outlet.type',
                   string='Outlet  Type',
                   help='Set Outlet  Type for this product'
               )  
    digital_location_id = fields.Many2one(
                      'digital.location',
                      string='Digital  Location',
                      help='Select  digital  location  for this product'
                  )        
    digital_type_id = fields.Many2one(
                         'digital.type',
                         string='Digital  Type',
                         help='Select  digital  type  for this product'
                     )  
    digital_size_id = fields.Many2one(
                         'digital.size',
                         string='Digital  Size',
                         help='Select  digital  size  for this product'
                     ) 
    ratecard_sin_id = fields.Many2one(
                         'ratecard.sin',
                         string='RateCard Type Singular',
                         help='Select   RateCard  Type  Singular for this product'
                     )  
    ratecard_mul_id = fields.Many2one(
                            'ratecard.mul',
                            string='RateCard Type Multiple',
                            help='Select   RateCard  Type  Multiple for this product'
                        ) 
    ad_type_id = fields.Many2one(
                            'ad.type',
                            string='Ad Type Singular',
                            help='Select   Ad  Type   for this product'
                        )      
    vat_rate_id = fields.Many2one(
                            'vat.rate',
                            string='VAT  Rate ',
                            help='Select   VAT RATE for this product'
                        )
    payment_terms_id = fields.Many2one(
                            'payment.terms',
                            string='PAYMENT  TERMS ',
                            help='Select  PAYMENT  TERMS for this product'
                        )  
    rateclass_code_id = fields.Many2one(
                            'rateclass.code',
                            string='RATECLASS  CODE',
                            help='Select  RATECLASS  CODE for this product'
                        )
    quote_stage_id = fields.Many2one(
                            'quote.stage',
                            string='QUOTE STAGE',
                            help='Select   QUOTE  STAGE  for this product'
                        )      
   



class ProductTemplate(models.Model):
    
    _inherit = 'product.template'
    
    spot_length_id  =  fields.Many2one(comodel_name='spot.length', string='Spot Length')

    outlet_id = fields.Many2one(
        'outlet',
        string='Outlet',
        help='Select a outlet for this product'
    )    
    timeband_id = fields.Many2one(
           'timeband',
           string='Time Band',
           help='Select a time band for this product'
       )
    pages_id = fields.Many2one(
               'pages',
               string='Pages',
               help='Select a page for this product'
           )    
    ad_size_id = fields.Many2one(
                   'ad.size',
                   string='AD SIZE',
                   help='Set AD SIZE for this product'
               )
    outlet_type_id = fields.Many2one(
                   'outlet.type',
                   string='Outlet  Type',
                   help='Set Outlet  Type for this product'
               )  
    digital_location_id = fields.Many2one(
                      'digital.location',
                      string='Digital  Location',
                      help='Select  digital  location  for this product'
                  )        
    digital_type_id = fields.Many2one(
                         'digital.type',
                         string='Digital  Type',
                         help='Select  digital  type  for this product'
                     )  
    digital_size_id = fields.Many2one(
                         'digital.size',
                         string='Digital  Size',
                         help='Select  digital  size  for this product'
                     ) 
    ratecard_sin_id = fields.Many2one(
                         'ratecard.sin',
                         string='RateCard Type Singular',
                         help='Select   RateCard  Type  Singular for this product'
                     )  
    ratecard_mul_id = fields.Many2one(
                            'ratecard.mul',
                            string='RateCard Type Multiple',
                            help='Select   RateCard  Type  Multiple for this product'
                        ) 
    ad_type_id = fields.Many2one(
                            'ad.type',
                            string='Ad Type Singular',
                            help='Select   Ad  Type   for this product'
                        )      
    vat_rate_id = fields.Many2one(
                            'vat.rate',
                            string='VAT  Rate ',
                            help='Select   VAT RATE for this product'
                        )
    payment_terms_id = fields.Many2one(
                            'payment.terms',
                            string='PAYMENT  TERMS ',
                            help='Select  PAYMENT  TERMS for this product'
                        )  
    rateclass_code_id = fields.Many2one(
                            'rateclass.code',
                            string='RATECLASS  CODE',
                            help='Select  RATECLASS  CODE for this product'
                        )
    quote_stage_id = fields.Many2one(
                            'quote.stage',
                            string='QUOTE STAGE',
                            help='Select   QUOTE  STAGE  for this product'
                        )      
    

class  timeband(models.Model):
    _name= 'timeband'
    _description = 'Time Band'    
    
    name   = fields.Char(string='Name' , size=64  ,  required=True)
    description = fields.Text('Description', translate=True)  
    hour_from  =  fields.Selection(selection=hour_from, string='HOUR FROM')
   # hour_from  = fields.date(string=' HOUR  FROM' , default=lambda self,cr,uid,context=None: fields.date.context_today(self,cr,uid,context) + " 09:00:00")
    hour_to  =  fields.Selection(selection=hour_to, string='HOUR TO')
    rate_class  = fields.Char(string='RATE  CLASS  CODE')
    list_position = fields.Selection(selection=list_position, string='LIST POSITION')
    
   
    logo = fields.Binary('Logo File')
    
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='timeband_id', 
                                     string='Time Bands')
    
    product_ids = fields.One2many(
          'product.template',
          'timeband_id',
          string='Time Band',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )

    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this Time  Band if it exists',
            ondelete='restrict'
        )    
    
class  pages(models.Model):
    _name  = 'pages'
    _description = 'Pages'
    
    name  =  fields.Integer(string='NAME' , size=64  , required=True )
    page  = fields.Selection(selection=page_no, string='PAGE')
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='pages_id', 
                                  string='Pages')
    
    product_ids = fields.One2many(
          'product.template',
          'pages_id',
          string='Pages',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  PAGE if it exists',
            ondelete='restrict'
        )        
    
    
    class  ad_size(models.Model):
        _name  = 'ad.size'
        _description = 'AD  SIZE'
        
        name  =  fields.Char(string='NAME')
        column  = fields.Selection(selection=_ad_column, string='COLUMN')
        inches  =  fields.Selection(selection=_ad_inches, string='INCHES')
        
        description = fields.Text('Description', translate=True)          
        logo = fields.Binary('Logo File')
        product_ids = fields.One2many(
              'product.template',
              'ad_size_id',
              string='AD SIZE',
          )    
    
        products_count = fields.Integer(
            string='Number of products',
            compute='_get_products_count',
        )
        
        @api.one
        @api.depends('product_ids')
        def _get_products_count(self):
            self.products_count = len(self.product_ids)
    
        
        outlet_id = fields.Many2one(
                'outlet',
                string='Outlet',
                help='Select a brand for this AD  SIZE if it exists',
                ondelete='restrict'
            )                

class  outlet_type(models.Model):
    _name  =  'outlet.type'
    _description = 'Outlet Type'
    
    name = fields.Char(string='NAME')
    #fields.Selection(selection=outlettype_, string='OUTLET TYPE')
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    outlet_id  = fields.One2many(comodel_name='outlet', inverse_name='outlet_type_id', 
                                string='Outlet Type')
    ratecard_sin_id  = fields.One2many(comodel_name='ratecard.sin', inverse_name='outlet_type_id', 
                                   string='Outlet Type')
    product_ids = fields.One2many(
          'product.template',
          'outlet_type_id',
          string='Outlet Type',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  Outlet  Type if it exists',
            ondelete='restrict'
        )       
        
class  digital_location(models.Model):
    _name  =  'digital.location'
    _description = 'Digital  Location'
    
    name  =  fields.Char(string='Digital Location',  size=64  ,  required=True)    
    ratecard_sin_id =fields.One2many(comodel_name='ratecard.sin', inverse_name='digital_location_id', 
                                    string='Digital Location')
    digital_location_id = fields.Many2one(
            'digital.location',
            string='Digital  Location',
            help='Select the  digital  location for this product'
        )        
    location  = fields.Char(string='LOCATION',  size=64  ,  required=True)
    homepage  =  fields.Char(string='HOMEPAGE' , size=64)
    news_page  =  fields.Char(string='NEWS PAGE' , size =64)
    entertainment_page = fields.Char(string='ENTERTAINMENT  HOME  PAGE' , size=64  ,  required=True)
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'digital_location_id',
          string='Digital Location',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  Digital  Location if it exists',
            ondelete='restrict'
        )       




class  digital_type(models.Model):
    _name  =  'digital.type'
    _description = 'DIGITAL  TYPE '
    
    name  =  fields.Char(string='NAME' , size=64  ,  required=True)
    #this  is  supposed to  be  one2one
    _type  = fields.Char(string='TYPE' , size=64  ,  required=True)
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='digital_type_id' , string='Digital  Type')
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'digital_type_id',
          string='Digital Type',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  Digital  Type if it exists',
            ondelete='restrict'
        )       


    

class  digital_size(models.Model):
    _name  = 'digital.size'
    _description = 'DIGITAL  SIZE '
    
    name  =  fields.Char(string='NAME' , size=64 ,  required=True)
    length =  fields.Integer(string='LENGTH(PIXELS)' , size=64  ,  required=True)
    width  = fields.Integer(string='WIDTH(PIXELS)' , size=64  , required=True)
    digital_type_id  =  fields.Many2one('digital.type' , 'DIGITAL TYPE')
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='digital_size_id' ,  string='Digital Size')
    
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'digital_size_id',
          string='Digital Size',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  Digital  Size if it exists',
            ondelete='restrict'
        )       



class  ratecard_sin(models.Model):
    _name =  'ratecard.sin'
    _description  = 'RATE CARD TYPE SINGULAR  '
    
    name  =   fields.Char(string='NAME')
    outlet_id = fields.Many2one(comodel_name='outlet', string='Outlet')
    timeband_id  = fields.Many2one(comodel_name='timeband', string='TimeBand')
    pages_id  =   fields.Many2one(comodel_name='pages', string='Pages')
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')
    digital_location_id  = fields.Many2one(comodel_name='digital.location', string='Digital Location')
    digital_type_id  = fields.Many2one(comodel_name='digital.type', string='Digital Type')
    digital_size_id  = fields.Many2one(comodel_name='digital.size', string='Digital  Size')
    ad_type_id  = fields.Many2one(comodel_name='ad.type', string='Ad Type')
    vat_rate_id  = fields.Many2one(comodel_name='vat.rate', string='Vat Rate')
    payment_terms_id  = fields.Many2one(comodel_name='payment.terms.id', string='Payment Terms')
    rateclass_code_id  = fields.Many2one(comodel_name='rateclass.code', string='RateClass Code')
    quote_stage_id  = fields.Many2one(comodel_name='quote.stage', string='Quote Stage')
    spot_length_id  = fields.Many2one(comodel_name='spot.length', string='Spot Length')
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'ratecard_sin_id',
          string='RateCard Type  Singular ',
      )    
    ratecard_mul_id = fields.Many2one( 'ratecard.mul',string='RateCard')      
    
    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    


    
class  ratecard_mul(models.Model):
    _name = 'ratecard.mul'
    _description = 'RATECARD TYPE  MULTIPLE'
    
    name  =  fields.Char(string='RATECARD MULTIPLE')
    ratecard_sin_id  =  fields.One2many(comodel_name='ratecard.sin',inverse_name='ratecard_mul_id',
                                string='MULTIPLES')
    
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'ratecard_mul_id',
          string='RateCard Type Multiple',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)
   
     

class  ad_type(models.Model):
    _name  =  'ad.type'
    _description = 'Ad TYPE'
    
    name  =  fields.Char(string='AD  TYPE' , size=64  , required=True)
    digital_ad_type = fields.Char(string='OUTLET TYPE')
    rate_card_type  = fields.Char(string='RATE  CARD  TYPE')
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='ad_type_id' , string="Ad Type")
    
    
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'ad_type_id',
          string='Ad Type',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  Ad TYpe if it exists',
            ondelete='restrict'
        )       




class  var_rate(models.Model):
    _name  = 'vat.rate'
    _description = 'VAT  RATE'
    
    name  = fields.Char(string='NAME')
    rate =  fields.Float(string='VAT RATE', digits=(17,3) )    # TODO  WHY  ITS  CAUSING A  CLIENT  ERROR  _sprinf  huh ? 
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='vat_rate_id' , string='Vat Rate')

    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'vat_rate_id',
          string='VAT  RATE',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  VAT  RATE if it exists',
            ondelete='restrict'
        )       


    
    
class  payment_terms(models.Model):
    _name  =  'payment.terms'
    _description = 'PAYMENT  TERMS'
    
    name   = fields.Char(string='CASH/CHEQUE' , help  = 'NETT 30    for  30 days  ')
    days  =   fields.Char(string='DAYS')
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='payment_terms_id' , string='Payment Terms')
    
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'payment_terms_id',
          string='Payment  Terms',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  Payment  Terms  if it exists',
            ondelete='restrict'
        )       



class  rateclass_code(models.Model):
    _name = 'rateclass.code'
    _description = 'RATECLASS  CODE'
    
    code  =  fields.Char(string='CODE' ,  required=True)
    name  =  fields.Char(string='MOVEABLE' ,  required=True)
    rate_class_type  =   fields.Char(string='TYPE' ,  required=True ,  size=256)
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='rateclass_code_id' , string='RateClass Code')
    
    
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'rateclass_code_id',
          string='RATECLASS  CODE',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  RATECLASS  CODE if it exists',
            ondelete='restrict'
        )       


    
class  quote_stage(models.Model):
    _name  =  'quote.stage'
    _decription  =  'QUOTE STAGE'
    
    name  =fields.Char(string='Name')
    code =  fields.Char(string='CODE' , size=64)
    quote_stage =  fields.Selection([('draft' , 'DRAFT'),
                                     ('negotiation' , 'NEGOTIATION'),
                                     ('delivered' , 'DELIVERED') , 
                                     ('closed_accepted' , 'CLOSED  ACCEPTED'),
                                     ('closed_lost' , 'CLOSED LOST'),
                                     ('closed_dead' , 'CLOSED DEAD'),
    ], string='QUOTE STAGE')
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='quote_stage_id' , string='Quote Stage')
    product_ids = fields.One2many(
          'product.template',
          'quote_stage_id',
          string='QUOTE  STAGE',
      )    

    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one(
            'outlet',
            string='Outlet',
            help='Select a brand for this  QUOTE  STAGE  Multiple if it exists',
            ondelete='restrict'
        )      