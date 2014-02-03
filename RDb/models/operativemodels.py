from django.db import models
from commonmodels import *
from basemodels import *
from types import rclasses
from datetime import timedelta
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
cycle_length = timedelta(days=7)
prio_min = 119
prio_min_name = 'lx'
prio_max = -20
prio_max_name = 'rt'
__prio_order = 1
if prio_min > prio_max: __prio_order *= -1
PRIO_levels = range(prio_min,prio_max+1,__prio_order)
PRIO_names = [prio_max_name]+map(lambda x: str(x),range(prio_min+1,prio_max,__prio_order))+[prio_min_name]
PRIOS = tuple(zip(PRIO_levels,PRIO_names))

class NECycle(VALUE):
    """
    NECycle: One cycle in the operational kernel.
    :param cycle_number: The number in the sequence of cycle_length time periods since the start of the kernel.  Also the primary key.
    :param cycle_start: The DateTime start of this cycle.
    """
    cycle_number = models.AutoField(primary_key=True)
    cycle_start = models.DateTimeField(auto_now_add=True)
    
    def get_cycle_end(self):
        return self.cycle_start + cycle_length
        
        
class NEResouceRequestQueue(DESCRIPTION, VALUE):
    """
    NEResourceRequestQueue: 
    :param resource: The resource being requested.
    :param request_cycle: The cycle during which the request was placed.
    :param PRIO:   The priority of the resource.
    """
    resource = models.ForeignKey(NEResource,related_name='rsc_requests')
    request_cycle = models.ForeignKey(NECycle,related_name='rsc_requests_for_cycle')
    PRIO   = models.IntegerField(choices=PRIOS)
    
    class Meta:
        verbose_name='Resource'

class NEResourceInstance(NEOBJECT, DESCRIPTION):
    """
    NEResourceInstance: An NEResource that has actually been allocated, and whose component materials count towards exploitation (E) figures.
    :param source: Where the instance comes from, such as the mine, forest, factory, or other via.
    """
    source = models.CharField(max_length=64,default='Earth')
    surveys = ResourceSurveyManager()
    rclass = models.CharField(max_length=1,choices=rclasses)
    
    class Meta:
        verbose_name='Resource Instance'
        
    
class NESemaphore(ABOUT):
    """
    NESemaphore: A description of a semaphore for an NEOBJECT.
    :param semaphore_max: The total number of locks available for this resource.
    :param semaphore_now: The number of locks currently available for this resource.
    :param semaphore_exp: The time (in seconds) after which a lock will expire.
    """
    semaphore_max = models.PositiveIntegerField()
    semaphore_now = models.PositiveIntegerField()
    semaphore_exp = models.PositiveIntegerField()
    
    
class NESemaphoreLock(models.Model):
    """
    NESemaphoreLock: A record of who is currently holding a semaphore lock.
    :param lock_held: Whether the lock is held (True) or free (False)
    :param lock_for: The semaphore that this lock belongs to.
    :param held_by: The actor that is holding this lock.
    """
    lock_held = models.BooleanField()
    lock_for = models.ForeignKey(NESemaphore,related_name='locks')
    held_by = models.ForeignKey('NEActor',related_name='locks_held')
    
    def take(self,lock_taker):
        if self.lock_held == True:
            return 0
        else:
            self.lock_held = True
            self.held_by = lock_taker
            return -1
        
    def release(self):
        if self.lock_held == True:
            self.lock_held = False
            return 1
        else:
            return 0
            

class NEServiceRequestQueue(DESCRIPTION, VALUE):
    """
    NEResourceRequestQueue: 
    :param resource: The resource being requested.
    :param request_cycle: The cycle during which the request was placed
    """
    svc_semaphore = models.ForeignKey(NESemaphore,related_name='svc_requests')
    request_cycle = models.ForeignKey(NECycle,related_name='svc_requests_for_cycle')
    
    def get_cycle_end(self):
        return self.cycle_start + cycle_length