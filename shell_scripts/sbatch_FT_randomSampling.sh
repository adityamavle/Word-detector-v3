#!/bin/bash
#SBATCH -A sreevatsa
#SBATCH -n 30
#SBATCH --gres=gpu:3
#SBATCH --mem-per-cpu=2G
#SBATCH --time=6-00:00:00
#SBATCH --job-name=finetune_v3
#SBATCH --output=train_v3.txt
#SBATCH -w gnode039


source /home2/sreevatsa/doctr-env/bin/activate
echo "Running script..."
module load u18/cuda/10.2
module load u18/cudnn/7.6.5-cuda-10.2
python3 -m torch.distributed.launch --nproc_per_node=2 /home2/sreevatsa/docTR/trainmodel-v3.py --resume /home2/sreevatsa/models/Doctr-v3-run4_epoch1.pt  --wb --freeze-backbone --name "Doctr-v3-run5"
echo "Script finished running" #add the new and old consort updated paths
