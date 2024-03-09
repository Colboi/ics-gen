source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate ics
gunicorn -b 0.0.0.0:8000 server:app