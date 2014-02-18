

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import Context, Template, RequestContext
from django.template.loader import get_template
from django.template.response import TemplateResponse
import core.datatables as datatables

from .forms import ProductionTaskForm, ProductionTaskCreateCloneForm, ProductionTaskUpdateForm
from .models import ProductionTask

def task_details(request, rid=None):
   if rid:
       try:
           req = ProductionTask.objects.get(id=rid)
           form = ProductionTaskForm(instance=req)
       except:
           return HttpResponseRedirect('/')
   else:
       return HttpResponseRedirect('/')

   return render(request, 'task/_form.html', {
       'active_app' : 'task',
       'pre_form_text' : 'ProductionTask details with ID = %s' % rid,
       'form': form,
       'parent_template' : 'task/_index.html',
   })

def task_clone(request, rid=None):
   if request.method == 'POST':
       form = ProductionTaskCreateCloneForm(request.POST)
       if form.is_valid():
          # Process the data in form.cleaned_data
           req = ProductionTask(**form.cleaned_data)
           req.save()
           return HttpResponseRedirect('/task/task/%s' % req.id) # Redirect after POST
   else:
       try:
           values = ProductionTask.objects.values().get(id=rid)
       except:
           return HttpResponseRedirect('/')
       del values['id']
       form = ProductionTaskCreateCloneForm(values)

   return render(request, 'task/_form.html', {
       'active_app' : 'task',
       'pre_form_text' : 'Clonning of ProductionTask with ID = %s' % rid,
       'form': form,
       'submit_url': 'task:task_clone',
       'url_args'  : rid,
       'parent_template' : 'task/_index.html',
   })

def task_update(request, rid=None):
   if request.method == 'POST':
       try:
           req = ProductionTask.objects.get(id=rid)
           form = ProductionTaskUpdateForm(request.POST, instance=req) # A form bound to the POST data
       except:
           return HttpResponseRedirect('/')
       if form.is_valid():
          # Process the data in form.cleaned_data
           req = ProductionTask(**form.cleaned_data)
           req.save()
           return HttpResponseRedirect('/task/task/%s' % req.id) # Redirect after POST
   else:
       try:
           req = ProductionTask.objects.get(id=rid)
           form = ProductionTaskUpdateForm(instance=req)
       except:
           return HttpResponseRedirect('/')
   return render(request, 'task/_form.html', {
       'active_app' : 'task',
       'pre_form_text' : 'Updating of ProductionTask with ID = %s' % rid,
       'form': form,
       'submit_url': 'task:task_update',
       'url_args': rid,
       'parent_template' : 'task/_index.html',
   })

def task_create(request):
   if request.method == 'POST': # If the form has been submitted...
       form = ProductionTaskCreateCloneForm(request.POST) # A form bound to the POST data
       if form.is_valid(): # All validation rules pass
           # Process the data in form.cleaned_data
           req = ProductionTask(**form.cleaned_data)
           req.save()
           return HttpResponseRedirect('/task/trequest/%s' % req.id) # Redirect after POST
   else:
       form = ProductionTaskCreateCloneForm() # An unbound form
   return render(request, 'task/_form.html', {
       'active_app' : 'task',
       'pre_form_text' : 'Create ProductionTask',
       'form': form,
       'submit_url': 'task:task_create',
       'parent_template' : 'task/_index.html',
   })



class ProductionTaskTable(datatables.DataTable):

    id = datatables.Column(
        label='ID',
        )

    step = datatables.Column(
        label='StepEx',
        model_field='step__id'
        )


    request = datatables.Column(
        label='Request',
        model_field='request__reqid'
        )

    parent_id = datatables.Column(
        label='Parent id',
        )

    name = datatables.Column(
        label='Name',
        )

    project = datatables.Column(
        label='Project',
        )

    status = datatables.Column(
        label='Status',
        )


    class Meta:
        model = ProductionTask
        bSort = True
        bPaginate = True
        bJQueryUI = True

        sScrollX = '100%'
        sScrollY = '25em'
        bScrollCollapse = True

        aaSorting = [[0, "desc"]]
        aLengthMenu = [[10, 50, 100, -1], [10, 50, 1000, "All"]]
        iDisplayLength = 10
        fnRowCallback =  """
                        function( nRow, aData, iDisplayIndex, iDisplayIndexFull )
                        {
                            $('td:eq(0)', nRow).html('<a href="/task/task/'+aData[0]+'/">'+aData[0]+'</a>&nbsp;&nbsp;'+
                                                     '<span style="float: right;" ><a href="/task/task_update/'+aData[0]+'/">Update</a>&nbsp;'+
                                                     '<a href="/task/task_clone/'+aData[0]+'/">Clone</a></span>'
                            );
                            $('td:eq(1)', nRow).html('<a href="/task/stepex/'+aData[1]+'/">'+aData[1]+'</a>');
                            $('td:eq(2)', nRow).html('<a href="/task/request/'+aData[2]+'/">'+aData[2]+'</a>');
                        }"""

        bServerSide = True
        sAjaxSource = '/task/task_table/'



@datatables.datatable(ProductionTaskTable, name='fct')
def task_table(request):
    qs = request.fct.get_queryset()
    request.fct.update_queryset(qs)
    return TemplateResponse(request, 'task/_datatable.html', {  'title': 'Production Tasks Table', 'active_app' : 'task', 'table': request.fct,
                                                                'parent_template': 'task/_index.html'})

