# -*- coding: utf-8 -*-
"""
types.py: Contains type variables for RDb.
Created on Sun Feb  2 21:45:37 2014

:const rclasses: Classes of NEResource.
:const dtypes: Types of NEDependencies.
|A "forward" dependency for resource R is a resource which depends on R.
|A "backward" dependency for resource R is a resource on which R depends.
|An "inter" dependency is either a co-product of R, or a member of a renewable cycle
:const infotypes: Types of information.
|Info types are types of values derived from or describing a value type.
:const valuetypes: Types of data. Incomplete.
:const ptypes: Types of processes.  Far from complete.
:const atypes: Types of actors.  Far from complete.
:const ctypes: Types of sources that can be cited.
:author: acumen
"""



rclasses = (
    ('R','Resource'),('M','Material'),('P','Product'),('S','Service'),('D','Data')
)

dtypes = (('f','Forward'),('b','Backward'),('i','Inter'))

infotypes = ( 
    ('u','Mean'),    
    ('m','Median'),
    ('o','Mode'),
    ('a','Maximum'),
    ('i','Minimum'),
    ('s','Standard deviation of'),
    ('E','Expected value of'),
    ('V','Variance of'),
    ('M','Moment'),
    ('^','Estimated'),
    ('e','Error of'),
    ('w','Skew of'),
    ('k','Kurtosis of'),
    ('p','Significance level of'),
    ('*','Optimal'),
    ('x','Safety'),
)
# Valuetype can be one of the following:
#########################################
# Mass-based
#  K,S,E,D: Resource mass quantity, in kg
#       K: resources known (R,M)
#       S: resources in reserve (R) or inventory (M,P)
#       E: reserve and allocated resources (R,M) or products in use (P)
#       D: material requirements (R,M) or product demand (P). The latter requires user input.
#########################################
# Rate-based
#   dK,dS,dE,dD: Changes in  in kg per year 
#       dK: rate of discovery (R,M)
#       dS: replenishment rate (RR) or discovery rate (NRR)
#       dE: extraction rate (R) or production rate (M,P)
#       dD: rate of change in demand
#   dEG,dEE,dEX,dEM: Changes in kWh/kg per year
#       dEE: rate of change in embodied energy
#       dPE: rate of change in process energy
#       dEX: rate of change in exergy
#       dEM: rate of change in emergy
#########################################
# Energy-based
#  EG, EE, EX, EM: Energy input requirement for the resource in kWh/kg
#       EE: embodied energy content
#       PE: process energy
#       EX: exergy value
#       EM: emergy value
#########################################
value_types = (
    ('Mass', (
        ('K','Known'),
        ('S','In Reserve'),
        ('E','Exploited'),
        ('D','Demanded'),
        )
    ),
    ('Rate', (
        ('dK','Discovery Rate'),
        ('dS','Reserve Rate'),
        ('dE','Exploitation Rate'),
        ('dD','Rate of Change in Demand'),
        )
    ),
    ('Operational', (
        ('NCY','Cycle Number'),
        ('TCY','Cycle Length'),
        ('PRIO','Priority'),
        )    
    ),
    ('Energy', (
        ('EE','Embodied Energy'),
        ('PE','Process Energy'),
        ('EX','Exergy'),
        ('EM','Emergy'),
        ('FE','Feedstock Energy')
        )
    ),
    ('Service', (
        ('UT','Total Uptime'),
        ('UC','Current Uptime'),
        ('STA','Service Time Available'),
        ('STU','Service Time Used'),
        ('SAR','Arrival Rate'),
        ('SSR','Service Rate'),
        )
    ),
    ('Reliability', (
        ('TBF','Time Before Failure'),
        ('MFOP','Maintenance-Free Operating Period'),
        )
    ),
    ('Other', (
        ('%Y','Percent Yield'),
        ('PR','Property Value'),
        ('EC','Embodied Carbon'),
        ('ECe','Embodied Carbon Equivalent'),
        ('$','Price'),
        ('W','Weight')
        )
    ),
)
econstates = (
    ('Growth', (
        ('G','Growing'),
        ('S','Steady-State'),
        ('D','Declining'),
        )
    ),
    ('Fulfillment', (
        ('NRM','Normal'),
        ('SCR','Scarcity'),
        ('MRG','Emergency'),
        )     
    )
)
ptypes = (
    ('Mass', (
        ('mco','Concentration'),
        ('mdi','Dispersion'),
        ('mxp','Transport'),
        ('mre','Reduction'),
        ('mac','Accretion'),
        ('mmi','Milling'),
        ('mgr','Grinding'),
        ('mcu','Cutting'),
        ('mbe','Bending'),
        ('mfo','Forming'),
        ('mag','Aggregation'),
        ('msm','Smelting'),        
        ('mds','Dissolution'),
        ('mas','Assembling'),
        ('mal','Alloying'),
        ('mus','Disassembling'),
        ('mrp','Repairing'),
        ('mrc','Recycling'),
        ('mrx','Reaction'),
        )
    ),
    ('Energy', (   
        ('egc','Conversion'),
        ('egs','Storage'),
        ('ego','Concentration'),
        ('ege','Entropic'),
        ('egf','Flow'),
        )
    ),
    ('Time', (
        ('ter','Erosion'),
        )
    ),
    ('Actor',(
        ('asc','State Change'),
        )
    ),
)
atypes = ( ('org','Organization'),('ogn','Organism'),('sys','System'),('hom','Person') )

ctypes = (
    ('J','Journal article'),('R','Report'),('P','Personal communication'),
    ('B','Book'),('M','Memo')
)