#!/usr/bin/env bash
set +e

export HARNESS_SERVER_ADDRESS=${HARNESS_SERVER_ADDRESS:-localhost}
export HARNESS_SERVER_PORT=${HARNESS_SERVER_PORT:-9090}
export host_url="http://${HARNESS_SERVER_ADDRESS}:${HARNESS_SERVER_PORT}"

data_folder=data
engine_json=${1:-./data/engines/ecommerce-purchase.json}
engine=ecommerce_electronic_p_10k #MAKE SURE THIS NAME IS THE SAME CONTAINED IN THE FILE NAME

train_file=${2:-./data/input_data/2019-Nov-sample-train-eletronics-purch-10kusers.csv}
test_file=${3:-./data/input_data/2019-Nov-sample-test-eletronics-userid-10kusers.csv}
results_file=${4:-./data/results/predictions-test.json}

echo "============================================="
echo "Settings used:"
echo "    Harness address: $HARNESS_SERVER_ADDRESS"
echo "    Harness port: $HARNESS_SERVER_PORT"
echo "    Full Harness URL: $host_url"
echo "    Engine json: $engine_json"
echo "    Train file: $train_file"
echo "    Test file: $test_file"
echo "    Results output file: $results_file"
echo "============================================="

sleep_time=20

echo
echo "----------------------------------------------------------------------------------------------------------------"
echo "Universal Recommender for ecommerce"
echo "----------------------------------------------------------------------------------------------------------------"
echo


echo "Wipe the Engine clean of data and model first"
harness-cli delete ${engine}
sleep 10
harness-cli add ${engine_json} || true
sleep 10

echo
echo "Sending input data"
echo
python3 ${data_folder}/python/import_ecommerce_data.py --engine_id ${engine} --input_file ${train_file} --url ${host_url}
#for view-category as secondary action run the following python file
#python3 ${data_folder}/python/import_ecommerce_data_category.py --engine_id ${engine} --input_file ${train_file} --url ${host_url}

echo
echo "Training a new model...."

harness-cli train $engine
echo "Wait ${sleep_time} seconds"
sleep ${sleep_time} # wait for training to complete
echo "Training complete!"
echo "Sending UR queries"
echo
read -n1 -r -p "Press a key to send queries..." key #have a look at elasticsearch and make sure the engine is listed with input events before sending queries

echo
python3 ${data_folder}/python/create_recommendation.py --engine_id ${engine} --url ${host_url} --input_file ${test_file} --output_file ${results_file}
