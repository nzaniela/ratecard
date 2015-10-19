# -*- encoding: utf-8 -*-
###############################################################################
#Outlet  --> Outlet                                                             #
###############################################################################
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp import tools
from  ragconstants import  year_week_no , days ,payment_type , schedule_types ,payment_duration, seconds , minutes  ,list_position , hour_from , hour_to , page_no ,_ad_column , _ad_inches , outlettype_

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
    rate_id = fields.Many2one(
                       'rate',
                       string='RATE',
                       help='Set RATE for this product'
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
                         string='RateCard Singular',
                         help='Select   RateCard  Type  Singular for this product'
                     )  
    multiple_ratecard_id = fields.Many2one(
                            'ratecard.mul',
                            string='RateCard Multiple',
                            help='Select   RateCard Multiple for this product'
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
    schedule_type_id = fields.Many2one(
              'schedule.type',
              string='Schedule',
              help='Select a Schedule for this product'
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
    
    rate_id  = fields.One2many(comodel_name='rate', inverse_name='timeband_id', 
                              string='RATE')
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
    ad_type_id  = fields.One2many(comodel_name='ad.type', inverse_name='outlet_type_id', 
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
    payment_terms_id  = fields.Many2one(comodel_name='payment.terms', string='Payment Terms')
    rateclass_code_id  = fields.Many2one(comodel_name='rateclass.code', string='RateClass Code')
    quote_stage_id  = fields.Many2one(comodel_name='quote.stage', string='Quote Stage')
    spot_length_id  = fields.Many2one(comodel_name='spot.length', string='Spot Length')
    schedule_type_id=fields.Many2one(comodel_name='schedule.type', string='Schedule Type')
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
    #ratecard_sin_id  =  fields.One2many(comodel_name='ratecard.sin',inverse_name='ratecard_mul_id',
                                #string='MULTIPLES')
    multiple_ratecard_id  = fields.Many2many(comodel_name='ratecard.sin', relation='ratecard_mul_ratecard_sin_rel', 
                                            column1='ratecard_mul_id', 
                                            column2='ratecard_sin_id', 
                                            string='RATECARDS')
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'multiple_ratecard_id',
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
    
    name  =  fields.Char(string='AD  TYPE' , size=64  , required=True)
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='OUTLET TYPE')
    rate_card_type  = fields.Selection(selection=[('0','SINGULAR'),('1','MULTIPLE')], string='RATECARD TYPE')
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='ad_type_id' , string="Ad Type")
   # name  = fields.One2many(comodel_name='rate', inverse_name='name', string='NAME')
 
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
            help='Select a brand for this  Ad Type if it exists',
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
    
    name   = fields.Selection(selection=payment_type,string='CASH/CHEQUE' , help  = 'NETT 30    for  30 days  ')
    days  =   fields.Selection(selection=payment_duration, string="DAYS")
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
class schedule_type(models.Model):
    _name = 'schedule.type'
    
    #add  name_get  so  that  when  schedule  name  is  called  the  type  to  be  passed  also
    
    name = fields.Selection(selection=[
        ('banded','BANDED'),
        ('fixed','FIXED')
        ],
                            string='Schedule Name')
    schedule_type = fields.Selection(selection=schedule_types, string='Schedule ')
    ratecard_sin_id = fields.One2many(comodel_name='ratecard.sin', inverse_name='schedule_type_id' , string='Schedule Type')
    description = fields.Text('Description', translate=True)
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
              'product.template',
              'schedule_type_id',
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
        

class  noof_spots(models.Model):
    _name= 'noof.spots'
    
    #dayofweek=fields.Selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], string='Day of Week', required=True, select=True)
    sunday   = fields.Integer(string='S')    
    monday  = fields.Integer(string='M')
    tuesday   = fields.Integer(string='T')
    wednesday   = fields.Integer(string='W')
    thursday   = fields.Integer(string='T')
    friday   = fields.Integer(string='F')
    saturday   = fields.Integer(string='S')
    spot_total  = fields.Integer(string='TOTAL SPOTS= ' , compute='_compute_spots' , store=True)
    weeks  = fields.Integer(string='WEEKS')    
    
    description = fields.Text('Description', translate=True) 
    
    #@api.one
    #@api.depends('sunday' , 'monday','tuesday' ,'wednesday'  , 'thursday'  ,'friday'  , 'saturday')
    #def  _compute_spots(self):
        #self.total = self.sunday + self.monday + self.tuesday+ self.wednesday+self.thursday + self.friday + self.saturday
    @api.one
    @api.depends('sunday' , 'monday','tuesday' ,'wednesday'  , 'thursday'  ,'friday'  , 'saturday')    
    def _compute_spots(self):
        self.spot_total = False
        for  line  in  self:
            total  = line.sunday + line.monday + line.tuesday+ line.wednesday+line.thursday + line.friday + line.saturday
        self.update({'spot_total':total})
        
        
        
        
    #def  on_change_spots(self,cr,user,ids,sunday , monday,tuesday ,wednesday  , thursday  ,friday  , saturday,context=None):
        #total  = sunday + monday+tuesday + wednesday  + thursday  + friday  + saturday
        #res  = {
            #'value':{
            #'total':total
            #}
        #}
        #return res
    
    spot_week_id = fields.One2many(
              'noof.spots',
              'spot_week_id',
              string='WEEK SPOTS',
          )        


class  spot_weeks(models.Model):
    _name = 'spot_week'
    
    name=fields.Selection(selection=year_week_no, string='Year Week No')
    noof_spots_id = fields.Many2one(
                  'noof.spots',
                  string='WEEKLY SPOTS',
                  help='Select a weekly  spot for this product'
              )        
    
class  rate(models.Model):
    _name  = 'rate'
    
    name = fields.Char(string='NAME')#ad  type  name
    #name=fields.Many2one(comodel_name='ad.type', string='NAME')
    timeband_id = fields.Many2one(
        'timeband',
        string='TIMEBAND',
        help='Select a timeband  for  this  rate if it exists',
        ondelete='cascade')  
    rate_amount = fields.Integer(string='RATE AMOUNT')
    

class sale_order(models.Model):
    _inherit = 'sale.order'
    product_name  = fields.Char(string='Product  Name')
    is_template  = fields.Boolean(string='Template')
    template_id  = fields.Many2one(comodel_name='sale.order', string='Offer' ,domain=[('is_template', '=', True)] )
   
    def onchange_template(self, cr, uid, ids, template=False, partner_id=False, pricelist_id=False, fiscal_position=False):
        line_obj = self.pool.get('sale.order.line')
        result = {'order_line': []}
        lines = []
 
        if not template:
            return {'value': result}

        if not partner_id:
            raise models.except_orm(_('No Customer Defined!'), _('Before choosing a template,\n select a customer in the template form.'))

        template = self.browse(cr, uid, template)
        order_lines = template.order_line
        for line in order_lines:
            vals = line_obj.product_id_change(cr, uid, [],
                pricelist = pricelist_id,
                product = line.product_id and line.product_id.id or False,
                qty = 0.0,
                uom = False,
                qty_uos = 0.0,
                uos = False,
                name = '',
                partner_id = partner_id,
                lang = False,
                update_tax = True,
                date_order = False,
                packaging = False,
                fiscal_position = fiscal_position,
                flag = False)
            vals['value']['discount'] = line.discount
            vals['value']['product_id'] = line.product_id and line.product_id.id or False
            vals['value']['state'] = 'draft'
            vals['value']['product_uom_qty'] = line.product_uom_qty
            vals['value']['product_uom'] = line.product_uom and line.product_uom.id or False
            lines.append(vals['value'])
        result['order_line'] = lines
        result['note'] = self.merge_message(cr, uid, template.note, template, None)
        return {'value': result}

    def merge_message(self, cr, uid, note, template, context=None):
        if context is None:
            context = {}

        def merge(match):
            exp = str(match.group()[2:-2]).strip()
            result = None
            try:
                result = eval(exp,
                              {
                                'object': template,
                                'context': dict(context), # copy context to prevent side-effects of eval
                                'time': time,
                              })
            except:
                raise osv.except_osv(_('Error!'), _('Wrong python condition defined for template: %s.')% (template.name))
            if result in (None, False):
                return str("--------")
            return tools.ustr(result)

        com = re.compile('(\[\[.+?\]\])')
        message = com.sub(merge, note)

        return message

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

#class  singular_quotation(models.Model):
    #_name = "singular.quotation"
    #_inherit = ['mail.thread', 'ir.needaction_mixin']
    #name  = fields.Char(string='Name')
    #product_name = fields.Char(string='Product Name')
    #partner_id  = fields.Char(string='Partner ID')
    #amount_total = fields.Integer(string='Amount  Total')
    #timeband = fields.Char(string='TIMEBAND')
    #price_unit  = fields.Integer(string='PRICE UNIT')
    #discount  = fields.Integer(string='DISCOUNT')
    #tax_id  = fields.Integer(string='TAX _ID')
    #th_weight = fields.Integer(string='TH WEIGHT')
    #sequence = fields.Integer(string='SEQUENCE')
    #amount_untaxed = fields.Integer(string='UNTAXED')
    #amount_tax = fields.Integer(string='AMOUNT  TAXED')
    #amount_total = fields.Integer(string='AMOUNT TOTAL')
    #state = fields.Selection([
        #('draft', 'Draft Quotation'),
        #('sent', 'Quotation Sent'),
        #('cancel', 'Cancelled'),
        #('waiting_date', 'Waiting Schedule'),
        #('progress', 'Sales Order'),
        #('manual', 'Sale to Invoice'),
        #('shipping_except', 'Shipping Exception'),
        #('invoice_except', 'Invoice Exception'),
        #('done', 'Done'),
            #], 'Status', readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
              #\nThe exception status is automatically set when a cancel operation occurs \
              #in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               #but waiting for the scheduler to run on the order date.", select=True)  
    
    
    
    
    
    


    
    
    
    
    