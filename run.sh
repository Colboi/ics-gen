
python init.py

for script in getter/*.py; do
    if [ -f "$script" ]; then
        echo "Running $script"
        python "$script"
    fi
done

python icsGen.py