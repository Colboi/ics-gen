# preparing environment 
cd /home/ubuntu/ics-gen/
source /home/ubuntu/miniconda3/etc/profile.d/conda.sh
conda activate ics

# initialize events.json
python init.py

# run scripts to get events
for script in eventsGetter/*.py; do
    if [ -f "$script" ]; then
        echo "Running $script"
        python "$script"
    fi
done

# generate schedule.ics
python icsGen.py