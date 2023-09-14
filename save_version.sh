VERSION=FINETUNE_EARLY_STOP_LOSS_600_path_w2v_new_embedd_change
mkdir -p output/versions/${VERSION}
mkdir -p output/versions/${VERSION}/code
cp output/test* output/versions/${VERSION}
cp output/dev.* output/versions/${VERSION}
cp output/result.xlsx output/versions/${VERSION}
cp output/result.xlsx output/versions/${VERSION}
cp data/*.jsonl output/versions/${VERSION}
cp *.py output/versions/${VERSION}/code
cp *.sh output/versions/${VERSION}/code
cp -r output/checkpoint-last output/versions/${VERSION}
mv screenlog.0 output/versions/${VERSION}