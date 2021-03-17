 
from os.path import join
import bpy
from bpy.path import abspath



def get_image_data_block(imageName):
    # type: (str) -> bpy.types.Image
    """This assumes your save your files in 
    ${projectRoot}/blender/blenderFiles/*.blend
    and that your images are in ${projectRoot}/images"""
    # filePath = abspath(bpy.data.filepath)
    # blenderFilesPath = dirname(filePath)
    # blenderPath = dirname(blenderFilesPath)
    # projectRootDirectoryPath = dirname(blenderPath)
    # imagesPath = join(projectRootDirectoryPath, "images")
    imagesPath = abspath(bpy.context.window_manager.converter_props.images_folder)

    return bpy.data.images.load(join(imagesPath, imageName), check_existing=True)
