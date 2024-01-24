python3 run.py --do_test --do_train --do_eval \
 --train_steps 1000 --eval_steps 100 \
--max_source_length 50 --max_target_length 30 \
--train_batch_size 32 --eval_batch_size 32 \
--model_name_or_path Salesforce/codet5-base --model_type roberta  \
--train_filename cmg.valid.jsonl --dev_filename cmg.valid.jsonl --test_filename cmg.test.jsonl  \
--output_dir output