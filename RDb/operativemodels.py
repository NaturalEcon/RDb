from django.db import models
from commonmodels import *
"""
RDb.operativemodels: Models for the operative half of RDb.
Created on Fri Jan 31 12:30:16 2014

:param prio_min: The lowest priority level.
:param prio_min_name: The string representation of the lowest priority level.
:param prio_max: The highest priority level.
:param prio_max_name: The string representation of the highest priority level.
:param prio_order: Ordinarily set to 1 or -1, can be increased to skip numbers in the PRIO module.
:const PRIOS: The list of monoids in the PRIO module, defined by the above parameters.
:author: acumen
"""
prio_min = 119
prio_min_name = 'lx'
prio_max = -20
prio_max_name = 'rt'
prio_order = 1
if prio_min > prio_max: prio_order *= -1
PRIOS = range(prio_min,prio_max+1,prio_order)
    
class NEResource(NEOBJECT,DESCRIPTION):
    """
    NEResource: Analogous to a class of resource, such as a model of product.
    :param std_quantum: The standard number of units this resource is measured in.  The default is 1.0.
    :param std_unit: The SI unit for the standard quantum.  The default is kilograms.
    :param PRIO:   The priority of the resource.
    """
    std_quantum = models.FloatField(default=1.0)
    std_unit = models.CharField(max_length=10,default='kg')
    PRIO   = models.IntegerField(choices=PRIOS)
    
    class Meta:
        verbose_name='Resource'
        
class NEResourceInstance(NEOBJECT, DESCRIPTION):
    """
    NEResourceInstance: An NEResource that has actually been allocated, and whose component materials count towards exploitation (E) figures.
    :param source: Where the instance comes from, such as the mine, forest, factory, or other via.
    :param emergy: The emergy content of this instance, if available.
    :param exergy: The exergy content of this instance, if available.
    """
    source = models.CharField(max_length=64,default='Earth')
    emergy = models.FloatField(null=True,blank=True)
    exergy = models.FloatField(null=True,blank=True)
    uptime = models.IntegerField()
    
class NESemaphore(ABOUT):
    """
    NESemaphore: A table of semaphores for resource instances, to determine whether or not they are in use and by whom.
    :param semaphore_max: The number of simultaneous users available for this resource.
    :param semaphore_now: The number of slots currently available for this resource.
    :param semaphore_exp: The time (in seconds) after which the oldest mutex will expire.
    :param semaphore_first: A foreign key to the first actor to decrement the semaphore.
    :param semaphore_will_expire: The time that the first actor will lose control of its mutex.
    """
    semaphore_max = models.PositiveIntegerField()
    semaphore_now = models.PositiveIntegerField()
    semaphore_exp = models.PositiveIntegerField()
    semaphore_first = models.ForeignKey('NEActor',blank=True,null=True)
    semaphore_will_expire = models.DateTimeField(blank=True,null=True)