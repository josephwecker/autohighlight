#! /bin/sh

for name in token tokenizer ah3 ah4 type;
do
    echo "Running test test-$name.py"
    python test-$name.py
done
grep '[^a-z]set(' *.py |grep -v utils.py
