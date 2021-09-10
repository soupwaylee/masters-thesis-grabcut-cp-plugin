import numpy as np


class ImageHandler:
    images = np.load('./studyimages.npz')

    @staticmethod
    def get_image(img_id):
        return ImageHandler.images.get(f'{img_id}', None)

    @staticmethod
    def get_image_as_response(img_id):
        result = ImageHandler.get_image(f'{img_id}')
        if result is not None:
            return np.ravel(result).tolist()


    #TODO
    # nz_size = np.transpose(np.nonzero(result)).shape[0]
    # return {
    #     tuple(np.transpose(np.nonzero(result))[nz_idx]):
    #       result[tuple(np.transpose(np.nonzero(result))[nz_idx])]
    #     for nz_idx in range(nz_size)
    # }
