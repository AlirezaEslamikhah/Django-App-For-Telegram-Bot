# # myapp/views.py
# from rest_framework.parsers import FileUploadParser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
from rest_framework.viewsets import ModelViewSet	
from .models import Image
from .serializers import ImageSerializer
from rest_framework import status
from PIL import Image as pilimage  
import PIL
from rest_framework.response import Response

import os
import subprocess
ocr_output = "posted.jpg"
import shutil # for delete files which generated from ocr
def delete_files_in_directory(directory_path):
    # Delete the entire directory including its contents
    try:
        shutil.rmtree(directory_path)
        print(f"Deleted: {directory_path}")
    except Exception as e:
        print(f"Error deleting {directory_path}: {e}")
class CustomError(Exception):
    pass
def extract_national_code():
# file_path = os.path.dirname(os.path.abspath(__file__))+"\\output\\out_posted.txt"
    file_path = os.path.dirname(os.path.abspath(__file__))+"\\output"

    files = [os.path.join(file_path, file) for file in os.listdir(file_path)]
    try:
        if len(files) > 1:
            raise CustomError("ERROR:more than one file in output")
        # Define the specific Persian character you're looking for
        target_character = ['شماره' , 'ملی']  # Replace with your specific Persian character

        # Open the file and read its lines
        with open(files[0], 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Extract lines containing the specific Persian character
        for specific_string in target_character:
            matching_lines:list = [line.strip() for line in lines if specific_string in line]
            if len(matching_lines)>0:
                break
        if len(matching_lines)>1:
            raise CustomError("ERROR:more than on matching lines")
        numeric_string = ''.join(c for c in matching_lines[0] if c.isdigit())#we can use regex but each time must compile regex library i think indeed i use is digit
    except CustomError as e:
        print(f"Custom Error: {e}")
        return str(e)
    return numeric_string
class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    def process_image(self , image):
        global ocr_output
        current_directory = os.path.dirname(os.path.abspath(__file__))
        saved_image_path = os.path.join(current_directory,'data')
        # creating a image object (main image)  
        im1 = pilimage.open(image)  
        
        # save a image using extension 
        im1 = im1.save(saved_image_path+'\\'+ocr_output) 
        subprocess.run(['python',current_directory+"\\src\\ocr.py"], capture_output=True, text=True)
        result = extract_national_code()
        delete_files_in_directory(current_directory+"\\output")#must delete output directory because we want just one out put not multiple output
        return result
    def create(self, request, *args, **kwargs):
        image_data = request.data.get('image')

        # Call the custom function to process the image


        # Call the original create method
        response = super().create(request, *args, **kwargs)#i don't want to create image because we don't need this but for short time i do in this approach
        processed_data = self.process_image(image_data)
        if 'ERROR' in processed_data:
            return Response({'error': processed_data.replace('ERROR:','')}, status=status.HTTP_400_BAD_REQUEST)

        # Customize the response as needed
        if response.status_code == status.HTTP_201_CREATED:
            # Add additional data to the response
            response.data['national_code'] = processed_data

        return response
    # parser_classes = (FileUploadParser,)

    # def post(self, request, *args, **kwargs):
    #     file_obj = request.FILES['image']
    #     serializer = ImageSerializer(data={'image': file_obj})

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
