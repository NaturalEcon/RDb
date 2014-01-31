from RDb.descriptivemodels import *
"""
Created on Tue Jan 28 12:44:21 2014

@author: acumen
"""

def new_survey(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = SurveyValueForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            resource = form.cleaned_data['resource']
            actor = form.cleaned_data['actor']
            process = form.cleaned_data['process']
            date = form.cleaned_data['date']
            source = form.cleaned_data['source']
            valuetype = form.cleaned_data['valuetype']
            value = form.cleaned_data['value']
            description = form.cleaned_data['description']
            relationship = form.cleaned_data['relationship']
            reference = form.cleaned_data['reference']
    
            NESurveyValue(resource=resource,actor=actor,process=process,date=date, \
                source=source,valuetype=valuetype,value=value,description=description, \
                relationship=relationship,reference=reference)
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })