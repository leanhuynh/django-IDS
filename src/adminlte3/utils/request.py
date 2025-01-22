from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http.multipartparser import MultiPartParser

def read_request_put(request):
    # Gắn bộ xử lý file tạm thời
    request.upload_handlers.insert(0, TemporaryFileUploadHandler())

    # Sử dụng MultiPartParser để phân tích request.body
    content_type = request.META.get('CONTENT_TYPE', '')
    if 'multipart/form-data' in content_type:
        try:
            parser = MultiPartParser(request.META, request, request.upload_handlers)
            data, files = parser.parse()
            
            # Chuyển dữ liệu thành dictionary
            data_dict = data.dict()  # Dữ liệu form thông thường
            for key, value in files.items():
                data_dict[key] = value  # Thêm file vào dictionary
    
            # Kết hợp form data và file data
            return data_dict, files
        except Exception as e:
            raise e
    else:
        raise Exception('unsupported content-type!')