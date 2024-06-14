import datetime
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Ticket
from .forms import CreateTicketForm,UpdateTicketForm


# View ticket details
def ticket_details(request,pk):
    ticket = Ticket.objects.get(pk=pk)
    context={'ticket':ticket}
    return render(request,'ticket/ticket_details.html',context)


"""For customers"""

# Create a ticket
def create_ticket(request):
    if request.method == 'POST'        :
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var=form.save(commit=False)
            var.created_by=request.user
            var.ticket_status='Pending'
            var.save()
            messages.info(request,"Your ticket has been successfully submitted. An enginner assign soon")
            return redirect('dashboard')        
        else:
            messages.warning(request,"Something went wrong. Please check input..!")
            return redirect('create-ticket')    
    else:
        form=CreateTicketForm()
        context={'form':form}
        return render(request,"ticket/create_ticket.html",context)

# Update ticket
def update_ticket(request,pk):
    ticket=Ticket.objects.get(pk=pk)
    if request.method == 'POST'        :
        form = UpdateTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.info(request,"Your ticket has been successfully updated and all changes are saved")
            return redirect('dashboard')        
        else:
            messages.warning(request,"Something went wrong. Please check input..!")
            #return redirect('create-ticket')    
    else:
        form=UpdateTicketForm(instance=ticket)
        context={'form':form}
        return render(request,"ticket/update_ticket.html",context)


# viewing all createdtickets
def all_tickets(request):
    ticket = Ticket.objects.filter(created_by=request.user)
    context={'ticket':ticket}
    return render(request,"ticket/all_ticket.hmtl",context)



"""For Engineers"""

# View ticket queue
def ticket_queue(request):
    tickets=Ticket.objects.filter(ticket_status='Pending')
    context = {'tickets':tickets}
    return render(request, 'ticket/ticket_queue.html',context)


# Accept aticket from the queue
def accept_ticket(request,pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to=request.user
    ticket.ticket_status='Active'
    ticket.accepted_date=datetime.datetime.now()
    ticket.save()
    messages.info(request," Ticket has been accepted. Please resolve as soon as possible!")
    return redirect('ticket-queue')

# Close a ticket
def close_ticket(request,pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status='Completed'
    ticket.is_resolved=True
    ticket.closed_date=datetime.datetime.now()
    ticket.save()
    messages.info(request," Ticket has been resolved. Thank you")
    return redirect('ticket-queue')


# ticket enginner is working on
def workspace(request):
    ticket = Ticket.objects.filter(assigned_to=request.user, is_resolved=False)
    context={'ticket':ticket}
    return render(request,'ticket/workspace.html',context)

# All closed/ Resolved tickets
def all_closed_tickeets(request):
    ticket=Ticket.objects.filter(assigned_to=request.user, is_resolved=True)
    context={'tickets':ticket}
    return render(request,'ticket/all_closed_tickets.html',context)