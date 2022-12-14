import pytorch_lightning as pl
from pathlib import Path
from argparse import ArgumentParser
from methods import ObjectDistributionModel
from object_distribution_dataset import ObjectDistributionDataModule
from pytorch_lightning.plugins import DDPPlugin

def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-ni", "--num_items", type=int, default=None, help="Data size"
    )
    parser.add_argument(
        "-bs", "--batch_size", type=int, default=32, help="Batch Size"
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=4, help="Number of workers"
    )
    parser.add_argument(
        "-si", "--start_index", type=int, default=0, help="Starting index"
    )
    parser.add_argument(
        "-g", "--gpu", type=int, default=0, help="Gpu number"
    )
    parser.add_argument(
        "-e", "--epochs", type=int, default=20, help="Max Epochs"
    )
    parser.add_argument(
        "-ls", "--log_step", type=int, default=1000, help="Log Step"
    )
    parser.add_argument(
        "-odsr", "--object_dataset_root", type=str, default="out/", help="Object Dataset Root"
    )
    parser.add_argument(
        "-dr", "--data_root", type=str, default="/localdisk1/data/cvusa_eag", help="CSV Dataset Path"
    )
    return parser.parse_args()

def train():
    args = get_args()
    print(args)
    obj_dist_dm = ObjectDistributionDataModule(
        cvusa_root = Path(args.data_root),
        start_index=args.start_index,
        num_items=args.num_items,
        num_workers=args.workers,
        batch_size=args.batch_size,
        obj_dataset_root=args.object_dataset_root
    )
    obj_dist_dm.prepare_data()
    obj_dist_dm.setup()

    model = ObjectDistributionModel()
    if args.gpu == -1:
        gpu = -1
    else:
        gpu = [args.gpu]

    trainer = pl.Trainer(
        max_epochs=args.epochs, 
        precision=16, 
        gpus=gpu,
        plugins=DDPPlugin(find_unused_parameters=False),
        log_every_n_steps=args.log_step
        )
    trainer.fit(model, obj_dist_dm)

if __name__ == "__main__":
    train()
