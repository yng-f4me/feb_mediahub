'''
Get_object_or_404: This function is used to retrieve an object 
from the database based on certain criteria. If the object is not found, it raises a 404 error.
'''

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Alerts
'''
To control content fetch i.e. if database has a lot of records 
we fetch the records in batches
'''
from django.core.paginator import Paginator
from django.db.models import Q # Q : query : sending commands to db
from .models import MediaAssets
from .forms import MediaAssetsForm

# Create your views here.


@login_required 
def dashboard_view(request):
    '''
    main dashboard to show all public media assets
    '''
    # Fetch all public media assets
    media_list = MediaAssets.objects.filter(is_public=True)

    # Get data from a form using the name attribute
    # This powers a search functionality for any user to be able to filter the media assetss
    query = request.GET.get('q')
    if query:
        media_list = media_list.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )

    # Content pagination(showcase data to user in batches (12)) 
    paginator = Paginator(media_list, 12)

    # Request the template to display more pages
    page_number = request.GET.get('page')
    media_assets = paginator.get_page(page_number)
    return render(request, 'media_assets/dashboard.html', 
    {
        'media_assets': media_assets,
        'query': query
    })

# View to show only media files belonging to the logged in user
@login_required
def my_media_view(request):
    '''
    user own media assets
    '''
    media_list = MediaAssets.objects.filter(uploaded_by=request.user)
    
    # pagination
    paginator = Paginator(media_list, 12)
    page_number = request.GET.get('page')
    media_assets = paginator.get_page(page_number)
    return render(request, 'media_assets/my_media.html',{
        'media_assets': media_assets
    })

# upload view (class)
@login_required
def upload_view(request):
    if request.method == 'POST':
        form = MediaAssetsForm(request.POST, request.FILES)
        if form.is_valid():
            media_asset = form.save(commit=False) # Delayed post
            media_asset.uploaded_by = request.user  # Tagging user to post
            media_asset.save()
            messages.success(request, 'Media asset uploaded successfully!')
            # return redirect('media_assets:my_media')
            return redirect('media_assets:dashboard') 
    else:
            form = MediaAssetsForm()
    return render(request, 'media_assets/upload_media.html',{
            'form': form
        })


# View to expose full media details
# View to alsp be used in updating the view count 
@login_required
def media_detail_view(request,pk):
    '''pk : primary key(uniquely identifies a record in
    a db table) : we use this to identify the role 
    of the current user'''
    '''showcase the full details of a media assets'''
    # get_object_or_404 to handle the data fetch 
    # i.e if object exists tag it if not showcases a 404 page.
    media = get_object_or_404(MediaAssets,pk=pk)
    # app specifications # tag on whether media is private or not
    if not media.is_public and media.uploaded_by != request.user and not request.user.is_teacher() and not request.user.is_superuser:
        messages.error(request,"This media is private!!")
        return redirect('media_assets:dashboard')
    ## if user is a teacher,superuser or the media is public
    # increment the view count 
    media.views_count += 1 # updating the medias view count 
    media.save(update_fields=['views_count'])
    # compute edit and delete permissions for the media 
    # the user can only edit or delete if they uploaded the media
    # or they are a superuser/teacher
    can_edit = media.can_edit(request.user)
    can_delete = media.can_delete(request.user)
    return render(request, 'media_assets/media_detail.html',{
        'media' : media,
        'can_edit': can_edit,
        'can_delete' : can_delete,
    })

# edit and deleting views (when user wants to edit or delete 
# items)
def edit_media_view(request,pk):
    '''only allow editing if user is the person who uploaded
    media or superuser/teacher'''
    media = get_object_or_404(MediaAssets,pk=pk)
    if not media.can_edit(request.user):
        messages.error(request,"You cannot edit this file")
        return redirect('media_assets:dashboard')
    if request.method == 'POST':
        form = MediaAssetsForm(request.POST,request.FILES,
        instance=media)
        # Correct
        if form.is_valid():

            form.save()
            messages.success(request,"Media Asset Updated!")
            return redirect("media_assets:media_detail",pk=pk)
    else: 
        form = MediaAssetsForm(instance=media)
    return render(request, 'media_assets/edit_media.html',{
        'form' : form,
        'media' : media,
    })

@login_required
def delete_media_view(request,pk):
    '''delete media assets based off pk'''
    media = get_object_or_404(MediaAssets,pk=pk)
    if not media.can_delete(request.user):
        messages.error(request,"You cannot delete media")
        return redirect('media_assets:dashboard')
    if request.method == 'POST':
        media.delete() # delete from db 
        messages.success(request,"Deleted Successfully")
        return redirect('media_assets:my_media')

    return render(request,'media_assets/delete_media.html',{
        'media':media
    })