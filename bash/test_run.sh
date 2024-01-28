#! /bin/bash
# clear existing test dir
rm -r ./Tester

# unzip clean copy of test dir
unzip "Tester.zip"

# show old
echo "Start State:"
tree Tester

echo "Organising..."
python3 ./python/modules/organise_by_type.py
 
echo "Complete."
tree Tester

echo "Testing "


