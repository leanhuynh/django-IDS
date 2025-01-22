from django.shortcuts import render, get_object_or_404
from .models import Role, User
from .form.register_form import RegisterForm
from .form.edit_form import EditForm
import bcrypt
from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict
from .utils.request import read_request_put

ROLE_DEFAULT = 1

# Create your views here.  
def index(request):
    return render(request,'../templates/adminlte/pages/index.html')

def create(request):
    try:
        if request.method == "POST":
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                # get all info from form
                cleaned_data = form.cleaned_data
                name = cleaned_data['name']
                email = cleaned_data['email']
                password = cleaned_data['password']
                # role_id = cleaned_data['role_id']
                role_id = ROLE_DEFAULT
                avatar = cleaned_data['avatar']

                # save image into storage
                new_user = User(
                    name=name,
                    email=email,
                    password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                    role_id=role_id,
                    avatar=avatar
                )

                new_user.save()
                new_user_json = model_to_dict(new_user)
                new_user_json['avatar'] = new_user.avatar.url
                new_user_json.pop('password', None)

                return JsonResponse({'message': 'Create new user successfully!', 'user':  new_user_json}, status=201)
            else:
                return JsonResponse({'message': 'Form is not validate!', 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'message': 'Method not allowed!'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e) + '!'}, status=500)
    
def edit(request, id):
    try:
        # validate id
        if not id:
            return JsonResponse({'message': 'Id is invalidated!!'}, status=400)
        
        if request.method == "PUT":
            form_data, files = read_request_put(request)
            form = EditForm(form_data, files)

            if form.is_valid():
                # get all info from form
                cleaned_data = form.cleaned_data
                name = cleaned_data['name']
                email = cleaned_data['email']
                password = cleaned_data['password']
                # role_id = cleaned_data['role_id']
                role_id = ROLE_DEFAULT
                avatar = cleaned_data['avatar']

                # get user by id
                user = get_object_or_404(User, id=id)
                user.name = name if name != user.name else user.name
                user.email = email if email != user.email else user.email
                user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user.avatar = avatar or user.avatar
                user.role_id = role_id if role_id != user.role_id else user.role_id
                user.save()

                user_json = model_to_dict(user)
                user_json['avatar'] = user.avatar.url
                user_json.pop('password', None)

                return JsonResponse({'message': f'Update user {user.name} successfully!', 'user':  user_json}, status=200)
            else:
                return JsonResponse({'message': str(form.errors), 'errors': str(form.errors)}, status=400)
        else:
            return JsonResponse({'message': 'Method not allowed!'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e) + '!'}, status=500)
    
    # if request.method == "PUT":
    #     # Gắn bộ xử lý file tạm thời
    #     request.upload_handlers.insert(0, TemporaryFileUploadHandler())

    #     # Sử dụng MultiPartParser để phân tích request.body
    #     content_type = request.META.get('CONTENT_TYPE', '')
    #     if 'multipart/form-data' in content_type:
    #         try:
    #             parser = MultiPartParser(request.META, request, request.upload_handlers)
    #             data, files = parser.parse()
                
    #             # Chuyển dữ liệu thành dictionary
    #             form_data = data.dict()
    #             # file_data = {key: value.name for key, value in files.items()}

    #             # Kết hợp form data và file data
    #             # form_data.update(file_data)
    #             print(form_data)
    #             return JsonResponse({'message': form_data}, status=200)
    #         except Exception as e:
    #             return JsonResponse({'message': f'Error parsing multipart/form-data: {str(e)}'}, status=400)
    #     else:
    #         return JsonResponse({'message': 'Unsupported Content-Type!'}, status=400)

    # return JsonResponse({'message': 'Method not allowed!'}, status=405)

def search(request):
    try:
        if request.method == "GET":
            keyword = request.GET.get('keyword', '')
            users = User.objects.filter(email__icontains=keyword) | User.objects.filter(name__icontains=keyword)
            users_json = []
            for user in users:
                user_json = model_to_dict(user)
                user_json['avatar'] = user.avatar.url if user.avatar else None
                user_json.pop('password', None)
                users_json.append(user_json)

            return JsonResponse({'users': users_json}, status=200)
        else:   
            return JsonResponse({'message': 'Method not allowed'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

def delete(request):
    try:
        if request.method == 'DELETE':
            id = request.GET.get('id', '')
            if not id:
                return JsonResponse({'message': 'Id is invalidated!!'}, status=400)
            
            user = get_object_or_404(User, id=id)

            if not user:
                return JsonResponse({'message': 'Not found user!!'}, status=400)
            
            # delete user
            user.delete()
            return JsonResponse({'message': f"User '{user.name}' deleted successfully!!"}, status=200)
            # form = DeleteForm(request.DELETE)
            # if form.is_valid():
            #     cleaned_data = form.cleaned_data
            #     id = cleaned_data['id']
            #     email = cleaned_data['email']
            #     raise Exception(email)
            
            #     # find user
            #     user = get_object_or_404(User, id)
            #     if user.email != email:
            #         return JsonResponse({'message': 'Not found user with given email'}, status=400)
                
            #     # delete user
            #     user.delete()
            #     return JsonResponse({'message': f'User {email} deleted successfully!!'}, status=200)
            
            # return JsonResponse({'message': 'Form is not validate!', 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'message': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({'message': str(e) + '!'}, status=500)