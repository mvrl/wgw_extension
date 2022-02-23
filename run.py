from dataset import ObjectDataModule, ObjectDataset
import pytorch_lightning as pl
from pathlib import Path
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms.functional import convert_image_dtype
import csv
from collections import Counter
import torch
from argparse import ArgumentParser

def write_csv(headers, results, file_name):
		with open(file_name, 'w', encoding='UTF8', newline='') as f:
			csvwriter = csv.writer(f) 
			csvwriter.writerow(headers) 
			csvwriter.writerows(results)

def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-ni", "--num_items", type=int, default=None, help="Data size"
    )
    parser.add_argument(
        "-bs", "--batch_size", type=int, default=2, help="Batch Size"
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=2, help="Number of workers"
    )
    parser.add_argument(
        "-si", "--start_index", type=int, default=0, help="Starting index"
    )
    parser.add_argument(
        "-g", "--gpu", type=int, default=0, help="Gpu number"
    )
    return parser.parse_args()

if __name__ == "__main__":
	args = get_args()
	print(args)
	device_name = f'cuda:{args.gpu}'
	device = torch.device(device_name if torch.cuda.is_available() else 'cpu')
	label_names = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
	]

	dm = ObjectDataModule(
		cvusa_root = Path("/u/eag-d1/data/crossview/cvusa/"),
		start_index=args.start_index,
		num_items=args.num_items,
		num_workers=args.workers,
		batch_size=args.batch_size
	)
	dm.setup()
	score_threshold = 0.8
	num_labels = 91
	model = fasterrcnn_resnet50_fpn(pretrained=True, progress=False)
	model = model.to(device)
	model = model.eval()
	results = []
	for batch in dm.train_dataloader():
		
		# output = model(batch['image'])
		d = batch['image'].to(device)
		output = model(d)
		for out, img_id, lat, lon in zip(output, batch['image_id'], batch['lat'], batch['lon']):
			try:
				all_labels = [""]*num_labels
				mask = out['scores'] > score_threshold
				labels_idx = out['labels'][mask]
				labels = Counter(labels_idx.tolist())
				for index, count in labels.items():
					all_labels[index] = count	
				row = [img_id, float(lat), float(lon)]
				row.extend(all_labels)
				results.append(row)
			except Exception as e:
				print(f'error with image {img_id}, error msg {e.message}, args {e.args}')
				continue
	name = f'out/object_detection_{args.start_index}_{args.num_items}.csv'
	headers = ['image_id', 'latitude', 'longitude']
	headers.extend(label_names)
	write_csv(headers, results, name)
	print('completed!')


	