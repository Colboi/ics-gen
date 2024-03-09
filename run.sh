cd /home/ubuntu/ics-gen/
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate ics

python init.py

for script in getter/*.py; do
    if [ -f "$script" ]; then
        echo "Running $script"
        python "$script"
    fi
done

python icsGen.py