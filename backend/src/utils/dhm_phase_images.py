import numpy as np


class ImageHandler:
    img_data = np.load('./testimages.npz')
    # needed to create explicit scope for img_data here
    # in order to bypass absence of class body in scope
    images = (lambda img_data=img_data:
              {f'{i}': img_data[f'img{i}']
               for i in range(1, len(img_data) + 1)})()

    @staticmethod
    def get_image(img_id):
        return ImageHandler.images.get(img_id, None)

    @staticmethod
    def get_image_as_response(img_id):
        result = ImageHandler.get_image(img_id)
        if result is not None:
            return np.ravel(result).tolist()


    #TODO
    # nz_size = np.transpose(np.nonzero(result)).shape[0]
    # return {
    #     tuple(np.transpose(np.nonzero(result))[nz_idx]):
    #       result[tuple(np.transpose(np.nonzero(result))[nz_idx])]
    #     for nz_idx in range(nz_size)
    # }
