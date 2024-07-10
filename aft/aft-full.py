import torch
from torch import nn
import torch.nn.functional as F


class AFT_Full(nn.Module):
    def __init__(self, max_len, d_model):
        super().__init__()
        self.d_model = d_model
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w = nn.Parameter(torch.Tensor(max_len, max_len))
        self.out = nn.Linear(d_model, d_model)

    def forward(self, x):
        batch_size, seq_len, _ = x.shape

        q = self.w_q(x)
        k = self.w_k(x)
        v = self.w_v(x)

        w_bias = self.w[:seq_len, :seq_len].unsqueeze(0)

        print('w_bias.shape:', w_bias.shape)
        print('k.shape:', k.shape)

        num = torch.exp(w_bias) @ (torch.exp(k) * v)
        den = torch.exp(w_bias) @ torch.exp(k)
        y = F.sigmoid(q) * num / den

        return self.out(y)


if __name__ == '__main__':
    model = AFT_Full(100, 64)
    x = torch.randn(256, 56, 64)
    y = model(x)
    print(y)
