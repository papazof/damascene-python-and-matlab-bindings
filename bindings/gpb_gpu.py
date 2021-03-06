from __future__ import division
import numpy as np
import os
from scipy.weave import inline,converters

cur_dir=os.path.abspath(os.path.dirname(__file__))

# Set library dirs here
cuda_path="/usr/local/cuda/lib64"
acml_path="/usr/local/acml/gfortran64/lib"
damascene_path=os.path.join(cur_dir, '../build')

libraries="cuda cudart cublas acml damascene".split()
library_dirs=[cuda_path,acml_path,damascene_path]

# Set compiler options
compiler='gcc'
extra_cmp_args=['-Wno-cpp',' -Wno-parentheses'] # disable generated NumPy warnings

def gpb(image):
    [height, width]=image.shape[:2]
    borders=np.zeros([height,width],np.float32)
    orientations=np.zeros([8,width,height],np.float32)
    textons=np.zeros([height,width],np.int32)
    padded_image=np.zeros([height,width,1],np.uint8)
    padded_image[:,:,:0]=image.astype(np.uint8)
    float_boundaries=image.astype(np.float32)/255
     	
	#print padded_image
    print padded_image.shape
    np.unique(float_boundaries)
    code="""
         gpb((float*)&padded_image(0,0),width,height,&borders(0,0),&textons(0,0),&orientations(0,0));
         """
    inline(code, ['padded_image','textons','width', 'height','borders','orientations'], type_converters=converters.blitz,
           compiler=compiler, extra_compile_args=extra_cmp_args,
           headers=['"'+os.path.join(cur_dir, 'gpb.h')+'"'], include_dirs=['.'],
           libraries=libraries, library_dirs=library_dirs, runtime_library_dirs=library_dirs,
           verbose=0, force=1)
    orientations=orientations.T
    return [borders,textons,orientations]


if __name__ == "__main__":
    from PIL import Image
    import matplotlib.pyplot as plt
    
    #image=Image.open('../damascene/polynesia.ppm');
    image=Image.open('./100007.png')
    data=np.array(image.getdata()).reshape(image.size[1],image.size[0],1)
    [borders,textons,orientations]=gpb(data);

    plt.matshow(borders)
    plt.matshow(textons)
    plt.show()

