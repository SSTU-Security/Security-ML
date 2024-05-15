from AdaFace import net
import torch
import os
import cv2
import numpy as np

adaface_models = {
    "ir_18": "weigts/adaface_ir18_casia.ckpt",
    "ir_50": "weigts/adaface_ir50_webface4m.ckpt",
    'ir_101': "weigts/adaface_ir101_webface4m.ckpt",
}


class Verificathion:
    def __init__(self, architecture='ir_50'):
        assert architecture in adaface_models.keys()
        self.model = net.build_model(architecture)
        statedict = torch.load(adaface_models[architecture])['state_dict']
        model_statedict = {key[6:]: val for key, val in statedict.items() if key.startswith('model.')}
        self.model.load_state_dict(model_statedict)
        self.model.to("cuda")
        self.model.eval()

    def to_input(self, pil_rgb_image):
        np_img = np.array(pil_rgb_image)
        brg_img = ((np_img[:, :, ::-1] / 255.) - 0.5) / 0.5
        tensor = torch.tensor([brg_img.transpose(2, 0, 1)]).float()
        return tensor

    def mypredict(self, img):
        features = []
        test_image_path = 'usersImage'
        img_c = cv2.resize(img, (112, 112))
        bgr_tensor_input = self.to_input(img_c)
        feature, _ = self.model(bgr_tensor_input.to("cuda"))
        features.append(feature)
        name = []
        for fname in sorted(os.listdir(test_image_path)):
            name.append(fname)
            img =  cv2.resize(cv2.imread(os.path.join(test_image_path, fname)), (112, 112))
            bgr_tensor_input = self.to_input(img)
            feature, _ = self.model(bgr_tensor_input.to("cuda"))
            features.append(feature)

        da = (torch.cat(features) @ torch.cat(features).T)[0][1:]
        index = np.argmax(da.cpu().detach().numpy())
        return da[index], name[index]
