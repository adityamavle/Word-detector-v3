#SBATCH -A sreevatsa
#SBATCH -n 20
#SBATCH --gres=gpu:2
#SBATCH --mem-per-cpu=2G
#SBATCH --time=4-00:00:00
#SBATCH --job-name=getTables
#SBATCH --output=p5piio.txt
#SBATCH -w gnode055

source /home2/sreevatsa/doctr-env/bin/activate
echo "Starting...."
module load u18/cuda/10.2
module load u18/cudnn/7.6.5-cuda-10.2
python3 /home2/sreevatsa/docTR/Misc/recallsort_model_1.py --resume "/home2/sreevatsa/models/final/db_resnet50.pt" --ext 'jpg','png','jpeg'