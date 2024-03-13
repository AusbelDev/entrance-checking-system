sed 1d ./data/dummy_data/generated_customers_data.csv | sqlite3 ./database/gym_members_db.sqlite <<EOF
.mode csv
.import /dev/stdin members
EOF