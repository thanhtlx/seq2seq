VERSION=FINETUNE_EARLY_STOP_LOSS_WITH_TYPE
mkdir output/versions/${VERSION}
cp output/test* output/versions/${VERSION}
cp output/dev.* output/versions/${VERSION}
cp output/result.xlsx output/versions/${VERSION}
cp output/result.xlsx output/versions/${VERSION}
cp data/*.jsonl output/versions/${VERSION}
cp -r output/checkpoint-last output/versions/${VERSION}
mv screenlog.0 output/versions/${VERSION}