# -*- encoding: utf-8 -*-
###############################################################################
# #                                                                           #                                                             #
###############################################################################
{
    'name': 'Radio  Africa  Defaults Manager',
    'version': '0.1',
    'category': 'Product',
    'summary': 'Add radio africa defaults to products',
       'author': 'DANIEL  MWAI',
       'license': 'AGPL-3',
    'depends': ['product','sale'],
    'data': [




        #Entry

        'views/rag_defaults_outlet.xml',
        'views/rag_defaults_outlet_type.xml',
        'views/rag_defaults_singulars_quotations.xml',
        # 'views/rag_defaults_multiples_quotations.xml',
        'views/product_template.xml',
        'views/res_partner.xml',


        # 'views/sale_view.xml',
        'views/ratecard_rnd.xml',
        'views/generic_request.xml',
        'views/opinion.xml',
        #NO OF SPOTS  WEEKLY MANAGEMENT
        'views/rag_defaults_week.xml',


        #RATECARDS SCHEDULING
        'views/ratecards_scheduler/ratecards_scheduler.xml',

            #SCHEDULING
        'views/ratecards_schedules/one_week_schedule.xml',
        'views/ratecards_schedules/two_weeks_schedule.xml',
        'views/ratecards_schedules/three_weeks_schedule.xml',
        'views/ratecards_schedules/four_weeks_schedule.xml',
        'views/ratecards_schedules/passed_context.xml',

          #MANY2MANY RELATION DONT  ADD  THIS for  now
        # 'views/partner.xml',

        'views/ratecard_singulars/ratecard_singulars.xml',



        #
        'views/rag_defaults_timeband.xml',
        'views/rag_defaults_pages.xml',
        #
        'views/rag_defaults_rate.xml',        
        
          'views/rag_defaults_spot_length.xml',
          'views/rag_defaults_noof_spots.xml',
          #
          'views/rag_defaults_schedule_type.xml',
          
          
        'views/rag_defaults_ad_size.xml',
        'views/rag_defaults_ad_type.xml',
        
        'views/rag_defaults_digital_location.xml',  
        'views/rag_defaults_digital_size.xml',  
        'views/rag_defaults_digital_type.xml',  
        
        'views/rag_defaults_vat_rate.xml',
        'views/rag_defaults_payment_terms.xml',  
        
        'views/rag_defaults_rateclass_code.xml',
        'views/rag_defaults_ratecard_radio.xml',
        'views/rag_defaults_ratecard_digital.xml',
        'views/rag_defaults_ratecard_print.xml',
        'views/rag_defaults_ratecard_tv.xml',
        
        #MUTIPLES
        # 'views/rag_defaults_ratecard_mul.xml',
        'views/rag_defaults_ratecard_multiple.xml', 
        'views/rag_defaults_ratecard_multiples.xml', 
        'views/rag_defaults_quote_stage.xml',




        #REPORTS
        # 'views/ratecard_multiple/report_view.xml',
        
        
        
        
        
        
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
