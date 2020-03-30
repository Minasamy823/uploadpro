import urllib.request as urllib
from io import BytesIO
import base64
from django.http import HttpResponseRedirect
from django.shortcuts import render
import imagehash
from .forms import *
from .models import Image as Model
from PIL import Image
import os
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


def ChangeImage(request, hash):
    template_name = 'detail.html'
    image_name = Model.objects.get(hash=hash).image.name
    im = Image.open('media/' + image_name).convert('RGB')
    width = request.GET.get('width', im.width)
    height = request.GET.get('height', im.height)
    size = request.GET.get('size', 0)
    data = {'width': width, 'height': height, 'size': size}
    form = ParamsForm(data)

    if form.is_valid():

        if width in ('0', ''):
            width = im.width
        if height in ('0', ''):
            height = im.height
        if size in ('0', ''):
            size = 0

        size = abs(int(size))
        width = abs(int(width))
        height = abs(int(height))

        im = im.resize((width, height), Image.ANTIALIAS)
        buffered = BytesIO()

        if size == 0:
            im.save(buffered, format="jpeg", quality=100)
        else:
            for x in range(91, 0, -10):
                buffered = BytesIO()
                im.save(buffered, format="jpeg", optimize=True, quality=x)

                if x == 1 or buffered.tell() < size:
                    break
                else:
                    buffered.close()
        image = str(base64.b64encode(buffered.getvalue()))[2:-1]

    context = {'context': '',
               'image': image,
               'width': width,
               'height': height,
               'size': size,
               'ParamsForm': form
               }
    return render(request, template_name, context)


def imagesList(request):
    if request.method == 'GET':
        template_name = 'list.html'
        images = Model.objects.all()
        context = {'images': images}
        return render(request, template_name, context)


def uploading(request):
    if request.method == 'GET':
        template_name = 'upload.html'
        form = ImageForm()
        context = {'form': form}
        return render(request, template_name, context)

    if request.method == 'POST':
        template_name = 'upload.html'
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            url = form.cleaned_data['url']
            pic = form.cleaned_data["image"]
            if pic:
                hash = str(imagehash.average_hash(Image.open(pic)))
                im = Model(hash=hash, image=pic)
                im.save()
                return HttpResponseRedirect('/')
            if url:
                fname = os.path.basename(url)
                image_url = urllib.urlretrieve(url)
                im = Image.open(image_url[0])
                hash_img = str(imagehash.average_hash(im))

                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urllib.urlopen(url).read())
                img_temp.flush()

                mo = Model()
                mo.hash = hash_img
                mo.image.save(fname, File(img_temp))

                return HttpResponseRedirect('/')
        else:
            context = {'form': form}
            return render(request, template_name, context)
