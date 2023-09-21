import math
import torch.nn as nn

class Discriminator(nn.Module):
    def __init__(self, channels_img, features_d, alpha, img_size):
        super(Discriminator, self).__init__()
        
        layers = []
        
        # Determinar quantas camadas são necessárias com base no tamanho da imagem
        num_blocks = int(math.log2(img_size)) - 3  # 3 é subtraído porque terminamos com 4x4 (2^2) e queremos começar de img_size
        
        # Camada inicial
        layers.append(nn.Conv2d(channels_img, features_d, 4, 2, 1))
        layers.append(nn.LeakyReLU(alpha))
        
        # Blocos intermediários
        in_channels = features_d
        for i in range(num_blocks):
            out_channels = in_channels * 2
            layers.append(self._block(in_channels, out_channels, alpha))
            in_channels = out_channels
        
        # Camada final
        layers.append(nn.Conv2d(in_channels, 1, 4, 2, 0))
        
        self.disc = nn.Sequential(*layers)

    def _block(self, in_channels, out_channels, alpha):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 4, 2, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(alpha)
        )

    def forward(self, x):
        return self.disc(x)