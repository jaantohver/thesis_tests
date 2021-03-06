import os
import sys
import torch
import utils
import dataset
import numpy as np
import models.crnn as crnn
from PIL import Image
from torch.autograd import Variable
from subprocess import call

if len(sys.argv) < 2:
    print("No input folder specified.")
    exit()

if len(sys.argv) < 3:
    print("No ground truth list specified.")
    exit()

input_folder = sys.argv[1]
output_folder = sys.argv[2]

model_path = './data/crnn.pth'
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

model = crnn.CRNN(32, 1, 37, 256)
if torch.cuda.is_available():
    model = model.cuda()

print('loading pretrained model from %s' % model_path)

model.load_state_dict(torch.load(model_path))

converter = utils.strLabelConverter(alphabet)

transformer = dataset.resizeNormalize((100, 32))

call(["rm", "-rf", "res"])
call(["mkdir", "res"])


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )

    return (matrix[size_x - 1, size_y - 1])

for dirname, dirnames, filenames in os.walk(input_folder):
    if len(filenames) > 0:
        if any('jpg' in s for s in filenames):
            count = 0
            relativeAccuracy = 0
            true_count = 0
            false_count = 0
            file_count = sum(1 for _ in ('jpg' in s for s in filenames))

            res_folder = "res/" + output_folder + '/' + dirname.split('/')[-1]
            res_file = res_folder + "/output.txt"
            call(["mkdir", "-p", res_folder])
            call(["touch", res_file])

            for filename in filenames:
                if ".jpg" not in filename:
                    continue

                true_label = filename.split('.')[0]
                true_label = ''.join(e for e in true_label if e.isalnum()).lower()

                full_path = dirname + "/" + filename

                image = Image.open(full_path).convert('L')
                image = transformer(image)
                if torch.cuda.is_available():
                    image = image.cuda()
                image = image.view(1, *image.size())
                image = Variable(image)

                model.eval()
                preds = model(image)

                _, preds = preds.max(2)
                preds = preds.transpose(1, 0).contiguous().view(-1)

                preds_size = Variable(torch.IntTensor([preds.size(0)]))
                raw_pred = converter.decode(preds.data, preds_size.data, raw=True)
                sim_pred = converter.decode(preds.data, preds_size.data, raw=False)

                count += 1

                if true_label == sim_pred:
                    true_count += 1
                else:
                    false_count += 1

                levDis = levenshtein(true_label, sim_pred)
                bigger = max(len(true_label), len(sim_pred))
                pct = (bigger - levDis) / bigger
                relativeAccuracy += (pct * 100) / file_count

                f = open(res_file, "a")
                f.write(str(true_label) + " - " + str(sim_pred) + " - " + str(pct * 100) + "\n")

            if true_count is 0:
                f.write("Accuracy = 0%\n")
            else:
                f.write("True count = " + " " + str(true_count) + "; false count = " + str(false_count) +
                        "; accuracy = " + str(true_count * 100 / count) + "%\n")

            f.write("Relative accuracy = " + str(relativeAccuracy) + "%\n")
