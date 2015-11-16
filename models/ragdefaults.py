# -*- encoding: utf-8 -*-
###############################################################################
#Outlet  --> Outlet                                                             #
###############################################################################
from openerp.tools.translate import _
from openerp import tools ,exceptions

import logging
import time
import  re
from datetime import date
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, timedelta
from openerp import SUPERUSER_ID
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from  ragconstants import  year_week_no , days ,payment_type , schedule_types ,payment_duration, seconds , minutes  ,list_position , hour_from , hour_to , page_no ,_ad_column , _ad_inches , outlettype_
import  pudb

#class sic_codes(models.Model):
    #_name = 'sic.codes'
    #name  = fields.Char(string='SIC NAME')
    #codes = fields.Char(string="Code")
class  week(models.Model):
    _name='week'
    
    # multiple_rate  =  fields.Integer(string='RATE ')
    # code  = fields.Char(string='ALLOCATION SPOTS CODE',readonly=True)
    #
    # _defaults = {
    #     'code':lambda obj,cr,uid,context:'/'
    # }
    #
    # def  create(self,cr,uid, vals,context=None):
    #     vals['code'] = self.pool.get('ir.sequence').get(cr,uid,'week')
    #     return super(week,self).create(cr,uid,vals,context=context)
    week_count = fields.Integer('COUNT WEEK')
    monday  = fields.Integer(string='MON')
    tuesday   = fields.Integer(string='TUE')
    wednesday   = fields.Integer(string='WED')
    thursday   = fields.Integer(string='THUR')
    friday   = fields.Integer(string='FRI')
    saturday   = fields.Integer(string='SAT')
    sunday   = fields.Integer(string='SUN')
    noofweeks = fields.Integer(string="WEEKS",default=1 , store=True,   track_visibility='always')
    #compute='_noofweeks',
    spot_total  = fields.Integer( compute='_compute_totalspots' , string='SPOTS TOTAL' ,readonly=True ,  store=True)

    price_subtotal = fields.Integer(compute='_compute_spotrateweektotal', string='SUBTOTAL', readonly=True, store=True)
    state = fields.Selection([
            ('draft', 'DRAFT'),
            ('sent', 'READY'),
            ('sale', 'FINAL'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
            ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')  
    validity_date = fields.Date(string='Validity Date', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    price_tax = fields.Integer(default=0 ,string='Taxes', readonly=True, store=True)
    #weeks  = fields.Integer(string='WEEKS')  
    ratecard_mul_rel_id  = fields.One2many(comodel_name='ratecard.mul.rel', inverse_name='allocate_id', 
                                   string='ALLOCATED SPOTS')
    
    
    allocate_mul_spots_id  = fields.One2many(comodel_name='allocate.mul.spots', inverse_name='week_id', string='ALLOCATED SPOTS')
    ratecard_multiple_id  = fields.Many2one(comodel_name='ratecard.multiple', string='ALLOCATED SPOTS')    
    ratecard_multi_id  = fields.One2many(comodel_name='ratecard.mul', inverse_name='week_id', string='ALLOCATED SPOTS')

    ratecard_sin_radio_id  = fields.One2many(comodel_name='ratecard.sin.radio',inverse_name='week_id',string='RADIO RATECARD')
    # @api.multi
    # def  name_get(self):
    #     result = []
    #     for  record in  self:
    #         print 'record name ' , record.rate_amount
    #         # if  record.name  and  record.code:
    #         #     result.append((record.id,record.name + '/' + record.code))
    #         if  record.rate_amount  or  record.id:
    #             result.append((record.id,record.name+ str('Ksh::')+str(record.rate_amount)))
    #     return result
    # monday  = fields.Integer(string='MON')
    # tuesday   = fields.Integer(string='TUE')
    # wednesday   = fields.Integer(string='WED')
    # thursday   = fields.Integer(string='THUR')
    # friday   = fields.Integer(string='FRI')
    # saturday   = fields.Integer(string='SAT')
    # sunday   = fields.Integer(string='SUN')
    # @api.model
    # def  name_search(self, name='', args=None, operator='ilike', limit=100):
    #     args = args or  []
    #     recs = self.browse()
    #     if  name :
    #         recs = self.search([('name' ,'=',name)] + args , limit=limit)
    #     if  not  recs:
    #         recs = self.search([('name' ,operator , name)] + args , limit=limit)
    #     return recs.name_get()
    
    @api.one
    @api.depends('noofweeks','ratecard_multiple_id.scheduled_for')
    def _noofweeks(self):
        """
        Compute autofill noofweeks.
        """
        for order in self:
            for line in order.ratecard_multiple_id:
                print  'line.scheduled_for== ' , line.scheduled_for
                s = line.scheduled_for *1 
                
            order.update({'noofweeks': s })            
    
    @api.one
    @api.depends('sunday' , 'monday','tuesday' ,'wednesday'  , 'thursday'  ,'friday'  , 'saturday')    
    def _compute_totalspots(self):
        for order in self:
            for  line  in  order:
                spottotal  = line.sunday + line.monday + line.tuesday+ line.wednesday+line.thursday + line.friday + line.saturday
            self.update({'spot_total':spottotal})    
        
    @api.one
    @api.depends('sunday' , 'monday','tuesday' ,'wednesday'  , 'thursday'  ,'friday'  , 'saturday', 'noofweeks')
    def _compute_spotrateweektotal(self):
        for order in self:
            for  line  in  order:
                week_spot_total  = line.sunday + line.monday + line.tuesday+ line.wednesday+line.thursday + line.friday + line.saturday
                subtotal = week_spot_total *  line.noofweeks
            self.update({'price_subtotal':subtotal})    
 
    
    
class  allocate_spots(models.Model):
    _name= 'allocate.spots'
    
    #dayofweek=fields.Selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], string='Day of Week', required=True, select=True)
    name = fields.Integer(string='NO OF WEEKS')
    monday  = fields.Integer(string='MON')
    tuesday   = fields.Integer(string='TUE')
    wednesday   = fields.Integer(string='WED')
    thursday   = fields.Integer(string='THUR')
    friday   = fields.Integer(string='FRI')
    saturday   = fields.Integer(string='SAT')
    sunday   = fields.Integer(string='SUN')    
    
    spot_total  = fields.Integer(string='TOTAL SPOTS= ' , compute='_compute_spots' , store=True)
    weeks  = fields.Integer(string='WEEKS')
    # sale_order_id  = fields.One2many(comodel_name='sale.order', inverse_name='allocate_spots_id',string='Allocate Spots')
    # sale_order_line_id = fields.One2many(comodel_name='sale.order.line', inverse_name='allocate_spots_id',string='Allocate Spots')
    @api.one
    @api.depends('sunday' , 'monday','tuesday' ,'wednesday'  , 'thursday'  ,'friday'  , 'saturday')    
    def _compute_spots(self):
        self.spot_total = False
        for  line  in  self:
            total  = line.sunday + line.monday + line.tuesday+ line.wednesday+line.thursday + line.friday + line.saturday
        self.update({'spot_total':total})
            
            
class  allocate_mul_spots(models.Model):
    _name= 'allocate.mul.spots'
    
    week_id = fields.Many2one( 'week',string='WEEK')  
    # sale_order_line_id = fields.One2many(comodel_name='sale.order.line', inverse_name='allocate_mul_spots_id',string='Allocate Multiple Spots')
    
    #dayofweek=fields.Selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], string='Day of Week', required=True, select=True)
    #monday  = fields.Integer(string='MON')
    #tuesday   = fields.Integer(string='TUE')
    #wednesday   = fields.Integer(string='WED')
    #thursday   = fields.Integer(string='THUR')
    #friday   = fields.Integer(string='FRI')
    #saturday   = fields.Integer(string='SAT')
    #sunday   = fields.Integer(string='SUN')    
    
    #spot_total  = fields.Integer(string='TOTAL SPOTS= ' , compute='_compute_spots' , store=True)
    #weeks  = fields.Integer(string='WEEKS')
    #sale_order_id  = fields.One2many(comodel_name='sale.order', inverse_name='allocate_spots_id', 
                                    #string='Allocate Spots')
    
    #sale_order_line_id = fields.Many2one( 'sale.order.line',string='ALLOCATE MULTIPLE SPOTS')  
    def _set_requested_date(self, cr, uid, ids, context=None):
        requested_date = (date.today() + timedelta(days=28)).strftime(DEFAULT_SERVER_DATE_FORMAT),
        day = date.today()
        if day.isoweekday() == 6:
            requested_date = (date.today() + timedelta(days=30)).strftime(DEFAULT_SERVER_DATE_FORMAT),
        if day.isoweekday() == 7:
            requested_date = (date.today() + timedelta(days=29)).strftime(DEFAULT_SERVER_DATE_FORMAT),
        return requested_date
    
    _defaults = {
        'mon': _set_requested_date,
    }    
    @api.one
    @api.depends('sunday' , 'monday','tuesday' ,'wednesday'  , 'thursday'  ,'friday'  , 'saturday')    
    def _compute_spots(self):
        self.spot_total = False
        for  line  in  self:
            total  = line.sunday + line.monday + line.tuesday+ line.wednesday+line.thursday + line.friday + line.saturday
        self.update({'spot_total':total})
            
            
    
class  quo_mul(models.Model):
    _name= 'quo.mul'
    _description = 'Multiple Quotation'    
    
    name   = fields.Char(string='Name' , size=64  ,  required=True)
    description = fields.Text('Description', translate=True)  
    outlet = fields.Char(string="Outlet")
    
   
    logo = fields.Binary('Logo File')  
    
    product_ids = fields.One2many(
          'product.template',
          'quo_mul_id',
          string='Multiple Quotation',
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
  
        
class spot_length(models.Model):
    _name = 'spot.length'
    name = fields.Char(string='NAME')
    seconds = fields.Selection(selection=seconds, string='Seconds')
    ratecard_sin_radio_id  = fields.One2many(comodel_name='ratecard.sin.radio', inverse_name='spot_length_id', string='Spot Length')
    ratecard_sin_tv_id  = fields.One2many(comodel_name='ratecard.sin.tv', inverse_name='spot_length_id',  string='Spot Length')
    sale_order_line_id = fields.One2many(comodel_name='sale.order.line', inverse_name='spot_length_id',string='Spot Length')

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

    # is_branch = fields.Boolean('Is Branch?')
    # parent_root_id = fields.Many2one('res.partner', 'Main Partner', domain=[('is_company', '=', True), ('is_branch', '=', False)])
    vat_no = fields.Integer(string='VAT NO:')

    # @api.multi
    # def name_get(self):
    #     res = super(res_partner, self).name_get()
    #     res_dict = dict(res)
    #     for record in self:
    #         if record.parent_root_id and record.is_branch:
    #             res_dict[record.id] = "%s / %s" % (record.parent_root_id.name, res_dict[record.id])
    #     return res_dict.items()

class outlet(models.Model):
    _name = 'outlet'

    name  = fields.Many2one('res.partner',string='OUTLET NAME' ,required=True)
    #name = fields.Char('Outlet Name', required=True)
    outlet_type_id = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')
    description = fields.Text('Description', translate=True)
    ratecard_sin_digital_id= fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='outlet_id',string='RateCard Singular')
    ratecard_sin_tv_id = fields.One2many(comodel_name='ratecard.sin.tv', inverse_name='outlet_id',string='RateCard Singular')
    ratecard_sin_print_id = fields.One2many(comodel_name='ratecard.sin.print', inverse_name='outlet_id',string='RateCard Singular')
    ratecard_sin_radio_id = fields.One2many(comodel_name='ratecard.sin.radio', inverse_name='outlet_id',string='RateCard Singular')
    sale_order_line_id = fields.One2many(comodel_name='sale.order.line', inverse_name='outlet_id',string='Outlet')
    sale_order_id = fields.One2many(comodel_name='sale.order', inverse_name='outlet_id',string='Outlet')
    ratecard_mul_id = fields.One2many(comodel_name='ratecard.mul', inverse_name='outlet_id',string='Outlet')
    ratecard_multiples_id = fields.One2many(comodel_name='ratecard.multiples', inverse_name='outlet_id',string='Outlet')
    rate  = fields.One2many(comodel_name='rate', inverse_name='outlet_id',string='Outlet')
    company_id = fields.Many2one('res.company',string='Company',help='Select a company for this outlet if it exists',ondelete='restrict')
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many('product.template','outlet_id',string='Outlet Products',)
    products_count = fields.Integer(string='Number of products',compute='_get_products_count',)

    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)
        timeband_id = fields.Many2one('timeband',string='Time Band',help='Select a time band for this product')
    pages_id = fields.Many2one('pages',string='Pages',help='Select a page for this product')
    ad_size_id = fields.Many2one('ad.size',string='AD SIZE',help='Set AD SIZE for this product')
    outlet_type_id = fields.Many2one('outlet.type',string='Outlet  Type',help='Set Outlet  Type for this product')
    digital_location_id = fields.Many2one('digital.location',string='Digital  Location',
                      help='Select  digital  location  for this product')
    digital_type_id = fields.Many2one('digital.type',string='Digital  Type',help='Select  digital  type  for this product')
    digital_size_id = fields.Many2one('digital.size', string='Digital  Size',help='Select  digital  size  for this product')
  
    ratecard_sin_radio_id = fields.Many2one( 'ratecard.sin.radio',string='RateCard Type Singular',help='Select   RateCard  Type  Singular for this product')      
    ratecard_sin_tv_id = fields.Many2one( 'ratecard.sin.tv',string='RateCard Type Singular',help='Select   RateCard  Type  Singular for this product')      
    ratecard_sin_digital_id = fields.Many2one( 'ratecard.sin.digital',string='RateCard Type Singular',help='Select   RateCard  Type  Singular for this product')      
    ratecard_sin_print_id = fields.Many2one( 'ratecard.sin.print',string='RateCard Type Singular',help='Select   RateCard  Type  Singular for this product')      
    
    ratecard_mul_id = fields.Many2one('ratecard.mul',string='RateCard Type Multiple',help='Select   RateCard  Type  Multiple for this product')
    ad_type_id = fields.Many2one('ad.type', string='Ad Type Singular', help='Select   Ad  Type   for this product')
    vat_rate_id = fields.Many2one('vat.rate', string='VAT  Rate ',help='Select   VAT RATE for this product')
    payment_terms_id = fields.Many2one('payment.terms',string='PAYMENT  TERMS ', help='Select  PAYMENT  TERMS for this product' )
    rateclass_code_id = fields.Many2one( 'rateclass.code',string='RATECLASS  CODE',help='Select  RATECLASS  CODE for this product')
    quote_stage_id = fields.Many2one('quote.stage', string='QUOTE STAGE',help='Select   QUOTE  STAGE  for this product')
    rate_id = fields.Many2one( 'rate',string='RATE',help='Set RATE for this product')
    _sql_constraints = [
           ('name_uniq','unique(name)','Outlet  Must Be Unique!'),
       ]    
    # @api.multi
    # def  name_get(self):
    #     result = []
    #     for  record in  self:
    #         if  record.name  and  record.id:
    #             result.append((record.name ,record.id))
    #         if  record.id:
    #             result.append((record.name,record.id))
    #
    #
    #     return result
    # @api.multi
    # def name_get(self):
    #     res = super(res_partner, self).name_get()
    #     res_dict = dict(res)
    #     for record in self:
    #         if record.name and record.id:
    #             res_dict[record.id] = "%s / %s" % (record.name, res_dict[record.id])
    #     return res_dict.items()

    @api.model
    def  name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or  []
        recs = self.browse()
        if  name :
            recs = self.search([('name' ,'=',name)] + args , limit=limit)
        # if  id:
        #     recs = self.search([('id' , '=' , id)] + args , limit=limit)
        if  not  recs:
            recs = self.search([('name' ,operator , name)] + args , limit=limit)
        return recs.name_get()


class ProductTemplate(models.Model):
    
    _inherit = 'product.template'

    name  = fields.Char('RATECARD')


    outlet_id = fields.Many2one('outlet',string='Outlet',help='Select a outlet for this product')
    ratecard_multiple_id = fields.Many2one('ratecard.multiple',string='MULTIPLE RATECARD')
    ratecard_multiples_id = fields.Many2one('ratecard.multiples',string='MULTIPLES RATECARD')
    rate_id = fields.Many2one(comodel_name='rate', string='RATE')

    timeband_id = fields.Many2one('timeband',string='Time Band',help='Select a time band for this product')
    pages_id = fields.Many2one('pages',string='Pages',help='Select a page for this product')
    ad_size_id = fields.Many2one('ad.size',string='AD SIZE',help='Set AD SIZE for this product')
    outlet_type_id = fields.Many2one('outlet.type',string='Outlet  Type',help='Set Outlet  Type for this product')
    digital_location_id = fields.Many2one('digital.location',string='Digital  Location',help='Select  digital  location  for this product')
    digital_type_id = fields.Many2one('digital.type',string='Digital  Type',help='Select  digital  type  for this product')
    digital_size_id = fields.Many2one('digital.size',string='Digital  Size',help='Select  digital  size  for this product')
    ratecard_sin_radio_id = fields.Many2one('ratecard.sin.radio',string='RADIO SINGULAR RATECARD',help='Select   RADIO SINGULAR RATECARD for this product')
    ratecard_sin_digital_id = fields.Many2one('ratecard.sin.digital',string='DIGITAL SINGULAR RATECARD',help='Select   DIGITAL SINGULAR RATECARD for this product')
    ratecard_sin_print_id = fields.Many2one('ratecard.sin.print',string='PRINT SINGULAR RATECARD',help='Select PRINT SINGULAR RATECARD for this product')
    ratecard_sin_tv_id = fields.Many2one('ratecard.sin.tv',string='TV SINGULAR RATECARD',help='Select TV SINGULAR RATECARD for this product')

    multiple_ratecard_id = fields.Many2one('ratecard.mul',string='RateCard Multiple',help='Select   RateCard Multiple for this product')
    ad_type_id = fields.Many2one('ad.type',string='Ad Type Singular',help='Select   Ad  Type   for this product')
    vat_rate_id = fields.Many2one('vat.rate',string='VAT  Rate ',help='Select   VAT RATE for this product')
    payment_terms_id = fields.Many2one('payment.terms',string='PAYMENT  TERMS ',help='Select  PAYMENT  TERMS for this product')
    rateclass_code_id = fields.Many2one('rateclass.code',string='RATECLASS  CODE',help='Select  RATECLASS  CODE for this product')
    quote_stage_id = fields.Many2one('quote.stage',string='QUOTE STAGE',help='Select   QUOTE  STAGE  for this product')
    schedule_type_id = fields.Many2one('schedule.type',string='Schedule',help='Select a Schedule for this product')
    spot_length_id  =  fields.Many2one(comodel_name='spot.length', string='Spot Length')
    quo_mul_id  =  fields.Many2one(comodel_name='quo.mul', string='Multiple Quotation')

    radio_ratecards = fields.Boolean(string='RADIO RATECARDS')
    digital_ratecards = fields.Boolean(string='DIGITAL RATECARDS')
    print_ratecards = fields.Boolean(string='PRINT RATECARDS')
    tv_ratecards = fields.Boolean(string='TV RATECARDS')

    radio_ratecard_cost = fields.Float(string='RADIO RATE COST', store=True, readonly=True, compute='_get_radioratecard_rate', track_visibility='always')
    digital_ratecard_cost = fields.Float('DIGITAL Ratecard Cost', store=True, readonly=True, compute='_get_digitalratecard_rate', track_visibility='always')
    print_ratecard_cost = fields.Float('PRINT Ratecard Cost', store=True, readonly=True, compute='_get_printratecard_rate', track_visibility='always')
    tv_ratecard_cost = fields.Float('TV Ratecard Cost', store=True, readonly=True, compute='_get_tvratecard_rate', track_visibility='always')


    radio_multiple_ratecards = fields.Boolean(string='RADIO MULTIPLE RATECARDS')
    radio_multiple_ratecard_cost = fields.Float('RADIO MULTIPLE RATECARD COST', compute='_get_radio_multiple_ratecard_rate', store=True, readonly=True, track_visibility='always')

    _defaults = {
        'company_id': lambda s,cr,uid,c: s.pool.get('res.company')._company_default_get(cr, uid, 'product.template', context=c),
        'singular_ratecard_cost': 1,
        'multiple_ratecard_cost': 0.0,
        'radio_ratecards':0,
        'digital_ratecards':0,
        'print_ratecards':0,
        'tv_ratecards':0,
        'multiple_ratecards':0,
        'active': True,
    }
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        template = self.browse(cr, uid, id, context=context)
        default['name'] = _("%s (copy)") % (template['name'])
        return super(ProductTemplate, self).copy(cr, uid, id, default=default, context=context)


    @api.one
    @api.depends('ratecard_multiple_id')
    def _get_radio_multiple_ratecard_rate(self):
        for  order  in  self:
            print  'INSIDE PRODUCT TEMPLATE ', order
            print 'Can we  get  total_amount here'
            name = ''
            outlet_id = ''
            outlet_type_id  =''
            ad_type_id  =''
            spot_length_id  =''
            timeband_id = ''
            rate_id  = ''
            radio_multiple_ratecard_cost = 0.0
            for  line  in  order.ratecard_multiple_id:
                print 'ALLOCATE SCHEDULE  COUNT' , line.allocate_schedule_count
                print 'SPOT TOTAL' , line.total_spot
                # print 'VAT  RATE' ,line.ratecard_multiple_id.vat_rate_id.id
                print 'RATE' ,line.rate_amount
                radio_multiple_ratecard_cost += line.taxed_amount
                print 'radio_multiple_ratecard_cost' , radio_multiple_ratecard_cost
                print 'NAME OF RADIO RATECARD' , line.name

                name = line.name

            order.update({
                    'radio_multiple_ratecard_cost':radio_multiple_ratecard_cost,
                    'name':name,
                    'outlet_id':outlet_id,
                    'outlet_type_id':outlet_type_id,
                    'ad_type_id':ad_type_id,
                    'spot_length_id':spot_length_id,
                    'timeband_id':timeband_id,
                    'rate_id':rate_id,

            })
    @api.one
    @api.depends('ratecard_sin_radio_id.rate_id')
    def _get_radioratecard_rate(self):
        for  order  in  self:
            print  'order', order
            print 'PRODUCT NAME ' , order.name
            name = ''
            outlet_id = ''
            outlet_type_id  =''
            ad_type_id  =''
            spot_length_id  =''
            timeband_id = ''
            rate_id  = ''
            radio_ratecard_cost = 0.0
            for  line  in  order.ratecard_sin_radio_id:
                print 'timeband' , line.timeband_id.id
                print 'VAT  RATE' ,line.vat_rate_id.id
                print 'NAME OF RADIO RATECARD' , line.name
                name = line.name
                outlet_id = line.outlet_id
                outlet_type_id  = line.outlet_type_id
                ad_type_id  = line.ad_type_id
                spot_length_id  =line.spot_length_id
                timeband_id = line.timeband_id
                rate_id  = line.rate_id
                radio_ratecard_cost += line.rate_id.rate_amount
                print 'radio_ratecard_cost' , radio_ratecard_cost

            order.update({
                    'radio_ratecard_cost':radio_ratecard_cost,
                     'name':name,
                     'outlet_id':outlet_id,
                     'outlet_type_id':outlet_type_id,
                     'ad_type_id':ad_type_id,
                     'spot_length_id':spot_length_id,
                     'timeband_id':timeband_id,
                     'rate_id':rate_id,

            })


    @api.one
    @api.depends('ratecard_sin_digital_id.rate_id')
    def _get_digitalratecard_rate(self):
        for  order  in  self:
            print  'order', order
            name  = ''
            outlet_id = ''
            outlet_type_id  =''
            ad_type_id  =''
            spot_length_id  =''
            timeband_id = ''
            rate_id  = ''
            digital_ratecard_cost = 0.0
            for  line  in  order.ratecard_sin_digital_id:
                print 'timeband' , line.timeband_id.id
                # print 'VAT  RATE' ,line.vat_rate_id.id
                digital_ratecard_cost += line.rate_id.rate_amount
                print 'digital_ratecard_cost' , digital_ratecard_cost
                print 'NAME OF RADIO RATECARD' , line.name
                name = line.name
                outlet_id = line.outlet_id
                outlet_type_id  = line.outlet_type_id
                ad_type_id  = line.ad_type_id
                spot_length_id  =line.spot_length_id
                timeband_id = line.timeband_id
                rate_id  = line.rate_id
            order.update({
                    'digital_ratecard_cost':digital_ratecard_cost,
                    'name':name,
                    'outlet_id':outlet_id,
                    'outlet_type_id':outlet_type_id,
                    'ad_type_id':ad_type_id,
                    'spot_length_id':spot_length_id,
                    'timeband_id':timeband_id,
                    'rate_id':rate_id,

            })

    @api.one
    @api.depends('ratecard_sin_print_id.rate_id')
    def _get_printratecard_rate(self):
        for  order  in  self:
            print  'order', order
            name  = ''
            outlet_id = ''
            outlet_type_id  =''
            ad_type_id  =''
            spot_length_id  =''
            timeband_id = ''
            rate_id  = ''
            print_ratecard_cost = 0.0
            for  line  in  order.ratecard_sin_print_id:
                print 'timeband' , line.timeband_id.id
                print_ratecard_cost += line.rate_id.rate_amount
                print 'print_ratecard_cost' , print_ratecard_cost
                print 'NAME OF RADIO RATECARD' , line.name
                name = line.name
                outlet_id = line.outlet_id
                outlet_type_id  = line.outlet_type_id
                ad_type_id  = line.ad_type_id
                spot_length_id  =line.spot_length_id
                timeband_id = line.timeband_id
                rate_id  = line.rate_id
            order.update({
                    'print_ratecard_cost':print_ratecard_cost,
                    'name':name,
                    'outlet_id':outlet_id,
                    'outlet_type_id':outlet_type_id,
                    'ad_type_id':ad_type_id,
                    'spot_length_id':spot_length_id,
                    'timeband_id':timeband_id,
                    'rate_id':rate_id,

            })
    @api.one
    @api.depends('ratecard_sin_tv_id.rate_id')
    def _get_tvratecard_rate(self):
        for  order  in  self:
            print  'order', order
            name = ''
            outlet_id = ''
            outlet_type_id  =''
            ad_type_id  =''
            spot_length_id  =''
            timeband_id = ''
            rate_id  = ''
            tv_ratecard_cost = 0.0
            for  line  in  order.ratecard_sin_tv_id:
                print 'timeband' , line.timeband_id.id
                # print 'VAT  RATE' ,line.vat_rate_id.id
                tv_ratecard_cost += line.rate_id.rate_amount
                print 'tv_ratecard_cost' , tv_ratecard_cost
                print 'NAME OF RADIO RATECARD' , line.name
                name = line.name
                outlet_id = line.outlet_id
                outlet_type_id  = line.outlet_type_id
                ad_type_id  = line.ad_type_id
                spot_length_id  =line.spot_length_id
                timeband_id = line.timeband_id
                rate_id  = line.rate_id

            order.update({
                    'tv_ratecard_cost':tv_ratecard_cost,
                    'name':name,
                    'outlet_id':outlet_id,
                    'outlet_type_id':outlet_type_id,
                    'ad_type_id':ad_type_id,
                    'spot_length_id':spot_length_id,
                    'timeband_id':timeband_id,
                    'rate_id':rate_id,
            })

    @api.onchange('radio_ratecard_cost')
    def on_change_radio_ratecard_cost(self):
        print 'RADIO RATECARD COST' ,self.radio_ratecard_cost
        self.list_price =self.radio_ratecard_cost
        print 'RADIO ONCHANGE list_price ' , self.list_price


    @api.onchange('digital_ratecard_cost')
    def on_change_digital_ratecard_cost(self):
        print 'DIGITAL RATECARD COST' ,self.digital_ratecard_cost
        self.list_price = self.digital_ratecard_cost


    @api.onchange('print_ratecard_cost')
    def on_change_print_ratecard_cost(self):
        self.list_price = self.print_ratecard_cost


    @api.onchange('tv_ratecard_cost')
    def on_change_tv_ratecard_cost(self):
        self.list_price = self.tv_ratecard_cost

    @api.onchange('radio_multiple_ratecard_cost')
    def on_change_radio_multiple_ratecard_cost(self):
       self.list_price =self.radio_multiple_ratecard_cost


    

class  timeband(models.Model):
    _name= 'timeband'
    _description = 'Time Band'    

    code  = fields.Char(string='TIMEBAND CODE',store=True,readonly=True)

    _defaults = {

        'code':lambda obj,cr,uid,context:'/TIMEBAND/'
    }

    def  create(self,cr,uid, vals,context=None):
        vals['code'] = self.pool.get('ir.sequence').get(cr,uid,'timeband')
        return super(timeband,self).create(cr,uid,vals,context=context)

    name   = fields.Char(string='Name' , size=64  ,  required=True)
    description = fields.Text('Description', translate=True)  
    hour_from  =  fields.Selection(selection=hour_from, string='HOUR FROM')
   # hour_from  = fields.date(string=' HOUR  FROM' , default=lambda self,cr,uid,context=None: fields.date.context_today(self,cr,uid,context) + " 09:00:00")
    hour_to  =  fields.Selection(selection=hour_to, string='HOUR TO')
    rateclass_code_id  = fields.Many2one('rateclass.code',string='RATECLASS CODE')
    list_position = fields.Selection(selection=list_position, string='LIST POSITION')
    sale_order_line_id = fields.One2many(comodel_name='sale.order.line', inverse_name='timeband_id',string='Timeband')


    
   
    logo = fields.Binary('Logo File')
    
    rate_id  = fields.One2many(comodel_name='rate', inverse_name='timeband_id', 
                              string='RATE')
    ratecard_sin_radio_id = fields.One2many(comodel_name='ratecard.sin.radio', inverse_name='timeband_id', string='Time Bands')
    ratecard_sin_digital_id = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='timeband_id', string='Time Bands')
    ratecard_sin_tv_id = fields.One2many(comodel_name='ratecard.sin.tv', inverse_name='timeband_id', string='Time Bands')
    ratecard_sin_print_id = fields.One2many(comodel_name='ratecard.sin.print', inverse_name='timeband_id', string='Time Bands')
    product_ids = fields.One2many('product.template','timeband_id',string='Time Band',)
    products_count = fields.Integer(string='Number of products', compute='_get_products_count',)
    outlet_id = fields.Many2one('outlet',string='Outlet',help='Select a brand for this Time  Band if it exists',ondelete='restrict')


    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    @api.multi
    def  name_get(self):
        result = []
        for  record in  self:
            if  record.name  and  record.outlet_id:
                result.append((record.id,record.name + '/' + record.code))

        return result

    @api.model
    def  name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or  []
        recs = self.browse()
        if  name :
            recs = self.search([('name' ,'=',name)] + args , limit=limit)
        if  not  recs:
            recs = self.search([('name' ,operator , name)] + args , limit=limit)
        return recs.name_get()


    
class  pages(models.Model):
    _name  = 'pages'
    _description = 'Pages'
    
    name  =  fields.Char(string='NAME' , size=64  , required=True )
    page  = fields.Selection(selection=page_no, string='PAGE')
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    ratecard_sin_digital_id = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='pages_id', 
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
                                string='Outlet Type' ,readonly=True)
    ratecard_sin_radio_id  = fields.One2many(comodel_name='ratecard.sin.radio', inverse_name='outlet_type_id', string='Outlet Type')
    ratecard_sin_tv_id  = fields.One2many(comodel_name='ratecard.sin.tv', inverse_name='outlet_type_id', string='Outlet Type')
    ratecard_sin_print_id  = fields.One2many(comodel_name='ratecard.sin.print', inverse_name='outlet_type_id', string='Outlet Type')
    ratecard_sin_digital_id  = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='outlet_type_id', string='Outlet Type')
    sale_order_line_id = fields.One2many(comodel_name='sale.order.line', inverse_name='outlet_type_id',string='Outlet Type')
    sale_order_id = fields.One2many(comodel_name='sale.order', inverse_name='outlet_type_id',string='Outlet Type')

    ratecard_mul_id = fields.One2many(comodel_name='ratecard.mul', inverse_name='outlet_type_id',string='Outlet Type')
    ratecard_multiples_id = fields.One2many(comodel_name='ratecard.multiples', inverse_name='outlet_type_id',string='Outlet Type')

    
    
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
    #def  _check_name(self,cr,uid,ids,context=None):
        
        #if  context  is  None:
            #context = {}
        #outlet_types = self.browse(cr,uid,ids,context=context)
        #for  outlet_type in  outlet_types:
            #outlet_type.
    _sql_constraints = [
        ('name_uniq','unique(name)','Outlet  Type Must Be Unique!'),
    ]
        
class  digital_location(models.Model):
    _name  =  'digital.location'
    _description = 'Digital  Location'
    
    name  =  fields.Char(string='Digital Location',  size=64  ,  required=True)    
    ratecard_sin_digital_id =fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='digital_location_id', 
                                    string='Digital Location')
    digital_location_id = fields.Many2one(
            'digital.location',
            string='Digital  Location',
            help='Select the  digital  location for this product'
        )        
    location  = fields.Char(string='LOCATION',  size=64  ,  required=True)
    homepage  =  fields.Char(string='HOMEPAGE' , size=64)
    news_page  =  fields.Char(string='NEWS PAGE' , size =64)
    entertainment_page = fields.Char(string='ENTERTAINMENT  HOME  PAGE' , size=64  )
    
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
    ratecard_sin_digital_id = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='digital_type_id' , string='Digital  Type')
    
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
    ratecard_sin_digital_id = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='digital_size_id' ,  string='Digital Size')
    
    
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



class  ratecard_sin_radio(models.Model):
    _name =  'ratecard.sin.radio'
    _description  = 'RATECARD SINGULAR RADIO  '

    code  = fields.Char(string='RADIO SINGULR RATECARD CODE',readonly=True)
    name  =   fields.Char(string='NAME')
    outlet_id = fields.Many2one(comodel_name='outlet', string='Outlet')
    timeband_id  = fields.Many2one(comodel_name='timeband', string='TimeBand')
    pages_id  =   fields.Many2one(comodel_name='pages', string='Pages')
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')
    ad_type_id  = fields.Many2one(comodel_name='ad.type', string='Ad Type')
    vat_rate_id  = fields.Many2one(comodel_name='vat.rate', string='Vat Rate')
    payment_terms_id  = fields.Many2one(comodel_name='payment.terms', string='Payment Terms')
    rateclass_code_id  = fields.Many2one(comodel_name='rateclass.code', string='RateClass Code')
    quote_stage_id  = fields.Many2one(comodel_name='quote.stage', string='Quote Stage')
    spot_length_id  = fields.Many2one(comodel_name='spot.length', string='Spot Length')
    schedule_type_id=fields.Many2one(comodel_name='schedule.type', string='Schedule Type')
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    ratecard_multiple_id = fields.Many2one(comodel_name='ratecard.multiple' , string='RADIO SINGULAR RATECARD')
    rate_id  = fields.Many2one(comodel_name='rate',string='TIMEBAND RATE')
    week_id =fields.Many2one(comodel_name='week',string='TIMEBAND SPOTS')

    week_count = fields.Integer('COUNT WEEK',track_visibility='always',  store=True)
    monday  = fields.Integer(string='MON',track_visibility='always'  ,  store=True)
    tuesday   = fields.Integer(string='TUE',track_visiility='always'  ,  store=True)
    wednesday   = fields.Integer(string='WED',track_visibility='always'  ,  store=True)
    thursday   = fields.Integer(string='THUR',track_visibility='always'  ,  store=True)
    friday   = fields.Integer(string='FRI',track_visibility='always'  ,  store=True)
    saturday   = fields.Integer(string='SAT',track_visibility='always'  ,  store=True)
    sunday   = fields.Integer(string='SUN',track_visibility='always'  ,  store=True)
    noofweeks = fields.Integer(string="WEEKS",default=1 , store=True,   track_visibility='always')
    #compute='_noofweeks',
    spot_total  = fields.Integer( compute='_compute_totalspots' , string='SPOTS' ,track_visibility='always' ,readonly=True ,  store=True)
    allocate_subtotal = fields.Integer(compute='_compute_spotrateweektotal', string='SPOTS WEEKS TOTAL', readonly=True, store=True)

    @api.one
    @api.depends('sunday' , 'monday','tuesday' ,'wednesday'  , 'thursday'  ,'friday'  , 'saturday')
    def _compute_totalspots(self):
        for order in self:
            for  line  in  order:
                spottotal  = line.sunday + line.monday + line.tuesday+ line.wednesday+line.thursday + line.friday + line.saturday
            self.update({'spot_total':spottotal})

    @api.one
    @api.depends('sunday' , 'monday','tuesday' ,'wednesday'  , 'thursday'  ,'friday'  , 'saturday', 'noofweeks')
    def _compute_spotrateweektotal(self):
        for order in self:
            for  line  in  order:
                week_spot_total  = line.sunday + line.monday + line.tuesday+ line.wednesday+line.thursday + line.friday + line.saturday
                subtotal = week_spot_total *  line.noofweeks
            self.update({'allocate_subtotal':subtotal})
    rates_total =  fields.Float(string='RATES TOTAL', compute='_getrate', store=True, readonly=True, track_visibility='always')

    @api.one
    @api.depends('rate_id.rate_amount')
    def _getrate(self):
        for  order  in  self:
            print  'order', order
            rates_total = 0.0
            for  line  in  order:
                print 'rates_total' , line.rate_id.rate_amount
                rates_total += line.rate_id.rate_amount
                print 'rates_total >>> ' , rates_total

            order.update({
                    'rates_total':rates_total,

            })


    compute_total =  fields.Float(string='COMPUTE RATE ALLOCATION TOTAL', compute='_compute_rate', store=True, readonly=True, track_visibility='always')

    @api.one
    @api.depends('rate_id.rate_amount','allocate_subtotal')
    def _compute_rate(self):
        for  order  in  self:
            print  'order', order
            compute_total = 0.0
            for  line  in  order:
                print '>>>> rates_total >>>>> ' , line.rate_id.rate_amount
                print '>>>> line.allocate_subtotal >>>> ',line.allocate_subtotal
                compute_total += line.rate_id.rate_amount * line.allocate_subtotal
                print '>>>>>> compute_total >>>>> ' , compute_total

            order.update({
                    'compute_total':compute_total,

            })



    _defaults = {

        'code':lambda obj,cr,uid,context:'/RADIO/SINGULAR/RATECARD/'
    }

    def  create(self,cr,uid, vals,context=None):
        vals['code'] = self.pool.get('ir.sequence').get(cr,uid,'ratecard.sin.radio')
        return super(ratecard_sin_radio,self).create(cr,uid,vals,context=context)
        
    def onchange_outlet(self,cr,uid,ids,outlet_id):
        result = {'value':{'outlet_type_id':False}}
        if  outlet_id:
            outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
            print  outlet 
            result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
        return result    
    product_ids = fields.One2many('product.template','ratecard_sin_radio_id',string='RateCard Type  Singular ',)
    ratecard_mul_id = fields.Many2one( 'ratecard.mul',string='RateCard')      
    
    products_count = fields.Integer( string='Number of products',compute='_get_products_count',)
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)
        
    #def  on_change_outlet(self,cr,uid,ids,outlet_id,context=None):
        #val = {}
        #if  not  outlet_id:
            #return {}
        #outlet_obj = self.pool.get('outlet')
        #outlet_data = outlet_obj.browse(cr,uid,outlet_id,context=context)
        #val.update({'outlet_type_id': [ outlet_type_.id for  outlet_type_ in  outlet_data.outlet_types_ids]})
        #return {'value': val}

class  ratecard_multiples(models.Model):
    _name='ratecard.multiples'
    name = fields.Char(string='RateCard  ')
    code  = fields.Char(string='MULTIPLE RATECARD CODE')
    sinmul_ratecard_id = fields.Char(string='SINMUL')
    outlet_id = fields.Many2one(comodel_name='outlet', string='Outlet')
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')
    ratecard_multiple_id  = fields.Many2many(comodel_name='ratecard.multiple',  relation='ratecard_multiples_rel',
                                             column1='ratecard_multiples_id', column2='ratecard_multiple_id' , string='MULTIPLE RATECARD')    
    description = fields.Text('Description', translate=True)
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many('product.template','ratecard_multiples_id', string='RateCard Multiple',)
    products_count = fields.Integer(string='Number of products',compute='_get_products_count',)
    state = fields.Selection([
        ('draft', 'Multiple RateCard  Draft'),
        ('sent', 'Multiple RateCard READY'),
        ('sale', 'MULTIPLE  RATECARD  FINAL'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    total_amount= fields.Integer( string='TOTAL Ksh:',store=True, readonly=True, compute='_get_multiple_total_ratecard_amount_rate', track_visibility='always')

    @api.one
    @api.depends('ratecard_multiple_id.taxed_amount')
    def _get_multiple_total_ratecard_amount_rate(self):
        for  order  in  self:
            print  'MULTIPLES RATECARD PRINT ', order
            total_amount = 0.0
            for  line  in  order.ratecard_multiple_id:
                for lineitems in  line:
                     # print 'timeband' , line.timeband_id.id
                    # print 'VAT  RATE' ,line.vat_rate_id.id

                    print  'MULTIPLES RATECARD TAXED  AMOUNT' , lineitems.taxed_amount
                    total_amount += lineitems.taxed_amount

                    print 'radio_ratecard_cost' , total_amount
            order.update({
                    'total_amount':total_amount,

            })

    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    def onchange_outlet(self,cr,uid,ids,outlet_id):
                result = {'value':{'outlet_type_id':False}}
                if  outlet_id:
                    outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
                    print  outlet
                    result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
                return result

    @api.multi
    def button_dummy(self):
        return True
    @api.multi
    def action_draft(self):
        self.filtered(lambda s: s.state in ['cancel', 'sent']).write({'state': 'draft'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})
    @api.multi
    def action_done(self):
        self.write({'state': 'done'})

    
class  ratecard_multiple(models.Model):
    #pudb.set_trace()
    _name = 'ratecard.multiple'
    #_inherits = {'ratecard.sin.radio':'ratecard_sin_radio_id'}
   # _inherits = {'ratecard.sinmul':'ratecard_sinmul_id'}
    name = fields.Char(string='Multiple RateCard Product  Name ' ,required=True)
    code  = fields.Char(string='Multiple RateCard Code ',readonly=True)
    scheduled_for  = fields.Integer(string='SCHEDULED FOR' , default=1)
    min_weeks = fields.Integer(string="MINIMUM NO OF WEEKS" , default=1 )    
    max_weeks = fields.Integer(string="Maximum NO OF WEEKS" , default=1, track_visibility='always' ,store=True)

    description = fields.Text('Description', translate=True)
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many('product.template','ratecard_multiple_id', string='RateCard Multiple',)

    products_count = fields.Integer(string='Number of products',compute='_get_products_count',)

    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    @api.model
    def _default_note(self):
        return self.env.user.company_id.sale_note

    @api.one
    @api.depends('scheduled_for')
    def  _compute_maxweeks(self):
        self.max_weeks = False
        for  line  in  self:
            mx  = line.scheduled_for * 1 
        self.update({'max_weeks':mx})     

    @api.one
    @api.constrains('min_weeks','max_weeks')
    def  _check_max_weeks(self):
        if  self.min_weeks > self.max_weeks :
            raise exceptions.ValidationError("No Of Minimum  Weeks  cannot be  greater than Maximum  No of Weeks")   
        
    @api.one
    @api.constrains('scheduled_for','min_weeks')
    def  _check_min_weeks(self):
        if  self.scheduled_for > self.min_weeks :
            raise exceptions.ValidationError("Minimum  must  be  greater or  equal to  Scheduled  For ")  
    
    
    allocate_spot = fields.Boolean(string='Allocate')
    state = fields.Selection([
        ('draft', 'Multiple RateCard  Draft'),
        ('sent', 'Multiple RateCard READY'),
        ('sale', 'MULTIPLE  RATECARD  FINAL'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')  
    
    validity_date = fields.Date(string='Product Date', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},required=True)
    
    
    
        
    note = fields.Text('Terms and conditions', default=_default_note)
    
    amount_untaxed = fields.Integer(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    amount_tax = fields.Integer(string='Taxes', store=True, readonly=True, compute='_compute_taxedamount', track_visibility='always')
    tax_id = fields.Many2many('account.tax', string='Taxes')
    discount = fields.Float(string='Discount (%)',store=True , digits_compute=dp.get_precision('Discount'), track_visibility='onchange' )    
 
    amount_total = fields.Integer(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')  
    total_spot = fields.Integer(string='SPOT  TOTAL', store=True, readonly=True, compute='_amount_all', track_visibility='always')    
    
    
    
    @api.depends('discount','allocate_schedule.price_subtotal')
    def _discount(self):
        """
        """
        for order in self:
            discount = 0
            print 'order' , order            
            amount_untaxed = amount_tax = 0.0
            for line in order.allocate_schedule:
                if  line.price_subtotal  ==False:
                    raise exceptions.Warning("Kindly Update Discount ,Its  empty ") 
                elif  line.price_subtotal  !=False:
                    discount +=discount
            order.update({
                'discount': discount,
            })    
    
    #@api.onchange('discount','amount_untaxed')
    #def  discount_update_amount_untaxed(self):
        #for  order  in self:
            #if  order.discount == False:
                #raise exceptions.Warning("Kindly Update Discount ,Its  empty ")                
            #if order.discount != 0 :
                #print  'amount_untaxed  '  , order.amount_untaxed
                #print  'discount ' , order.discount
                #order.amount_untaxed  -=  orderamount_untaxed* (1 - (order.discount ) / 100.0)                
            
    #company_id = fields.Many2one(comodel='res.company', string='Company', store=True, readonly=True)
    subtotal_discounted = fields.Integer(string='Total After  Discount', store=True, readonly=True, compute='_compute_discountamount', track_visibility='always')
    fiscal_position_id = fields.Many2one('account.fiscal.position', oldname='fiscal_position', string='Fiscal Position')  
    #vat_rate  = fields.Many2one(comodel_name='vat.rate', string='TAX  RATE (%)',digits_compute=dp.get_precision('TAX RATE'), default=0.0)
    vat_rate  = fields.Float(string='TAX  RATE (%)',digits_compute=dp.get_precision('TAX RATE'), default=17, track_visibility='onchange'  )    
    taxed_amount  = fields.Integer( string='TOTAL Ksh:',store=True, readonly=True, compute='_compute_taxedamount', track_visibility='always')
    multiple_ratecard_id  = fields.Many2many(comodel_name='ratecard.sin.radio', relation='ratecard_mul_ratecard_sin_rel', 
                                                column1='ratecard_mul_id', 
                                                column2='ratecard_sin_radio_id', 
                                                string='RATECARDS')   
    # allocate_multiple_id  =  fields.Many2many(comodel_name='ratecard.mul' ,relation='ratecard_mul_ratecard_sin_rel',
    #                                           column1='multiple_ratecard_id' , column2='week_id' ,string='ALLOCATE RATECARD',required=True)
    #
    ratecard_sin_radio_id = fields.One2many(comodel_name='ratecard.sin.radio', 
                                              inverse_name='ratecard_multiple_id', 
                                              string='RADIO SINGULAR RATECARD',required=True)
    
    
    allocate_schedule = fields.Many2many(comodel_name='week', relation='ratecard_multiple_week_rel',
                                         column1='ratecard_multiple_id', column2='week_id',
                                         track_visibility='onchange', string='ALLOCATE SPOTS',required=True)
    #Updated  now  from _amount_all method
    allocate_schedule_count = fields.Integer(string='WEEKS ALLOCATED',compute='_get_allocate_schedule_count', track_visibility='always' ,readonly=True , store=True)

    @api.one
    @api.depends('allocate_schedule_count', 'allocate_schedule')
    def _get_allocate_schedule_count(self):
        for  order  in  self:
            print  'order', order
            allocate_schedule_count = 0
            for  line  in  order.allocate_schedule:
                print '_get_allocate_schedule_count ALLOCATE SCHEDULE COUNTS' , len(self.allocate_schedule)
                allocate_schedule_count = len(self.allocate_schedule)
                print '_get_allocate_schedule_count ALLOCATED SCHEDULE COUNTS ARE' , allocate_schedule_count
                print '_get_allocate_schedule_count allocate_schedule_count' , allocate_schedule_count

            order.update({
                    'allocate_schedule_count':allocate_schedule_count,

            })

    @api.onchange('allocate_schedule')
    def _onchange_allocate_schedule(self):
        print 'we entered the allocate_schedule count'
        self.allocate_schedule = self.allocate_schedule
    #     # for  order in  self:
    #     #     print 'allocate_schedule count' , order
    #     #     for line  in  order:
    #     #         # line.name
    #     #         print  'Count line  items' , line
    #     #         print 'line.name' , line

    multiple_ratecard_id_count = fields.Integer(string='SINGULAR RATECARDS SELECTED',compute='_get_multiple_ratecard_id_count_count', track_visibility='always' ,store=True)

    @api.onchange('multiple_ratecard_id')
    def _onchange_multiple_ratecard(self):
        print 'we entered the multiple ratecard many2many'
        for  order in  self:
            print 'Order Name' , order
            for line  in  order:
                # line.name
                print 'line.name' , line

    @api.onchange('allocate_schedule')
    def _onchange_allocate_schedule(self):
        print 'refreshed allocate_schedule'
        for  order in  self:
            print 'allocate_schedule' , order
            for line  in  order:
                print 'line.name' , line



    # @api.one
    # @api.depends('allocate_schedule' ,'allocate_schedule_count')
    # def _get_allocate_schedule_count(self):
    #     for  order in  self:
    #         order.allocate_schedule_count = len(order.allocate_schedule)
    #         print 'allocate_schedule_counts' , order.allocate_schedule_count
    #     order.update({
    #             'allocate_schedule_count':order.allocate_schedule_count,
    #
    #         })

    @api.one
    @api.depends('multiple_ratecard_id','multiple_ratecard_id_count')
    def _get_multiple_ratecard_id_count_count(self):
        for  order in  self:
            order.multiple_ratecard_id_count = len(order.multiple_ratecard_id)
            print 'multiple_ratecard_id_count' , order.multiple_ratecard_id_count
        order.update({
                'multiple_ratecard_id_count':order.multiple_ratecard_id_count,

            })


    # partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always')
    # @api.one
    # @api.constrains('allocate_schedule_count','multiple_ratecard_id_count')
    # def _check_lineitems(self):
    #     for  line  in self:
    #         if  line.allocate_schedule_count > line.multiple_ratecard_id_count :
    #             print  'ALLOCATE  SCHEDULE  COUNT  IS  GREATER' ,  line.allocate_schedule_count ,line.multiple_ratecard_id_count
    #             raise exceptions.ValidationError("WEEKS ALLOCATED MUST BE EQUAL TO SELECTED SINGULAR RATECARDS")
    #         elif  line.allocate_schedule_count < line.multiple_ratecard_id_count:
    #             print 'ALLOCATED SPOTS  GREATER THAN SINGULAR RATECARDS SELECTED' , line.multiple_ratecard_id_count , line.allocate_schedule_count
    #             raise exceptions.ValidationError("ALLOCATED SPOTS  GREATER THAN SINGULAR RATECARDS SELECTED")
    #         elif   line.multiple_ratecard_id_count > line.allocate_schedule_count :
    #             print  'SINGULAR RATECARDS SELECTED ARE GREATER THAN  ALLOCATED SPOTS ' ,  line.allocate_schedule_count ,line.multiple_ratecard_id_count
    #             raise exceptions.ValidationError("SINGULAR RATECARDS SELECTED ARE GREATER THAN  ALLOCATED SPOTS PLEASE CORRECT TO MATCH")
    #         elif  line.multiple_ratecard_id_count < line.allocate_schedule_count:
    #             print 'SINGULAR RATECARDS SELECTED ARE LESS THAN  ALLOCATED SPOTS' , line.multiple_ratecard_id_count , line.allocate_schedule_count
    #             raise exceptions.ValidationError("SINGULAR RATECARDS SELECTED ARE LESS THAN  ALLOCATED SPOTS")
    #         elif line.allocate_schedule_count == line.multiple_ratecard_id_count :
    #             print  'SUCCESSFULL , THEY ARE  EQUAL' ,  line.allocate_schedule_count , line.multiple_ratecard_id_count
    #             pass

    # @api.onchange('allocate_schedule_count', 'multiple_ratecard_id_count')
    # @api.multi
    # def _onchange_price(self):
    #     error_message = 'SINGULAR RATECARDS LINES SELECTED MUST MATCH ALLOCATED SPOTS LINES '
    #     res = {}
    #     for line in  self:
    #         print 'allocate_schedule_count VALUES' , line.allocate_schedule_count
    #         print 'multiple_ratecard_id_count VALUES' , line.multiple_ratecard_id_count
    #         if  (line.multiple_ratecard_id_count > 0) and (line.multiple_ratecard_id_count != line.allocate_schedule_count):
    #             print 'line.multiple_ratecard_id_count > 0  ::: allocate_schedule_count VALUES' , line.allocate_schedule_count
    #             print ' line.multiple_ratecard_id_count > 0 ::: multiple_ratecard_id_count VALUES' , line.multiple_ratecard_id_count
    #             error_message = 'KINDLY ALLOCATE SPOT'
    #             res = {'warning': {
    #             'title': 'YOU HAVE ADDED A  SINGULAR RATECARD LINE' ,
    #             'message': error_message,
    #         }
    #             }
    #         elif (line.allocate_schedule_count > 0) and   (line.allocate_schedule_count != line.multiple_ratecard_id_count):
    #             print 'line.allocate_schedule_count > 0  ::: allocate_schedule_count VALUES' , line.allocate_schedule_count
    #             print ' line.allocate_schedule_count > 0 ::: multiple_ratecard_id_count VALUES' , line.multiple_ratecard_id_count
    #             error_message = 'KINDLY ALLOCATE SINGULAR RATECARD'
    #             res = {'warning': {
    #             'title': 'YOU HAVE JUST ADDED AN ALLOCATION SPOT ' ,
    #             'message': error_message,
    #         }
    #             }
    #         elif line.allocate_schedule_count != line.multiple_ratecard_id_count:
    #             print 'line.allocate_schedule_count != line.multiple_ratecard_id_count ::: allocate_schedule_count VALUES' , line.allocate_schedule_count
    #             print ' line.allocate_schedule_count != line.multiple_ratecard_id_count  ::: multiple_ratecard_id_count VALUES' , line.multiple_ratecard_id_count
    #             error_message = 'SINGULAR RATECARDS LINES SELECTED MUST MATCH ALLOCATED SPOTS LINES TO PROCEED'
    #             res = {'warning': {
    #             'title': 'SINGULAR RATECARDS LINES SELECTED MUST MATCH ALLOCATED SPOTS LINES' ,
    #             'message': error_message,
    #         }
    #             }
    #     return res
        # Can optionally return a warning and domains
        # return {
        #     'warning': {
        #         'title': 'SELECTED SINGULAR RATECARDS MUST  HAVE  CORRESPONDING ALLOCATED SPOTS AND  VICE VERSA' ,
        #         'message': error_message,
        #     }
        # }

    _defaults = {
        'code':lambda obj,cr,uid,context:'/'
    }

    rate_amount = fields.Float(string='RATES TOTAL Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')

    # @api.one
    # @api.depends('multiple_ratecard_id.compute_total')
    # def _getrate(self):
    #     for  order  in  self:
    #         print  'order', order
    #         rate_amount = 0.0
    #         for  lineitems in  order:
    #             for line  in lineitems.multiple_ratecard_id:
    #                     print '>>>>> line.timeband_id.id' , line.timeband_id.id
    #                     print '>>>>> line.vat_rate_id.id' ,line.vat_rate_id.id
    #                     rate_amount += line.compute_total
    #                     print '>>>> multiple_ratecard_id.compute_total >>>>> ' , rate_amount
    #         order.update({
    #                 'rate_amount':rate_amount,
    #
    #         })




    @api.one
    @api.depends('amount_untaxed','discount' ,'vat_rate','amount_tax','rate_amount')
    def _compute_taxedamount(self):
        for order in self:
            for  line  in  order:
                subtotaldiscounted= line.amount_untaxed* (1 - (line.discount or 0.0) / 100.0)   
                subtotaltaxed  = subtotaldiscounted * (1- (line.vat_rate or 0.0)/100.0)
                amount_tax  = subtotaldiscounted  - subtotaltaxed
                aftertax  = subtotaldiscounted +amount_tax  
                
            line.update({
                'subtotal_discounted':subtotaldiscounted,
                'taxed_amount':aftertax,
                'amount_tax':amount_tax,
            })         
    
    @api.one
    @api.depends('amount_untaxed','discount' )    
    def _compute_discountamount(self):
        for order in self:
            for  line  in  order:
                subtotaldiscounted= line.amount_untaxed* (1 - (line.discount or 0.0) / 100.0)                
            line.update({'subtotal_discounted':subtotaldiscounted})        
    #_defaults = {
        #'code': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'object.object'),
    #} 
    #def  create(self,cr,uid,vals,context=None):
        #if  not  vals['allocate_schedule'][0][2]:
            #raise Exception('MISSING ALLOCATED  SPOTS ')
        #created_hc  = []    self.update({'spot_total':total})  
        #for  id  in
    @api.multi
    @api.depends('allocate_schedule_count','scheduled_for','rate_amount','discount','multiple_ratecard_id.noofweeks','multiple_ratecard_id.compute_total','multiple_ratecard_id.spot_total')
    def _amount_all(self):
        """
        Compute the total amounts of the Weeks  and  Rate.
        """
        for order in self:
            print 'order' , order            
            amount_untaxed = amount_tax = 0.0
            total_spot = 0
            compute_total = 0
            update_noofweeks = 0
            allocate_schedule_count = 0
            print  'rate_amount ', order.rate_amount
            print 'amount  untaxed' , amount_untaxed
            for  orderitems  in  order:
                for lineitems in orderitems:
                    for  line in  lineitems.multiple_ratecard_id:
                        print '=======> order.scheduled_for =====> ' ,  order.scheduled_for
                        print 'WEEKS', line.noofweeks
                        if  order.scheduled_for !=0 :
                            print 'order.scheduled_for' , order.scheduled_for
                            update_noofweeks =  order.scheduled_for
                            print  'update_noofweeks ' , update_noofweeks
                        print 'line.noofweeks<><><><>>>' , update_noofweeks
                        print 'spot_total'
                        print  'order.spot_total == ' , line.spot_total
                        total_spot += line.spot_total
                        print 'out  of  spot_total'
                        print 'ALLOCATE SCHEDULE COUNTS' , len(self.allocate_schedule)
                        allocate_schedule_count = len(self.allocate_schedule)
                        print 'ALLOCATED SCHEDULE COUNTS ARE' , allocate_schedule_count
                        print 'ORDER TIMES COUNTS' , len(order)
                        # amount_untaxed += order.rate_amount * line.compute_total
                        compute_total +=line.compute_total
                        print '>>>> Compute Total ==== ' ,compute_total
                        amount_untaxed += line.compute_total
                        print  'Amount  untaxed == ' , line.compute_total
                        amount_tax = 1*1
                        print  'amount_tax == ' , amount_tax
                    if  (order.amount_untaxed >  (0 or  0.00))and  (order.discount == (0 or  0.00)):
                        print  'untaxed' , order.amount_untaxed
                #raise exceptions.ValidationError("Please  Update Discount ! must  be  greater  than  0.00 ") 
            order.update({
                'total_spot':total_spot,
                'rate_amount':compute_total,
                'scheduled_for':update_noofweeks,
                # 'allocate_schedule_count': allocate_schedule_count,
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })    
    @api.multi
    def button_dummy(self):
        return True   
    @api.multi
    def action_draft(self):
        self.filtered(lambda s: s.state in ['cancel', 'sent']).write({'state': 'draft'})
    
    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})
    @api.multi
    def action_done(self):
        self.write({'state': 'done'})    
    
    def  _create_allocate_schedule(self):
        self.allocate_schedule = self.env['ratecard.multiple'].create({
            'name' : self.name,
            'padding':5,
            'company_id':self.company_id.id,
        })
    def  create(self,cr,uid, vals,context=None):
        rec  = super(ratecard_multiple,self).create(vals)
        if  not  rec.allow_schedule:
            rec._create_allocate_schedule()
        return  rec
    
    def  create(self,cr,uid, vals,context=None):
        vals['code'] = self.pool.get('ir.sequence').get(cr,uid,'ratecard.multiple')
        return super(ratecard_multiple,self).create(cr,uid,vals,context=context)
    #not working  but  compiles --> weird  -- investigate further  
    #def create(self, cr, uid, vals, context=None):
        #if not vals:
            #vals = {}
        #if context is None:
            #context = {}
        #vals['code'] = self.pool.get('ir.sequence').get(cr, uid, 'object.object')
        
        #return super(ratecard_multiple, self).create(cr, uid, vals, context=context)
    #def  onchange_allocateschedule(self,cr,uids,ids,allocate_schedule):
        #res = {} 
        #for  record  in  self.browse(cr,uid,ids,context=None, )
        
        
    
    def onchange_outlet(self,cr,uid,ids,outlet_id):
        result = {'value':{'outlet_type_id':False}}
        if  outlet_id:
            outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
            print  outlet 
            result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
        return result        
        
    #def name_get(self,cr,uid,ids,context=None):
        #result = {}
        #for record in self.browse(cr,uid,ids,context=context):
            #result[record.id] = record.name + " " + str(record.ratecard_sin_radio_id.id)
    
        #return result.items()    
        
#relation
class  ratecard_mul_ratecard_sin_rel(models.Model):
    _name = 'ratecard.mul.ratecard.sin.rel'
    week_id  = fields.Many2one(comodel='week',string='NO OF WEEKS')

class ratecard_multiple_week_rel(models.Model):
    _name = 'ratecard.multiple.week.rel'
    ratecard_multiple_id = fields.Many2one(comodel_name='ratecard.multiple' , string='NO OF WEEKS')

    @api.onchange('ratecard_multiple_id')
    def _onchange_methods(self):
        count = 0
        for order in self:
            print  'can  we  get order.ratecard_multiple_id'
            print len(order.ratecard_multiple_id)
            count = len(order.ratecard_multiple_id)
    
    
class  ratecard_sin_print(models.Model):
    _name =  'ratecard.sin.print'
    _description  = 'RATECARD SINGULAR PRINT  '
    
    name  =   fields.Char(string='NAME')
    outlet_id = fields.Many2one(comodel_name='outlet', string='Outlet')
    timeband_id  = fields.Many2one(comodel_name='timeband', string='TimeBand')
    pages_id  =   fields.Many2one(comodel_name='pages', string='Pages')
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')
    
    def onchange_outlet(self,cr,uid,ids,outlet_id):
        result = {'value':{'outlet_type_id':False}}
        if  outlet_id:
            outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
            print  outlet 
            result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
        return result
    ad_type_id  = fields.Many2one(comodel_name='ad.type', string='Ad Type')
    payment_terms_id  = fields.Many2one(comodel_name='payment.terms', string='Payment Terms')
    rateclass_code_id  = fields.Many2one(comodel_name='rateclass.code', string='RateClass Code')
    quote_stage_id  = fields.Many2one(comodel_name='quote.stage', string='Quote Stage')
    schedule_type_id=fields.Many2one(comodel_name='schedule.type', string='Schedule Type')
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
          'product.template',
          'ratecard_sin_print_id',
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

    code  = fields.Char(string='PRINT RATECARD CODE',readonly=True)

    rate_id  = fields.Many2one(comodel_name='rate',string='TIMEBAND RATE')

    _defaults = {

        'code':lambda obj,cr,uid,context:'PRINT/RATECARD/'
    }

    def  create(self,cr,uid, vals,context=None):
        vals['code'] = self.pool.get('ir.sequence').get(cr,uid,'ratecard.sin.print')
        return super(ratecard_sin_print,self).create(cr,uid,vals,context=context)

    def onchange_outlet(self,cr,uid,ids,outlet_id):
        result = {'value':{'outlet_type_id':False}}
        if  outlet_id:
            outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
            print  outlet
            result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
        return result
    
        
class  ratecard_sin_digital(models.Model):
    _name =  'ratecard.sin.digital'
    _description  = 'RATECARD SINGULAR DIGITAL '
    
    name  =   fields.Char(string='NAME')
    outlet_id = fields.Many2one(comodel_name='outlet', string='Outlet')
    timeband_id  = fields.Many2one(comodel_name='timeband', string='TimeBand')
    pages_id  =   fields.Many2one(comodel_name='pages', string='Pages')
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')
    
    def onchange_outlet(self,cr,uid,ids,outlet_id):
        result = {'value':{'outlet_type_id':False}}
        if  outlet_id:
            outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
            print  outlet 
            result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
        return result
    
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

    product_ids = fields.One2many('product.template','ratecard_sin_digital_id', string='RateCard Type  Singular ',)
    ratecard_mul_id = fields.Many2one( 'ratecard.mul',string='RateCard')      
    code  = fields.Char(string='DIGITAL RATECARD CODE',readonly=True)

    rate_id  = fields.Many2one(comodel_name='rate',string='TIMEBAND RATE')

    _defaults = {

        'code':lambda obj,cr,uid,context:'DIGITAL/RATECARD/'
    }

    def  create(self,cr,uid, vals,context=None):
        vals['code'] = self.pool.get('ir.sequence').get(cr,uid,'ratecard.sin.digital')
        return super(ratecard_sin_digital,self).create(cr,uid,vals,context=context)

    def onchange_outlet(self,cr,uid,ids,outlet_id):
        result = {'value':{'outlet_type_id':False}}
        if  outlet_id:
            outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
            print  outlet
            result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
        return result
    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)
        
    #def  on_change_outlet(self,cr,uid,ids,outlet_id,context=None):
        #val = {}
        #if  not  outlet_id:
            #return {}
        #outlet_obj = self.pool.get('outlet')
        #outlet_data = outlet_obj.browse(cr,uid,outlet_id,context=context)
        #val.update({'outlet_type_id': [ outlet_type_.id for  outlet_type_ in  outlet_data.outlet_types_ids]})
        #return {'value': val}

    
        
class  ratecard_sin_tv(models.Model):
    _name =  'ratecard.sin.tv'
    _description  = 'RATECARD SINGULAR TV'
    
    name  =   fields.Char(string='NAME')
    outlet_id = fields.Many2one(comodel_name='outlet', string='Outlet')
    timeband_id  = fields.Many2one(comodel_name='timeband', string='TimeBand')
    pages_id  =   fields.Many2one(comodel_name='pages', string='Pages')
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')
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
          'ratecard_sin_tv_id',
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
        
    code  = fields.Char(string='TV RATECARD CODE',readonly=True)

    rate_id  = fields.Many2one(comodel_name='rate',string='TIMEBAND RATE')

    _defaults = {

        'code':lambda obj,cr,uid,context:'TV/RATECARD/'
    }

    def  create(self,cr,uid, vals,context=None):
        vals['code'] = self.pool.get('ir.sequence').get(cr,uid,'ratecard.sin.tv')
        return super(ratecard_sin_tv,self).create(cr,uid,vals,context=context)

    def onchange_outlet(self,cr,uid,ids,outlet_id):
        result = {'value':{'outlet_type_id':False}}
        if  outlet_id:
            outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
            print  outlet
            result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
        return result

class  ratecard_mul_rel(models.Model):
    _name  =  'ratecard.mul.rel'
    
    ratecard_left_id  = fields.Many2one('ratecard.mul')
    ratecard_right_id = fields.Many2one('ratecard.mul','Relation')
    allocate_id  = fields.Many2one(comodel_name='week', string='ALLOCATE SPOTS')
    week_ids = fields.Many2many(comodel_name='week', relation='ratecard_mul_rel_week_rel', column1='ratecard_mul.rel_id', column2='week_id', string='ALLOCATE SPOTS')    
    code_left_right = fields.Integer(string="CODE")
         
    
    
    

    
class  ratecard_mul(models.Model):
    _name = 'ratecard.mul'
    _description = 'RATECARD TYPE  MULTIPLE'
    
    m2m_right2left = fields.Many2many('ratecard.mul','ratecard_mul_rel','ratecard_right_id','ratecard_left_id')
    m2m_left2right  = fields.Many2many('ratecard.mul','ratecard_mul_rel' , 'ratecard_left_id', 'ratecard_right_id')
    o2m_left_ids = fields.One2many('ratecard.mul.rel','ratecard_left_id')
    name  =  fields.Char(string='RATECARD MULTIPLE')
    ratecard_sin_radio_id  =  fields.One2many(comodel_name='ratecard.sin.radio',inverse_name='ratecard_mul_id',
                                string='MULTIPLES')
    multiple_ratecard_id  = fields.Many2many(comodel_name='ratecard.sin.radio', relation='ratecard_mul_ratecard_sin_rel', 
                                            column1='ratecard_mul_id', 
                                            column2='ratecard_sin_radio_id', 
                                            string='RATECARDS')
    # sale_order_id = fields.One2many(comodel_name='sale.order', inverse_name='ratecard_mul_id',string='MULTIPLE RATECARD')
    outlet_id = fields.Many2one(comodel_name='outlet', string='Outlet')
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')    
    scheduled_for  = fields.Integer(string='SCHEDULED FOR' , default=1)
    min_weeks = fields.Integer(string="MINIMUM NO OF WEEKS" , default=1 )    
    max_weeks = fields.Integer(string="Maximum NO OF WEEKS" , default=1)    #compute='_compute_max_weeks' , store=True
    total = fields.Char(string="TOTAL" )     
    x = fields.Char(string="x" )     
    y = fields.Char(string="y" )     
    test_day = fields.Char(string='Test Day')
    noof_spots_id = fields.Many2one(comodel_name='noof.spots', string='NO  OF  SPOTS')
    week_id  = fields.Many2one(comodel_name='week', string='ALLOCATE SPOTS')
    
    week_ids = fields.Many2many(comodel_name='week', relation='ratecard_mul_week_rel', column1='ratecard_mul_id', column2='week_id', string='ALLOCATE SPOTS')
    spot = fields.Integer(string='SPOTS',default='0')  
    from_date  = fields.Date(string="FROM DATE")
    order_month  = fields.Char(string='MONTH')
    order_day  = fields.Char(string='DAY')
    order_year  = fields.Char(string='YEAR')
    compute_weeks = fields.Integer(string='ALLOCATED WEEKS')
    
    
    to_date  = fields.Date(string="TO DATE")
    
    _defaults={
        
        'order_month' : lambda *a: time.strftime('%m'),
        'order_day' : lambda *a: time.strftime('%d'),
        'order_year' : lambda *a: time.strftime('%Y'),            
    
    }
    
    #@api.one
    #@api.depends('from_date','to_date','compute_weeks')
    #def  _compute_weeks(self):
        #self.compute_weeks =False
        #for  line  in  self:
            #cal_weeks  = 
            
   
    
    @api.one
    @api.depends('sunday' , 'monday','tuesday' ,'wednesday'  , 'thursday'  ,'friday'  , 'saturday')    
    def _compute_spots(self):
        self.spot_total = False
        for  line  in  self:
            total  = line.sunday + line.monday + line.tuesday+ line.wednesday+line.thursday + line.friday + line.saturday
        self.update({'spot_total':total})    
        
    @api.one
    @api.depends('scheduled_for')
    def  _compute_max_weeks(self):
        self.max_weeks = False
        for  line  in  self:
            mx  = line.scheduled_for * 1 
        self.update({'max_weeks':mx})
        
        
    @api.one
    @api.constrains('min_weeks','max_weeks')
    def  _check_max_weeks(self):
        if  self.min_weeks > self.max_weeks :
            raise exceptions.ValidationError("No Of Minimum  Weeks  cannot be  greater than Maximum  No of Weeks")    
        
    @api.one
    @api.constrains('scheduled_for','min_weeks')
    def  _check_min_weeks(self):
        if  self.scheduled_for > self.min_weeks :
            raise exceptions.ValidationError("Minimum  must  be  greater or  equal to  Scheduled  For ")
    
    
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

    
    def onchange_outlet(self,cr,uid,ids,outlet_id):
                result = {'value':{'outlet_type_id':False}}
                if  outlet_id:
                    outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
                    print  outlet 
                    result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
                return result       
    

     

class  ad_type(models.Model):
    _name  =  'ad.type'
    
    name  =  fields.Char(string='AD  TYPE' , size=64  , required=True)
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='OUTLET TYPE')
    rate_card_type  = fields.Selection(selection=[('0','SINGULAR'),('1','MULTIPLE')], string='RATECARD TYPE')
    ratecard_sin_radio_id = fields.One2many(comodel_name='ratecard.sin.radio', inverse_name='ad_type_id' , string="Ad Type")
    ratecard_sin_digital_id = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='ad_type_id' , string="Ad Type")
    ratecard_sin_print_id = fields.One2many(comodel_name='ratecard.sin.print', inverse_name='ad_type_id' , string="Ad Type")
    ratecard_sin_tv_id = fields.One2many(comodel_name='ratecard.sin.tv', inverse_name='ad_type_id' , string="Ad Type")
    outlet_id = fields.Many2one('outlet',string='Outlet',help='Select a brand for this  Ad Type if it exists',ondelete='restrict' )
    sale_order_line_id = fields.One2many(comodel_name='sale.order.line', inverse_name='ad_type_id',string='AD TYPE')

    #name  = fields.One2many(comodel_name='rate', inverse_name='name', string='NAME')
 
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many('product.template','ad_type_id',string='Ad Type',)

    products_count = fields.Integer(string='Number of products',compute='_get_products_count',)

    @api.onchange('name','outlet_type_id','rate_card_type')
    def _onchange_multiple_ratecard_type(self):

        # if self.name !=False:
        #     for record in self:
        #     #or 'CLASSIFIED' or 'classified' or 'PROMOTION' or 'promotion':
        #         print 'AD TYPE NAME' , record.name
        #         if record.name in record.rate_card_type:
        #             print record.name
        #             record.rate_card_type == 'MULTIPLE'

        if self.name ==False:
            raise exceptions.Warning(_('AD TYPE NAME HAS BE FILLED'))




    # def onchange_outlet(self,cr,uid,ids,outlet_id):
    #     result = {'value':{'outlet_type_id':False}}
    #     if  outlet_id:
    #         outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
    #         print  outlet
    #         result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
    #     return result
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)




class  var_rate(models.Model):
    _name  = 'vat.rate'
    _description = 'VAT  RATE (%)'
    
    name  = fields.Char(string='VAR RATE (%)')
    rate = fields.Float(string='VAR RATE (%)',store=True , digits_compute=dp.get_precision('VAT RATE (%)'), track_visibility='onchange' )

    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many('product.template','vat_rate_id',string='VAR RATE (%)',)

    products_count = fields.Integer(string='Number of products',compute='_get_products_count',)
    
    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one('outlet',string='Outlet',help='Select a brand for this  VAT  RATE if it exists',ondelete='restrict')
    ratecard_multiple_id  = fields.One2many('ratecard.multiple','vat_rate',string='VAT RATE')


    
    
class  payment_terms(models.Model):
    _name  =  'payment.terms'
    _description = 'PAYMENT  TERMS'
    
    name   = fields.Selection(selection=payment_type,string='CASH/CHEQUE' , help  = 'NETT 30    for  30 days  ')
    days  =   fields.Selection(selection=payment_duration, string="DAYS")
    ratecard_sin_radio_id = fields.One2many(comodel_name='ratecard.sin.radio', inverse_name='payment_terms_id' , string='Payment Terms')
    ratecard_sin_digital_id = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='payment_terms_id' , string='Payment Terms')
    ratecard_sin_print_id = fields.One2many(comodel_name='ratecard.sin.print', inverse_name='payment_terms_id' , string='Payment Terms')
    ratecard_sin_tv_id = fields.One2many(comodel_name='ratecard.sin.tv', inverse_name='payment_terms_id' , string='Payment Terms')
    
    
    
    
    
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
    
    code = fields.Selection(selection=[('FIXED','FIXED'),('MOVEABLE','MOVEABLE') ,('RUN OF STATION','RUN OF STATION')], string='RATECLASS CODE')
    name  =  fields.Selection(selection=[('FIXED','FIXED'),('MOVEABLE','MOVEABLE') ,('RUN OF STATION','RUN OF STATION')], string='RATECLASS CODE')
    rate_class_type  = fields.Selection(selection=[('0','Advertisement is  fixed and  cannot be  moved'),
                                                   ('2','Advertisement CAN BE  MOVED WITHIN TIMEBAND'),
                                                   ('3','Scheduled to run  within the overall time parameters inidcated subject to  preemption'
                                                        'for other  business at the discretion of the  STATION')], string='TYPE')

    ratecard_digital_id = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='rateclass_code_id' , string='RateClass Code')
    ratecard_radio_id = fields.One2many(comodel_name='ratecard.sin.radio', inverse_name='rateclass_code_id' , string='RateClass Code')
    ratecard_print_id = fields.One2many(comodel_name='ratecard.sin.print', inverse_name='rateclass_code_id' , string='RateClass Code')
    ratecard_tv_id = fields.One2many(comodel_name='ratecard.sin.tv', inverse_name='rateclass_code_id' , string='RateClass Code')
    timeband_id  = fields.One2many(comodel_name='timeband' , inverse_name='rateclass_code_id' ,string='RATECLASS CODE')
    quote_stage  = fields.One2many(comodel_name='quote.stage' , inverse_name='rateclass_code_id' ,string='RATECLASS CODE')


    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many('product.template','rateclass_code_id',string='RATECLASS  CODE',)
    products_count = fields.Integer( string='Number of products',compute='_get_products_count',)

    # @api.multi
    # def  name_get(self):
    #     result = []
    #     for  record in  self:
    #         if  record.name  and  record.code:
    #             result.append((record.id,record.name + '/' + record.code + '/' + record.rate_class_type))
    #     return result
    #
    # @api.model
    # def  name_search(self, name='', args=None, operator='ilike', limit=100):
    #     args = args or  []
    #     recs = self.browse()
    #     if  name :
    #         recs = self.search([('name' ,'=',name)] + args , limit=limit)
    #     if  not  recs:
    #         recs = self.search([('name' ,operator , name)] + args , limit=limit)
    #     return recs.name_get()

    @api.one
    @api.depends('product_ids')
    def _get_products_count(self):
        self.products_count = len(self.product_ids)

    
    outlet_id = fields.Many2one('outlet',string='Outlet',help='Select a brand for this  RATECLASS  CODE if it exists', ondelete='restrict')


    
class  quote_stage(models.Model):
    _name  =  'quote.stage'
    _decription  =  'QUOTE STAGE'
    
    name  =fields.Char(string='Name')
    rateclass_code_id = fields.Many2one('rateclass.code',string='RATECLASS CODE')
    quote_stage =  fields.Selection([('draft' , 'DRAFT'),
                                     ('negotiation' , 'NEGOTIATION'),
                                     ('delivered' , 'DELIVERED') , 
                                     ('closed_accepted' , 'CLOSED  ACCEPTED'),
                                     ('closed_lost' , 'CLOSED LOST'),
                                     ('closed_dead' , 'CLOSED DEAD'),
    ], string='QUOTE STAGE')
    
    description = fields.Text('Description', translate=True)          
    logo = fields.Binary('Logo File')
    ratecard_radio_id = fields.One2many(comodel_name='ratecard.sin.radio', inverse_name='quote_stage_id' , string='Quote Stage')
    ratecard_sin_print_id = fields.One2many(comodel_name='ratecard.sin.print', inverse_name='quote_stage_id' , string='Quote Stage')
    ratecard_sin_digital_id = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='quote_stage_id' , string='Quote Stage')
    ratecard_sin_tv_id = fields.One2many(comodel_name='ratecard.sin.tv', inverse_name='quote_stage_id' , string='Quote Stage')
    
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
        ('BANDED','BANDED'),
        ('FIXED','FIXED')
        ],
                            string='Schedule Name')
    schedule_type = fields.Selection(selection=schedule_types, string='Schedule ')
    ratecard_sin_radio_id = fields.One2many(comodel_name='ratecard.sin.radio', inverse_name='schedule_type_id' , string='Schedule Type')
    ratecard_sin_print_id = fields.One2many(comodel_name='ratecard.sin.print', inverse_name='schedule_type_id' , string='Schedule Type')
    ratecard_sin_digital_id = fields.One2many(comodel_name='ratecard.sin.digital', inverse_name='schedule_type_id' , string='Schedule Type')
    ratecard_sin_tv_id = fields.One2many(comodel_name='ratecard.sin.tv', inverse_name='schedule_type_id' , string='Schedule Type')
    
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
    ratecard_mul_id  = fields.One2many(comodel_name='ratecard.mul', inverse_name='noof_spots_id', string='WEEK')
    
    
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
    noof_spots_id = fields.Many2one('noof.spots',string='WEEKLY SPOTS',help='Select a weekly  spot for this product')
    
class  rate(models.Model):
    _name  = 'rate'
    name = fields.Char(string='RATE OUTLET TIMEBAND NAME' , required=True , help='RATE NAME  IS  BASED ON CHOSEN AUTOFIELD TIMEBAND OUTLET ')
    code  = fields.Char(string='RATE CODE',readonly=True)
    timeband_id = fields.Many2one('timeband', string='TIMEBAND',help='Select a timeband  for  this  rate if it exists',ondelete='cascade')
    rate_amount = fields.Float(string='RATE AMOUNT (Ksh::)' , required=True,store=True , digits_compute=dp.get_precision('RATE AMOUNT'), track_visibility='onchange' )
    description = fields.Text('Description',required=True, translate=True)
    # outlet_id = fields.Char(string='OUTLET' , store=True, track_visibility='onchange')
    outlet_id = fields.Many2one('outlet',string='Outlet', track_visibility='onchange' ,help='Select a brand for this Time  Band if it exists',ondelete='restrict')

    # outlet_id = fields.Many2one(comodel_name='outlet',string='OUTLET' , store=True, track_visibility='onchange')
    ratecard_sin_radio_id = fields.One2many(comodel_name='ratecard.sin.radio',inverse_name='rate_id',string='TIMEBAND RATE')
    ratecard_sin_digital_id = fields.One2many(comodel_name='ratecard.sin.digital',inverse_name='rate_id',string='TIMEBAND RATE')
    ratecard_sin_print_id = fields.One2many(comodel_name='ratecard.sin.print',inverse_name='rate_id',string='TIMEBAND RATE')
    ratecard_sin_tv_id = fields.One2many(comodel_name='ratecard.sin.tv',inverse_name='rate_id',string='TIMEBAND RATE')
    sale_order_line_id = fields.One2many(comodel_name='sale.order.line', inverse_name='rate_id',string='TIMEBAND RATE')
    product_ids = fields.One2many('product.template','rate_id',string='Outlet Products',)



    # def onchange_timeband(self,cr,uid,ids,timeband_id):
    #     result = {'value':{'outlet_id':False}}
    #     if timeband_id:
    #         timeband = self.pool.get('timeband').browse(cr,uid,timeband_id)
    #         print  timeband
    #         result['value'] = {'outlet_id':timeband.outlet_id.id}
    #         return result
    #
    def onchange_timeband(self,cr,uid,ids,timeband_id):
        result = {'value':{'outlet_id':False}}
        if  timeband_id:
            timeband = self.pool.get('timeband').browse(cr,uid,timeband_id)
            print  timeband
            result['value'] = {'outlet_id':timeband.outlet_id.id}
        return result

    _defaults = {

        'code':lambda obj,cr,uid,context:'/TIMEBAND/RATE'
    }

    @api.onchange('rate_amount','timeband_id')
    def _onchange_rate_amount(self):
        if  self.timeband_id != False and self.rate_amount ==False:
            raise exceptions.ValidationError('Please Update Rate Amount')

    def  create(self,cr,uid, vals,context=None):
        vals['code'] = self.pool.get('ir.sequence').get(cr,uid,'rate')
        return super(rate,self).create(cr,uid,vals,context=context)

    @api.multi
    def  name_get(self):
        result = []
        for  record in  self:
            print 'record name ' , record.rate_amount
            # if  record.name  and  record.code:
            #     result.append((record.id,record.name + '/' + record.code))
            if  record.rate_amount  or  record.id:
                result.append((record.id,record.name+ str('Ksh::')+str(record.rate_amount)))
        return result

    @api.model
    def  name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or  []
        recs = self.browse()
        if  name :
            recs = self.search([('name' ,'=',name)] + args , limit=limit)
        if  not  recs:
            recs = self.search([('name' ,operator , name)] + args , limit=limit)
        return recs.name_get()

    def  onchange_timeband_outlet(self,cr,uid,ids,timeband_id,context=None):
        value={'outlet_id':False}
        if  timeband_id:
            timeband = self.pool.get('timeband').browse(cr,uid,timeband_id)
            value['outlet_id'] = timeband.outlet_id.name
        return {'value':value}

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    product_name= fields.Char(string='Product Name')
    noofweeks = fields.Integer(string='NO OF WEEKS')
    singular_ratecards = fields.Boolean(string='SINGULAR RATECARDS')
    multiple_ratecards = fields.Boolean(string='MULTIPLE RATECARDS')
    scheduled_start_date = fields.Date(string='SCHEDULED START DATE')
    multiple_noofweeks = fields.Integer(string='MULTIPLE NO OF WEEKS')
    multiple_scheduled_start_date = fields.Date(string='MULTIPLE SCHEDULED START DATE')
    partner_id = fields.Many2one(comodel_name='res.partner' ,string='CLIENT CONTACT', domain=[('is_company', '=', False)])
    outlet_id = fields.Many2one(comodel_name='outlet', string='Outlet')
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')


    _defaults = {
        'singular_ratecards':0,
        'multiple_ratecards':0,
        'active': True,
    }


    
    def onchange_outlet(self,cr,uid,ids,outlet_id):
            result = {'value':{'outlet_type_id':False}}
            if  outlet_id:
                outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
                print  outlet 
                result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
            return result    


    partner_order_id = fields.Many2one('res.partner', 'Sales Person', domain=[('is_company', '=', False)])
    

    @api.multi
    def onchange_partner_id(self, partner_id):
        vals = super(SaleOrder, self).onchange_partner_id(partner_id)
        if partner_id:
            partner = self.env['res.partner'].search([('id', '=', partner_id)])
            for child in partner.child_ids:
                if child.type == 'contact':
                    vals['value']['partner_order_id'] = child.id
                    return vals
            if partner.child_ids:
                vals['value']['partner_order_id'] = partner.child_ids[0].id
        return vals

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # outlet = fields.Char(string='OUTLET')
    # outlet_type = fields.Char( string='OUTLET TYPE' , readonly=True, states={'draft': [('readonly', False)]})
    outlet_id = fields.Many2one(comodel_name='outlet', string='Outlet')
    outlet_type_id  = fields.Many2one(comodel_name='outlet.type', string='Outlet Type')
    ad_type_id = fields.Many2one(comodel_name='ad.type', string='AD TYPE')
    spot_length_id = fields.Many2one(comodel_name='spot.length', string='LENGTH')
    timeband_id = fields.Many2one(comodel_name='timeband', string='TIMEBAND')
    rate_id = fields.Many2one(comodel_name='rate', string='RATE')

    saturday   = fields.Integer(string='SAT')
    monday  = fields.Integer(string='MON')
    tuesday   = fields.Integer(string='TUE')
    wednesday   = fields.Integer(string='WED')
    thursday   = fields.Integer(string='THUR')
    friday   = fields.Integer(string='FRI')
    sunday   = fields.Integer(string='SUN')

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        context = context or {}
        lang = lang or context.get('lang',False)
        if not  partner_id:
            raise exceptions.Warning(_('No Customer Defined!'), _('Before choosing a product,\n select a customer in the sales form.'))
        warning = {}
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        context = {'lang': lang, 'partner_id': partner_id}
        if partner_id:
            lang = partner_obj.browse(cr, uid, partner_id).lang
        context_partner = {'lang': lang, 'partner_id': partner_id}

        if not product:
            return {'value': {'th_weight': 0,
                'product_uos_qty': qty}, 'domain': {'product_uom': [],
                   'product_uos': []}}
        if not date_order:
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        result = {}
        warning_msgs = ''
        product_obj = product_obj.browse(cr, uid, product, context=context_partner) # product_obj definition
        #ADD  FIELDS HERE  IN PRODUCT TEMPLATE
        result['outlet_id'] = product_obj.outlet_id
        result['outlet_type_id'] = product_obj.outlet_type_id
        result['ad_type_id'] = product_obj.ad_type_id
        result['spot_length_id'] = product_obj.spot_length_id
        result['timeband_id'] = product_obj.timeband_id
        result['rate_id'] = product_obj.rate_id

        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if product_obj.uom_id.category_id.id != uom2.category_id.id:
                uom = False
        if uos:
            if product_obj.uos_id:
                uos2 = product_uom_obj.browse(cr, uid, uos)
                if product_obj.uos_id.category_id.id != uos2.category_id.id:
                    uos = False
            else:
                uos = False
        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
        if update_tax: #The quantity only have changed
            result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)

        if not flag:
            result['name'] = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
            if product_obj.description_sale:
                result['name'] += '\n'+product_obj.description_sale
        domain = {}
        if (not uom) and (not uos):
            result['product_uom'] = product_obj.uom_id.id
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
                uos_category_id = product_obj.uos_id.category_id.id
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
                uos_category_id = False
            result['th_weight'] = qty * product_obj.weight
            domain = {'product_uom':
                        [('category_id', '=', product_obj.uom_id.category_id.id)],
                        'product_uos':
                        [('category_id', '=', uos_category_id)]}
        elif uos and not uom: # only happens if uom is False
            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
            result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
            result['th_weight'] = result['product_uom_qty'] * product_obj.weight
        elif uom: # whether uos is set or not
            default_uom = product_obj.uom_id and product_obj.uom_id.id
            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
            result['th_weight'] = q * product_obj.weight        # Round the quantity up

        if not uom2:
            uom2 = product_obj.uom_id
        # get unit price

        if not pricelist:
            warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
                    'Please set one before choosing a product.')
            warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
        else:
            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                    product, qty or 1.0, partner_id, {
                        'uom': uom or result.get('product_uom'),
                        'date': date_order,
                        })[pricelist]
            if price is False:
                warn_msg = _("Cannot find a pricelist line matching this product and quantity.\n"
                        "You have to change either the product, the quantity or the pricelist.")

                warning_msgs += _("No valid pricelist line found ! :") + warn_msg +"\n\n"
            else:
                result.update({'price_unit': price})
        if warning_msgs:
            warning = {
                       'title': _('Configuration Error!'),
                       'message' : warning_msgs
                    }
        return {'value': result, 'domain': domain, 'warning': warning}


    def onchange_outlet(self,cr,uid,ids,outlet_id):
        result = {'value':{'outlet_type_id':False}}
        if  outlet_id:
            outlet = self.pool.get('outlet').browse(cr,uid,outlet_id)
            print  outlet
            result['value'] = {'outlet_type_id':outlet.outlet_type_id.id}
        return result





